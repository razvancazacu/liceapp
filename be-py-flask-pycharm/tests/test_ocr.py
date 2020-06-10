import sys
from scripts.orar_ocr import *
import unittest


class TestPageReading(unittest.TestCase):

    def test_page16(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_16.jpg')
        with open('resources_json/out_16.json', 'r') as test_file:
            # test_file.write(page.to_json())
            json_string = test_file.read()
            self.assertEqual(json_string, page.to_json())

    def test_page20_large_text(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_20.jpg')
        with open('resources_json/out_20.json', 'r') as test_file:
            # test_file.write(page.to_json())
            json_string = test_file.read()
            self.assertEqual(json_string, page.to_json())

    def test_page64_no_teacher(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_64.jpg')
        with open('resources_json/out_64.json', 'r') as test_file:
            # test_file.write(page.to_json())
            json_string = test_file.read()
            self.assertEqual(json_string, page.to_json())

    def test_page85_overlapped(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_85.jpg')
        with open('resources_json/out_85.json', 'r') as test_file:
            # test_file.write(page.to_json())
            json_string = test_file.read()
            self.assertEqual(json_string, page.to_json())


if __name__ == '__main__':
    unittest.main()