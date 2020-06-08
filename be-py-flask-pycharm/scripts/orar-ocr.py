import cv2
import numpy as np
import pytesseract
import os
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def print_img(img):
    cv2.imshow('img', img)
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
    thresh, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    img_bin = 255 - img_bin
    return img_bin


def get_vh_lines_img(img):
    #     countcol(width) of kernel as 100th of total width
    kernel_len = np.array(img).shape[1] // 100
    #     Defining a vertical kernel to detect all vertical lines of image
    ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
    #     Defining a horizontal kernel to detect all horizontal lines of image
    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
    #     A kernel of 2x2
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    img_bin = get_binnary_img(img)
    #     Use vertical kernel to detect and save the vertical lines in a jpg
    image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
    vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)
    cv2.imwrite("../poze-orar/out_0_vertical.jpg", vertical_lines)
    #     Use horizontal kernel to detect and save the horizontal lines in a jpg
    image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
    horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)
    cv2.imwrite("../poze-orar/out_0_horizontal.jpg", horizontal_lines)
    #     Combine horizontal and vertical lines in a new third image, with both having same weight.
    img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 1, 0.0)
    #     Eroding and thesholding the image

    img_vh = cv2.erode(~img_vh, kernel, iterations=2)
    thresh, img_vh = cv2.threshold(img_vh, 128, 255, cv2.THRESH_BINARY)

    cv2.imwrite("../poze-orar/out_0_img_vh.jpg", img_vh)
    bitxor = cv2.bitwise_xor(img, img_vh)
    bitnot = cv2.bitwise_not(bitxor)

    return img_vh, bitnot


def get_table_cells(img, data_type):
    img_vh, bitnot = get_vh_lines_img(img)
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
        return box[::-1], bitnot
    else:
        return box[::-1]


def load_images_from_folder(path):
    img_color = cv2.imread(path)
    page_title = get_page_title(img_color)
    img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    img_days = get_cropped_days_img(img)
    boxes_days = get_table_cells(img_days, 'days')

    img_hours = get_cropped_hours_img(img)
    boxes_hours = get_table_cells(img_hours, 'hours')

    img_classes = get_cropped_classes_img(img)
    img_classes_col = get_cropped_classes_img(img_color)
    boxes_classes, bitnot_classes = get_table_cells(img_classes, 'classes')

    return page_title, boxes_days, boxes_hours, boxes_classes, bitnot_classes, img_classes_col


def Sort(sub_li):
    return sorted(sub_li, key=lambda x: x[0])


def print_page_data(days, hours, classes):
    print('---------------------------------Rows')
    print('Luni:      ', days[0])
    print('Marti:     ', days[1])
    print('Miercuri:  ', days[2])
    print('Joi:       ', days[3])
    print('Vineri:    ', days[4])
    print('------------------------------Columns')
    print('8:  ', hours[0])
    print('9:  ', hours[1])
    print('10: ', hours[2])
    print('11: ', hours[3])
    print('12: ', hours[4])
    print('13: ', hours[5])
    print('14: ', hours[6])
    print('15: ', hours[7])
    print('16: ', hours[8])
    print('17: ', hours[9])
    print('18: ', hours[10])
    print('19: ', hours[11])
    print('------------------------------Cells')

    for index, cl in enumerate(classes):
        if cl[0] == 0:
            print('new Day')
        print(index, cl)


def get_cell_string(cell_img, psm='psm-3'):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
    border = cv2.copyMakeBorder(cell_img, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=[255, 255])
    resizing = cv2.resize(border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    dilation = cv2.dilate(resizing, kernel, iterations=1)
    erosion = cv2.erode(dilation, kernel, iterations=2)
    if psm == 'psm-3':
        out = pytesseract.image_to_string(cell_img, config="--psm 3")
    elif psm == 'psm-10':
        out = pytesseract.image_to_string(cell_img, config="--psm 10")

    return out


class Ora:
    def __init__(self, zi, ora_inceput, ora_final, profesor, materie, sala, saptamana, warnings, grupa='', date=''):
        self.zi = zi
        self.ora_inceput = ora_inceput
        self.ora_final = ora_final
        self.date = date
        self.profesor = profesor
        self.materie = materie
        self.sala = sala
        self.grupa = grupa
        self.warnings = warnings
        if len(grupa) == 0 or grupa == 'none':
            self.saptamana = "Impar / Par"
        else:
            self.saptamana = saptamana

    def __str__(self):
        return "\nZi: " + str(self.zi) + "\nOra de incepere: " + str(self.ora_inceput) + "\nOra de final: " + str(
            self.ora_final) + "\nProfesor: " + str(self.profesor) + "\nMaterie: " + str(
            self.materie) + "\nSala: " + str(self.sala) + "\nSaptamana: " + str(
            self.saptamana) + "\nGrupa: " + str(self.grupa)

    def get_class_data(self):
        print(self.date)


def get_small_cell_values(grupa, filtered, img_classes_col, x, y, w, h, warnings):
    cell_img = img_classes_col[y:y + h, x:x + int((2 * w) / 3)]
    left_part = get_cell_string(cell_img)
    left_part = left_part.splitlines()
    filtered_part = [word for word in left_part if len(word) > 4]
    left_part = filtered_part
    cell_img = img_classes_col[y:y + h, x + int((2.1 * w) / 3):x + w]
    right_part = get_cell_string(cell_img)
    if len(right_part) == 0:
        right_part = get_cell_string(cell_img, psm="psm-10")
    right_part = right_part.splitlines()
    filtered_part = [word for word in right_part if (len(word) >= 1) and (word != ' ')]
    right_part = filtered_part
    idx_gr = left_part[1].find('Gr')
    idx_gr_2 = left_part[1].find('G r')
    if idx_gr != -1:
        grupa = left_part[1][idx_gr:]
        left_part[1] = left_part[1][:idx_gr]
    elif idx_gr_2 != -1:
        grupa = left_part[1][idx_gr_2:]
        left_part[1] = left_part[1][:idx_gr_2]
    if grupa == 'none':
        warnings.append("Possible group required for this cell")
    filtered = left_part + right_part


def extract_classes_data(page_path):
    print(page_path)
    ore = []
    page_title, days, hours, classes, img_classes_bit, img_classes_col = load_images_from_folder(page_path)
    hours_starting_x = [hour[0] for hour in hours]

    warnings = []
    for indx, cl in enumerate(classes):
        x, y, w, h = cl
        if x not in hours_starting_x:  # skipping wrong taken cells
            continue
        cell_img = img_classes_col[y:y + h, x:x + w]  # full size cell
        # print_img(cell_img)
        if np.mean(cell_img) <= 250:  # skipping white cells
            # print_img(cell_img)

            grupa = 'none'
            materie = ''
            sala = ''
            filtered = []
            if h < 65:  # for 1/8 cells and 1/6
                get_small_cell_values(grupa, filtered, img_classes_col, x, y, w, h, warnings)
            else:
                out = get_cell_string(cell_img)
                words = out.splitlines()
                filtered = [word for word in words if (len(word) >= 1) and (word != ' ')]
            if len(filtered):

                # calculate day
                current_day = int(y / (days[-1][1] - days[-2][1]))

                # Calculating if hour its weekly or once a odd/even week
                _, day_cell_y, _, day_cell_h = days[current_day]
                eps = 5
                if (y + eps) >= day_cell_y + int(day_cell_h / 2):
                    saptamana = "Par"
                elif ((day_cell_h / 3) - 2 * eps) < h < ((day_cell_h / 3) + eps):  # treime ( 3 grupe saptamanal)
                    saptamana = "Impar / Par"
                else:
                    saptamana = "Impar"

                # Extracting the hour of the class
                current_hour_idx = 0
                for index, hour in enumerate(hours):
                    if hour[0] == x:
                        current_hour_idx = index
                        break

                if len(filtered) == 1:
                    warnings.append(
                        "Cell" + str(indx) + "First run received only one data. Retrying with greyscale image and "
                                             "isolating parts")
                    cell_img = img_classes_bit[y:y + h, x:x + w]
                    out = get_cell_string(cell_img)
                    words = out.splitlines()
                    cell_img = img_classes_bit[y + int((2 * h) / 3):y + h, x + int((2.1 * w) / 3):x + w]
                    out = get_cell_string(cell_img, psm="psm-10")
                    words += out.splitlines()
                    filtered = [word for word in words if (len(word) >= 1) and (word != ' ')]

                if len(filtered) <= 1:
                    warnings.append("Cell" + str(indx) + "Unsuccessful retry. ")
                    ore.append(Ora(day_string[current_day], hour_string[current_hour_idx],
                                   hour_string[current_hour_idx + round((w / 260))], 'none', 'none', 'none', 'none',
                                   'none', 'none',
                                   filtered))
                    continue

                # Case when cell has on the same row the teacher name and the group
                gr_idx = filtered[0].find('Gr')
                if gr_idx != -1:
                    grupa = filtered[0][gr_idx:]
                    profesor = filtered[0][:gr_idx]
                else:
                    profesor = filtered[0]

                # Rare case of missreading 'Gr' as 'G r'
                if len(filtered) == 4:
                    filtered[1] += filtered[2]  # posibila inlocuire : read until no number meet Gr__4
                    filtered.pop(2)

                if len(filtered) == 2:
                    gr_in_first = filtered[0].find('Gr')
                    gr_in_first_2 = filtered[0].find('G r')
                    if gr_in_first != -1:
                        grupa = filtered[0][gr_in_first:]
                        filtered[0] = filtered[0].replace(grupa, '')
                    elif gr_in_first_2 != -1:
                        grupa = filtered[0][gr_in_first_2:]
                        filtered[0] = filtered[0].replace(grupa, '')
                    profesor = filtered[0]
                    words = [word for word in filtered[1].split() if (len(word) >= 1) and (word != ' ')]

                    # classroom and class are read
                    if len(words) > 1:
                        sala = words[-1]
                        materie = ''.join(words[:-1])
                    # classroom is not detected ( it is a single digit, so it needs psm-10 )
                    elif len(words) == 1:
                        cell_img = img_classes_col[y + int((2 * h) / 3):y + h, x + int((2.1 * w) / 3):x + w]
                        sala = get_cell_string(cell_img, "psm-10")
                        materie = words[0]
                    else:
                        warnings.append("No received data")
                elif len(filtered) == 3:

                    materie = filtered[1]
                    partitioning = [word for word in filtered[2].split() if (len(word) >= 1) and (word != ' ')]
                    # print(partitioning)

                    if len(partitioning) == 3:
                        grupa = partitioning[0] + partitioning[1]
                        sala = partitioning[2]
                    elif len(partitioning) == 2:
                        grupa = partitioning[0]
                        sala = partitioning[1]
                    else:
                        sala = partitioning[0]
                if sala == '':
                    cell_img = img_classes_bit[y + int((2 * h) / 3):y + h, x + int((2.1 * w) / 3):x + w]
                    sala = get_cell_string(cell_img, psm="psm-10")

                if sala.find("Har") != -1:
                    sala = "Amf. Hater (Et. 0)"
                elif sala.find("Sto") != -1:
                    sala = "Amf. Stoilow (Et. 1)"
                elif sala.find("Pom") != -1:
                    sala = "Amf. Pompeiu (Et. 2)"
                elif sala.find("Tit") != -1:
                    sala = "Amf. Titeica (Et. 3)"
                elif sala.find("Chim") != -1:
                    sala = "Amf. R1 (Et. 1, Fac. Chimie)"
                    grupa = "none"
                elif sala == 'O':
                    sala = "Sala " + '0'
                else:
                    sala = "Sala " + sala

                grupa = grupa.replace(" ", "").replace("_", "").replace(")", "")
                profesor = profesor.replace('|', 'I')
                materie = materie.replace('|', 'l')
                grupa = ''.join([i if ord(i) < 128 else '' for i in grupa])
                materie = ''.join([i if ord(i) < 128 else '' for i in materie])
                profesor = ''.join([i if ord(i) < 128 else '' for i in profesor])
                ore.append(Ora(day_string[current_day], hour_string[current_hour_idx],
                               hour_string[current_hour_idx + round((w / 260))], profesor, materie, sala, saptamana,
                               warnings, grupa,
                               filtered))
    return Pagina(page_title, ore)


class Pagina:
    def __init__(self, titlu, ore):
        self.titlu = titlu
        self.ore = ore


day_string = ["Luni", "Marti", "Miercuri", "Joi", "Vineri"]
hour_string = ["8:00",
               "9:00",
               "10:00",
               "11:00",
               "12:00",
               "13:00",
               "14:00",
               "15:00",
               "16:00",
               "17:00",
               "18:00",
               "19:00",
               "20:00"]

from joblib import Parallel, delayed
import multiprocessing

num_cores = multiprocessing.cpu_count()
if __name__ == '__main__':
    start = time.time()
    # with open('page.txt', 'w') as outfile:
    #     folder = os.path.dirname(os.path.abspath('../tmp/300dpi/pages'))
    #     for filename in os.listdir(folder):
    #         path = os.path.join(folder, filename)
    #         outfile.write(str(filename) + '---------------------------------' + '\n')
    #         ore = extract_classes_data(path)
    #         for o in ore:
    #             outfile.write(str(o) + '\n')
    with open('page.txt', 'w') as outfile:
        folder = os.path.dirname(os.path.abspath('../tmp/300dpi/pages'))
        paths = []
        for filename in os.listdir(folder):
            paths.append(os.path.join(folder, filename))
        # print(paths)
        pagini = Parallel(n_jobs=num_cores, backend='multiprocessing')(
            delayed(extract_classes_data)(path) for path in paths[:10])
        print(pagini)
        print('--------------------')
        for pag in pagini:
            outfile.write(str(pag.titlu) + '\n')
            for ora in pag.ore:
                outfile.write(str(ora) + '\n')

    print(time.time() - start)

# # Testing
# ore = extract_classes_data(
#     'C:\\Users\\cmrra\\Documents\\Licenta-Project\\liceapp\\be-py-flask-pycharm\\tmp\\300dpi\\out_52.jpg')
# for o in ore:
#     print(o)

# print_page_data(days, hours, classes)
# # optime < 50 h
# # patrime >65 <100
# # sesime >55 <65..
# # jumatati aprox 190
# # luni-vineri heigh = aprox(380).
