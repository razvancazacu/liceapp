import threading
import time
from multiprocessing import Process
from os import listdir, getcwd
from os.path import isfile, join, abspath

import flask_server
from scripts.orar_convert_pdf_to_image import convert_pdf_to_images
from scripts.orar_download import get_fmi_pdf
from scripts.pages_db import extract_pages


class MainControl:

    def __init__(self, current_pdf='', pdf_option='latest', host='127.0.0.1', port='5002'):
        self.host = host
        self.port = port
        self.current_pdf = current_pdf
        self.pdf_option = pdf_option
        self.server_process = Process(target=flask_server.main, args=(self.host, self.port))
        self.server_status = "Offline"
        self.thread_time_sleep = threading.Timer(3.0, self.auto_extract_on_timer)
        self.start_time = time.time()

    @property
    def current_pdf(self):
        return self.__current_pdf

    @current_pdf.setter
    def current_pdf(self, value):
        self.__current_pdf = value

    @property
    def pdf_option(self):
        return self.__pdf_option

    @pdf_option.setter
    def pdf_option(self, value):
        self.__pdf_option = value

    def download_pdf(self):
        print("Started download for the", self.pdf_option, "schedule")
        self.current_pdf = get_fmi_pdf(self.pdf_option)
        print("Downloaded", self.current_pdf)

    def convert_pdf_to_img(self):
        if self.current_pdf:
            convert_pdf_to_images(self.current_pdf)
        else:
            print("No PDF selected")

    def start_server(self):
        if not self.server_process.is_alive():
            self.server_process.start()
            self.server_status = "Online"
        else:
            print("!! Server Already Online !!")

    def get_local_pdfs(self):
        resources_path = abspath(getcwd()) + '/resources'
        onlyfiles = [f for f in listdir(resources_path) if isfile(join(resources_path, f))]
        if len(onlyfiles):
            return onlyfiles
        return "-"

    def close_server(self):
        if self.server_process.is_alive():
            self.server_process.terminate()
            self.server_process.join()
            print("Server Closed")
        else:
            print("Server Offline")

    def extract_data(self):
        print("Started Data Extraction From Pages")
        path = 'resources/Images/'
        if len(listdir(path)) == 0:
            print("No files found in the images directory.")
        else:
            path += 'Pages'
            extract_pages(path)
        print("Ended Data Extraction")

    def auto_start(self):
        print("Started server, download, convert and data extraction")
        self.start_server()
        self.download_pdf()
        self.convert_pdf_to_img()
        self.extract_data()

    def auto_extract_on_timer(self):
        self.download_pdf()
        self.convert_pdf_to_img()
        self.extract_data()

    def auto_extract_on_timer_sleeper(self):
        if not self.thread_time_sleep.is_alive():
            print("Starting automatic extraction from 5 to 5 hours ( 300 minutes )")
            self.thread_time_sleep = threading.Timer(18000.0, self.auto_extract_on_timer)
            self.start_time = time.time()
            self.thread_time_sleep.start()
        else:
            print("Timer already set.",
                  "Next data extraction: %s minutes" % ((18000.0 - (time.time() - self.start_time)) / 60))

    def stop_extraction_on_interval(self):
        if self.thread_time_sleep.is_alive():
            print("Stopping automatic data extraction")
            self.thread_time_sleep.cancel()
            print("Time remained until next data extraction: %s minutes" % (
                    (18000.0 - (time.time() - self.start_time)) / 60))
        else:
            print("Automatic data extraction already offline")
