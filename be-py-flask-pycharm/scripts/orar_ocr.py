import datetime
import json
import multiprocessing
import os
import re
import time

import cv2
import numpy as np
import pytesseract
from joblib import Parallel, delayed

from scripts.utils import *

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

TEACHER_REGEX = '[A-Z]*[a-z]+[\s]{0,2}[A-Za-z]{1,2}[\s]*$'
TEACHER_REGEX_NO_SPACE = '[A-Z]*[a-z]+[\s]{0}[A-Za-z]{1,2}[\s]*$'


def resize_with_aspect_ratio(image, width=None, height=None, inter=cv2.INTER_AREA):
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)


def print_img(img):
    if img.shape[0] > 1500 or img.shape[1] > 1500:
        img = resize_with_aspect_ratio(img, 1280, 720)
    cv2.moveWindow('image', 200, 200)
    cv2.imshow('window', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_page_title(img):
    x, y = img.shape[0:2]
    cropped = img[0:int(x * 0.08), 0:y]
    page_title = pytesseract.image_to_string(cropped)
    return page_title


def get_cropped_hours_img(img):
    x, y = img.shape[0:2]
    cropped_ore = img[int(x * 0.08):int(x * 0.161), int(y * 0.085):y]
    return cropped_ore


def get_cropped_days_img(img):
    x, y = img.shape[0:2]
    cropped_days = img[int(x * 0.161):x, 0:int(y * 0.085)]
    return cropped_days


def get_cropped_classes_img(img):
    x, y = img.shape[0:2]
    cropped_classes = img[int(x * 0.161):x, int(y * 0.085):y]
    return cropped_classes


def get_binnary_img(img):
    thresh, img_bin = cv2.threshold(img, 115, 255, cv2.THRESH_BINARY)
    img_bin = 255 - img_bin
    return img_bin


def get_vh_lines_img(img):
    #     countcol(width) of kernel as 100th of total width
    kernel_len = np.array(img).shape[1] // 100
    #     Defining a vertical kernel to detect all vertical lines of image
    ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
    #     Defining a horizontal kernel to detect all horizontal lines of image
    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
    #     A kernel of 2x2 - filtru
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img_bin = get_binnary_img(img)
    #     Use vertical kernel to detect and save the vertical lines in a jpg
    #     Removal of all things except elements masked by kernel, in this case, vertical lines
    image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)

    vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)
    cv2.imwrite("extracted/binary.jpg", img_bin)
    cv2.imwrite("extracted/vertical.jpg", vertical_lines)
    #     Use horizontal kernel to detect and save the horizontal lines in a jpg
    image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
    # print_img(image_2)
    horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)

    # print_img(horizontal_lines)
    cv2.imwrite("extracted/horizontal.jpg", horizontal_lines)
    #     Combine horizontal and vertical lines in a new third image, with both having same weight.
    img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 1, 0.0)
    #     Eroding and thesholding the image

    img_vh = cv2.erode(~img_vh, kernel, iterations=2)
    thresh, img_vh = cv2.threshold(img_vh, 128, 255, cv2.THRESH_BINARY)

    cv2.imwrite("extracted/vh.jpg", img_vh)
    cv2.imwrite("extracted/base.jpg", img)
    bitxor = cv2.bitwise_xor(img, img_vh)
    cv2.imwrite("extracted/bitxor.jpg", bitxor)
    bitnot = cv2.bitwise_not(bitxor)
    return img_vh, bitnot, img_bin


def get_table_cells(img, data_type):
    img_vh, img_gray, img_bit = get_vh_lines_img(img)
    contours, hierarchy = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    box = []
    i = 0
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if h < 500:
            image = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 200, 0), 4)
            if data_type == 'days':
                if w > 200 and h > 300:
                    box.append([x, y, w, h])
            elif data_type == 'hours':
                if 200 < w < 1000 and h > 120:
                    box.append([x, y, w, h])
            elif data_type == 'classes':
                box.append([x, y, w, h])
        i += 1
    if data_type == 'classes':
        return box[::-1], img_gray, img_bit
    else:
        return box[::-1]


def load_images_from_folder(path):
    img_color = cv2.imread(path)

    if img_color is not None:
        page_title = get_page_title(img_color)
        img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
        img_days = get_cropped_days_img(img)
        boxes_days = get_table_cells(img_days, 'days')

        img_hours = get_cropped_hours_img(img)
        boxes_hours = get_table_cells(img_hours, 'hours')

        img_classes = get_cropped_classes_img(img)
        # print_img(img_classes)
        img_classes_col = get_cropped_classes_img(img_color)
        boxes_classes, gray_classes, bit_classes = get_table_cells(img_classes, 'classes')

    else:
        raise NameError("No image found at path: ", path)

    return page_title, boxes_days, boxes_hours, boxes_classes, gray_classes, img_classes_col, bit_classes


def get_cell_string(cell_img, psm='psm-3'):
    if psm == 'psm-3':
        out = pytesseract.image_to_string(cell_img, config="--psm 3")
    else:
        out = pytesseract.image_to_string(cell_img, config="--psm 10")
    return out


class Ora:
    def __init__(self, zi, ora_inceput, ora_final, profesor, materie, sala, saptamana, grupa='', date=None):
        if date is None:
            date = []
        self.zi = zi
        self.ora_inceput = ora_inceput
        self.ora_final = ora_final
        self.profesor = profesor
        self.materie = materie
        self.sala = sala
        self.grupa = grupa
        self.saptamana = saptamana
        self.date = date

    def __str__(self):
        return "\nZi: " + str(self.zi) + "\nOra de incepere: " + str(self.ora_inceput) + "\nOra de final: " + str(
            self.ora_final) + "\nProfesor: " + str(self.profesor) + "\nMaterie: " + str(
            self.materie) + "\nSala: " + str(self.sala) + "\nSaptamana: " + str(
            self.saptamana) + "\nGrupa: " + str(self.grupa)

    def __iter__(self):
        yield self.zi
        yield self.ora_inceput
        yield self.ora_final
        yield self.profesor
        yield self.materie
        yield self.sala
        yield self.grupa
        yield self.saptamana

    def get_class_data(self):
        print(self.date)


def is_every_week_hour(day_cell_h, current_cell_height, grupa):
    # print('day_cell_h', day_cell_h, 'current_cell_height', current_cell_height, 'grupa', grupa)
    # eps = 5
    cell_third = day_cell_h / 3
    cell_half = day_cell_h / 2
    return ((cell_third - 2 * 5) < current_cell_height < (cell_third + 5)) or (
            current_cell_height + 5 >= day_cell_h) or (
                   (current_cell_height + 5 >= cell_half) and ('Gr' in grupa))


def is_once_even_week_hour(current_cell_y, day_cell_y, day_cell_h):
    # print('current_cell_y', current_cell_y, 'day_cell_y', day_cell_y, 'day_cell_h', day_cell_h)
    # eps = 5
    day_cell_half_height = int(day_cell_h / 2)
    return (current_cell_y + 5) >= day_cell_y + day_cell_half_height


def add_space_to_teacher(teacher_string):
    if 'indu' not in teacher_string:
        if sum(1 for c in teacher_string if c.isupper()) == 2:
            teacher_string = teacher_string[:-1] + " " + teacher_string[-1:]
        else:
            teacher_string = teacher_string[:-2] + " " + teacher_string[-2:]
    return teacher_string


def get_small_cell_values(grupa, img_classes_col, x, y, w, h):
    # left part
    cell_img = img_classes_col[y:y + h, x:x + int((1.9 * w) / 3)]
    # print_img(cell_img)

    left_part = get_cell_string(cell_img)
    left_part = [word for word in left_part.splitlines() if len(word) > 1]
    # print(left_part)

    # right part
    cell_img = img_classes_col[y:y + h, x + int((2.3 * w) / 3):x + w]
    right_part = get_cell_string(cell_img)

    if len(right_part) == 0:  # No classroom received
        right_part = get_cell_string(cell_img, psm="psm-10")
    right_part = [word for word in right_part.splitlines() if (len(word) >= 1) and (word != ' ')]

    # The second argument is the teacher name
    # Swapping needed for further processing
    if len(left_part) >= 2:
        filtered_left_part = [word for word in left_part[1].split() if (len(word) >= 1) and (word != ' ')]
    # print(filtered_left_part)

        if len(filtered_left_part) >= 2 and re.match(TEACHER_REGEX,
                                                     filtered_left_part[0] + filtered_left_part[1]) or (
                'indu' in left_part[1]):
            left_part[0], left_part[1] = left_part[1], left_part[0]

        elif (len(filtered_left_part) == 1 and re.match(TEACHER_REGEX_NO_SPACE, filtered_left_part[0])) or (
                'indu' in filtered_left_part[0]):
            left_part[1] = add_space_to_teacher(left_part[1])
            left_part[0], left_part[1] = left_part[1], left_part[0]
        # print(left_part)

    grupa = extract_group(grupa, right_part)
    if grupa == "none":
        grupa = extract_group(grupa, left_part)
        if grupa == "none" and left_part[-1][-1].isdigit():
            grupa = left_part[-1][-1]
            left_part[-1] = left_part[-1][:-1:]
    return left_part + right_part, grupa


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def extract_group(grupa, words):
    for idx, word in enumerate(words):
        idx_gr = word.lower().rfind('gr')
        idx_gr_2 = word.lower().rfind('g r')
        if idx_gr != -1 and has_numbers(word[idx_gr:]) and (len(word) - idx_gr) < 5:
            grupa = words[idx][idx_gr:]
            words[idx] = words[idx][:idx_gr]
            break
        elif idx_gr_2 != -1 and has_numbers(word[idx_gr_2:]):
            grupa = words[idx][idx_gr_2:]
            words[idx] = words[idx][:idx_gr_2]
            break
    return grupa


def extract_classes_data(page_path):
    print("started work on file from path:", page_path)
    page_title, days, hours, classes, img_classes_gray, img_classes_col, img_classes_bit = load_images_from_folder(
        page_path)
    hours_starting_x = [hour[0] for hour in hours]
    ore = []
    warnings = []
    # print(img_classes_col)
    for indx, cl in enumerate(classes):
        x, y, w, h = cl

        if x not in hours_starting_x:  # skipping wrong taken cells
            continue
        cell_img = img_classes_col[y:y + h, x:x + w]  # full size cell
        if np.mean(cell_img) <= 250:  # skipping white cells
            # print_img(cell_img)
            grupa = 'none'
            materie = ''
            sala = ''

            if h < 65:  # process cells that are  1/8  and 1/6 of full size
                filtered, grupa = get_small_cell_values(grupa, img_classes_col, x, y, w, h)
                extracted_data = (filtered + [grupa]).copy()
            else:
                out = get_cell_string(cell_img)
                words = out.splitlines()
                filtered = [word for word in words if (len(word) >= 1) and (word != ' ')]
                extracted_data = filtered.copy()
            # print("FILTERED", filtered)
            current_hour_idx = extract_starting_hour(hours, x)

            if len(filtered) <= 1:
                cell_img = img_classes_bit[y:y + h, x:x + w]
                out = get_cell_string(cell_img)
                words = out.splitlines()
                if len(words) < 2:
                    cell_img = img_classes_bit[y + int((2 * h) / 3):y + h, x + int((2.1 * w) / 3):x + w]
                    out = get_cell_string(cell_img, psm="psm-10")
                    words += out.splitlines()

                filtered = [word for word in words if (len(word) >= 1) and (word != ' ')]
            # print(filtered)
            if len(filtered) <= 1:
                warnings.append("Cell " + str(indx) + "Unsuccessful retry. ")
                ore.append(Ora(day_string[0], hour_string[current_hour_idx],
                               hour_string[current_hour_idx + round((w / 260))], 'none', 'none', 'none', 'none',
                               'none', extracted_data))
                continue

            # Case when cell has on the same row the teacher name and the group
            idx_gr = filtered[0].lower().rfind('gr')
            if idx_gr != -1 and has_numbers(filtered[0][idx_gr:]):
                grupa = filtered[0][idx_gr:]
                profesor = filtered[0][:idx_gr]
            else:
                profesor = filtered[0]
                idx_slash = profesor.find('/')
                if idx_slash != -1 and len(profesor[idx_slash + 1:].split()) != 2 and len(filtered[1]) < 3:
                    profesor = profesor + " " + filtered[1]
                    filtered[0] = profesor
                    filtered.pop(1)
            # Rare case of missreading 'Gr' as 'G r' or words splitted
            size_of_filtered = len(filtered)
            if size_of_filtered == 4:
                filtered[1] = filtered[1].replace('_', '').replace('|', 'I')
                if re.match(TEACHER_REGEX, filtered[1]) or re.match(TEACHER_REGEX_NO_SPACE, filtered[1]):
                    if '/' in filtered[0]:
                        filtered[0] += ' ' + filtered[1]
                    else:
                        filtered[0] += ' / ' + filtered[1]
                    filtered.pop(1)
                    profesor = filtered[0]
                else:
                    filtered[1] += filtered[2]
                    filtered.pop(2)
                size_of_filtered = len(filtered)

            # Extracted more words than anticipated.
            elif size_of_filtered > 4:
                # print("filtered before", filtered)
                new_w = ""
                while len(filtered) > 3:
                    if 'G' not in filtered[1]:
                        new_w += filtered[1]
                        filtered.pop(1)
                filtered[1] = new_w + filtered[1]
                size_of_filtered = len(filtered)

            if size_of_filtered == 3:
                materie = filtered[1]
                partitioning = [word for word in filtered[2].split() if (len(word) >= 1) and (word != ' ')]
                len_part = len(partitioning)
                if len_part >= 3:
                    if any(word in partitioning[0] for word in {'G', 'SE', 'CU', 'se'}):
                        grupa = ''.join(partitioning[:-1])
                        sala = partitioning[-1]
                elif len_part == 2 and ('G' in partitioning[0]):
                    grupa = partitioning[0]
                    sala = partitioning[1]
                elif len_part == 1:
                    if any(word in partitioning[0] for word in {'Gr', 'G r'}):
                        grupa = ''.join(partitioning)
                        sala = 'none'
                    else:
                        sala = ''.join(partitioning)
            elif size_of_filtered == 2:
                grupa = extract_group(grupa, filtered)
                swap_prof_materie = False
                if re.match(TEACHER_REGEX_NO_SPACE, filtered[0].replace('|', 'I')) and filtered[0].replace(' ',
                                                                                                           ''):
                    profesor = add_space_to_teacher(filtered[0].replace('|', 'I'))
                    # print("space needed", filtered)
                elif re.match(TEACHER_REGEX, filtered[0]) or ('indu' in filtered[0].replace('|', 'I')) or (
                        '/' in filtered[0]) and filtered[0].replace(' ', ''):
                    profesor = filtered[0].replace('|', 'I')
                    # print("No change, no space", filtered)
                else:
                    materie = filtered[0]
                    swap_prof_materie = True
                    # print("space not needed, change needed", filtered)
                if '[' in filtered[1] and ']' in filtered[1]:
                    idx_d = filtered[1].find(']')
                    materie = filtered[1][:idx_d + 1]
                    sala = filtered[1][idx_d + 1:]
                    # print(materie, sala)

                # Case of class at Magurele and no teacher is assigned
                elif 'Magurele' in filtered[1] and 'lab' in filtered[1]:
                    sala = filtered[1]
                    if profesor == materie:
                        profesor = 'none'
                else:
                    words = [word for word in filtered[1].split() if (len(word) >= 1) and (word != ' ')]
                    # print('materie', materie, 'profesor', profesor)
                    # classroom and class are read
                    if len(words) > 1:
                        # sala = words[-1]
                        for idx, word in enumerate(words):
                            if has_numbers(word):
                                sala = word
                                words.pop(idx)
                        aux_word = ''.join(words[:]).replace('|', 'I')
                        if swap_prof_materie and (
                                re.match(TEACHER_REGEX_NO_SPACE, aux_word) or re.match(TEACHER_REGEX, aux_word) or (
                                'BanuDem' in aux_word)):
                            profesor = add_space_to_teacher(aux_word)
                        else:
                            materie = aux_word
                    # classroom is not detected ( it is a single digit, so it needs psm-10 )
                    elif len(words) == 1:
                        cell_img = img_classes_col[y + int((2 * h) / 3):y + h, x + int((2.1 * w) / 3):x + w]
                        sala = get_cell_string(cell_img, "psm-10")
                        if swap_prof_materie and (
                                re.match(TEACHER_REGEX_NO_SPACE, words[0]) or re.match(TEACHER_REGEX, words[0])):
                            profesor = words[0]
                        else:
                            materie = words[0]
                    else:
                        warnings.append("No received data")

            # Case of 1/3 or 1/4 cells that dont have a group.
            # Isolating cell part of group.
            # print(grupa)
            grupa = grupa.replace('|', '1')
            temp = re.findall(r'\d+', grupa)
            res = list(map(int, temp))

            if 50 < h < 100 and len(res) == 0:
                cell_img = img_classes_gray[y:y + int(h / 2), x + int((2.4 * w) / 3):x + w]
                grupa = get_cell_string(cell_img)

            grupa, grupa_processed, sala = classroom_group_preprocessing(grupa, h, img_classes_gray, sala, w, x, y,
                                                                         warnings)
            # print(grupa, grupa_processed)
            temp = re.findall(r'\d+', profesor)
            res = list(map(int, temp))
            if profesor == '':
                warnings.append("ERROR:No teacher found")
                profesor = 'None'
            elif 'Fizica' in profesor.replace(' ', '') and materie == '':
                materie = profesor
                profesor = 'None'
            # calculate day
            current_day = int(y / (days[-1][1] - days[-2][1]))
            # Calculating if hour its weekly or once a odd/even week
            _, day_cell_y, _, day_cell_h = days[current_day]
            saptamana = get_week_type(day_cell_h, day_cell_y, grupa, h, y)

            grupa = grupa_processed
            profesor = profesor.replace('|', 'I').replace('.', '').replace('-', '').replace('_', '')
            materie = materie.replace('|', 'I').replace(' ', '')
            grupa = ''.join([i if ord(i) < 128 else '' for i in grupa])
            materie = ''.join([i if ord(i) < 128 else '' for i in materie])
            profesor = ''.join([i if ord(i) < 128 else '' for i in profesor])
            if 'gulici' in profesor:
                profesor = "Dragulici D"
            elif 'indust' in profesor:
                profesor = "Industrie"
            ore.append(Ora(day_string[current_day], hour_string[current_hour_idx],
                           hour_string[current_hour_idx + round((w / 260))], profesor, materie, sala, saptamana,
                           grupa, extracted_data))
            # print(ore[-1])
    return Pagina(page_title, warnings, ore)


def get_week_type(day_cell_h, day_cell_y, grupa, h, y):
    if is_every_week_hour(day_cell_h, h, grupa):  # 1/2 cell that happens in every week
        saptamana = "Impar / Par"
    elif is_once_even_week_hour(y, day_cell_y, day_cell_h):
        saptamana = "Par"
    else:
        saptamana = "Impar"
    return saptamana


def classroom_group_preprocessing(grupa, h, img_classes_gray, sala, w, x, y, warnings):
    cell_img = img_classes_gray[y + int((2 * h) / 3):y + h, x + int((2.1 * w) / 3):x + w]
    if sala == '':
        # cell_img = img_classes_gray[y + int((1.8 * h) / 3):y + h, x + int((2.1 * w) / 3):x + w]
        # print_img(cell_img)
        sala = get_cell_string(cell_img, psm="psm-10")
    sala = sala.replace('|', '1').replace('.', '-').replace(' ', '')
    if any(x in sala for x in ['Ha', 'ret']):
        sala = "Amf. Haret (Et. 0)"
    elif any(x in sala for x in ['St', 'low']):
        sala = "Amf. Stoilow (Et. 1)"
    elif any(x in sala for x in ['Po', 'peiu']):
        sala = "Amf. Pompeiu (Et. 2)"
    elif any(x in sala for x in ['Ti', 'eica']):
        sala = "Amf. Titeica (Et. 3)"
    elif any(x in sala for x in ['Chim', 'imie']):
        sala = "Amf. R1 (Et. 1, Fac. Chimie)"
    elif any(x in sala for x in ['goo', 'gle']):
        sala = "214 Google"
    elif sala == 'O':
        sala = "Sala " + '9'
    elif sala == 'Z' or sala == 'S':
        sala = "Sala " + '2'
    elif any(x in sala for x in ['V2', 'W']):
        sala = "Sala " + '12'
    elif any(x in sala for x in ['zie', 'Zag', 'Ze']):
        sala = "Sala " + '219'
    elif any(x in sala for x in ['Mag', 'Fiz', 'ica','urele', 'lab']):
        if 'lab' in sala:
            sala = 'laborator Magurele'
        else:
            sala = "Fac.Fizica -Magurele"
    elif not has_numbers(sala):
        sala = "Sala " + get_cell_string(cell_img, psm="psm-3")
        # if not has_numbers(sala) or sala == '':
            # Commented because there is a pandemic atm
            # warnings.append("WARN: No Classroom extracted")
    else:
        sala = "Sala " + sala

    temp = re.findall(r'\d+', grupa)1
    res = list(map(int, temp))

    if len(res):
        if res[0] < 10:
            grupa_processed = 'Grupa:'
        else:
            grupa_processed = 'Serii:'
        for number in res:
            if number < 10:
                grupa_processed += str(number)
            else:
                grupa_processed += str(number) + ' '
    else:
        grupa_processed = 'none'
        if h < 100:
            warnings.append("WARN: Possible group required")

    return grupa, grupa_processed, sala


def extract_starting_hour(hours, x):
    # Extracting the hour of the class
    current_hour_idx = 0
    for index, hour in enumerate(hours):
        if hour[0] == x:
            current_hour_idx = index
            break
    return current_hour_idx


class Pagina:
    def __init__(self, titlu, warnings, ore):
        self.titlu = titlu.replace('|', '1')
        self.warnings = warnings
        self.ore = ore

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          indent=4)


def get_pages(img_folder_path):
    pages = extract_pages_data(img_folder_path)
    return pages


def write_pages_to_json_file(img_folder_path):
    pages = extract_pages_data(img_folder_path)
    dt_string = datetime.datetime.now().strftime("_%d_%m_%Y_%H_%M_%S")
    with open('extracted/JSON/page_to_json' + dt_string + '.json', 'w') as outfile:
        outfile.write(json.dumps(pages, default=Pagina.to_json))
        # json.loads


def extract_pages_data(img_folder_path):
    start = time.time()
    folder = os.path.dirname(os.path.abspath(img_folder_path))
    paths = []
    for filename in os.listdir(folder):
        paths.append(os.path.join(folder, filename))
    num_cores = multiprocessing.cpu_count()
    pages = Parallel(n_jobs=4, backend='multiprocessing')(
        delayed(extract_classes_data)(path) for path in paths)
    print(time.time() - start)
    return pages
