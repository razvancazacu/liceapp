import unittest

from scripts.orar_ocr import *


class TestPageReading(unittest.TestCase):
    maxDiff = None

    # def test_page0_dpi400to300(self):
    #     test_dir_path = 'resources_img/'
    #     start = time.time()
    #
    #     page1 = extract_classes_data(test_dir_path + '300dpi.jpg')
    #     flag2 = time.time() - start
    #     print(flag2)
    #     start = time.time()
    #     page1 = extract_classes_data(test_dir_path + '400dpi.jpg')
    #     flag2 = time.time() - start
    #     print(flag2)
    #     page2 = extract_classes_data(test_dir_path + '500dpi.jpg')
    #     flag = time.time() - start
    #     print(flag)
    #     start = time.time()

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

    def test_page80_4groups(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_80.jpg')
        with open('resources_json/out_80.json', 'r') as test_file:
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

    def test_sem2_class_401(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem2_401.jpg')
        with open('resources_json/out_sem2_401.json', 'r') as test_file:
            # test_file.write(page.to_json())
            json_string = test_file.read()
            self.assertEqual(json_string, page.to_json())

    def test_sem2_class_402(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem2_402.jpg')
        with open('resources_json/out_sem2_402.json', 'r') as test_file:
            # test_file.write(page.to_json())
            json_string = test_file.read()
            self.assertEqual(json_string, page.to_json())

    def test_sem2_class_405(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem2_405.jpg')
        with open('resources_json/out_sem2_405.json', 'r') as test_file:
            # test_file.write(page.to_json())
            json_string = test_file.read()
            self.assertEqual(json_string, page.to_json())

    # TODO
    def test_sem2_class_406(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem2_406.jpg')
        # with open('resources_json/out_sem2_75.json', 'r') as test_file:
        #     # test_file.write(page.to_json())
        #     json_string = test_file.read()
        #     self.assertEqual(json_string, page.to_json())

    # TODO
    def test_sem2_class_507(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem2_507.jpg')
        # with open('resources_json/out_sem2_75.json', 'r') as test_file:
        #     # test_file.write(page.to_json())
        #     json_string = test_file.read()
        #     self.assertEqual(json_string, page.to_json())


if __name__ == '__main__':
    unittest.main()
