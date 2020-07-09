import unittest

from scripts.orar_ocr import *


class TestPageReading(unittest.TestCase):
    maxDiff = None

    def test_page16(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_16.jpg')
        with open('resources_json/out_16.json', 'w') as test_file:
            test_file.write(page.to_json())
            # json_string = test_file.read()
            # self.assertEqual(json_string, page.to_json())

    def test_page20_large_text(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_20.jpg')
        with open('resources_json/out_20.json', 'w') as test_file:
            test_file.write(page.to_json())
            # json_string = test_file.read()
            # self.assertEqual(json_string, page.to_json())

    def test_page64_no_teacher(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_64.jpg')
        with open('resources_json/out_64.json', 'w') as test_file:
            test_file.write(page.to_json())
            # json_string = test_file.read()
            # self.assertEqual(json_string, page.to_json())

    def test_page80_4groups(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_80.jpg')
        with open('resources_json/out_80.json', 'w') as test_file:
            test_file.write(page.to_json())
            # json_string = test_file.read()
            # self.assertEqual(json_string, page.to_json())

    def test_sem1_class_401(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem1_401.jpg')
        with open('resources_json/out_sem1_401.json', 'w') as test_file:
            test_file.write(page.to_json())
            # json_string = test_file.read()
            # self.assertEqual(json_string, page.to_json())

    def test_sem1_class_402(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem1_402.jpg')
        with open('resources_json/out_sem1_402.json', 'w') as test_file:
            test_file.write(page.to_json())
            # json_string = test_file.read()
            # self.assertEqual(json_string, page.to_json())

    def test_sem1_class_405(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem1_405.jpg')
        with open('resources_json/out_sem1_405.json', 'w') as test_file:
            test_file.write(page.to_json())
            # json_string = test_file.read()
            # self.assertEqual(json_string, page.to_json())

    def test_sem2_class_231(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem2_231.jpg')
        with open('resources_json/out_sem2_231.json', 'w') as test_file:
            test_file.write(page.to_json())
            # json_string = test_file.read()
            # self.assertEqual(json_string, page.to_json())

    def test_sem2_class_235(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem2_235.jpg')
        with open('resources_json/out_sem2_235.json', 'w') as test_file:
            test_file.write(page.to_json())
            # json_string = test_file.read()
            # self.assertEqual(json_string, page.to_json())

    def test_sem2_class_406(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem2_406.jpg')
        with open('resources_json/out_sem2_406.json', 'w') as test_file:
            test_file.write(page.to_json())
            # json_string = test_file.read()
            # self.assertEqual(json_string, page.to_json())

    def test_sem2_class_321(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem2_321.jpg')
        with open('resources_json/out_sem2_321.json', 'w') as test_file:
            test_file.write(page.to_json())
            # json_string = test_file.read()
            # self.assertEqual(json_string, page.to_json())

    def test_sem2_class_332(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem2_332.jpg')
        with open('resources_json/out_sem2_332.json', 'w') as test_file:
            test_file.write(page.to_json())
            # json_string = test_file.read()
            # self.assertEqual(json_string, page.to_json())

    def test_sem2_class_452(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem2_452.jpg')
        with open('resources_json/out_sem2_452.json', 'w') as test_file:
            test_file.write(page.to_json())
            # json_string = test_file.read()
            # self.assertEqual(json_string, page.to_json())

    def test_sem2_class_505(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem2_505.jpg')
        with open('resources_json/out_sem2_505.json', 'w') as test_file:
            test_file.write(page.to_json())
            # json_string = test_file.read()
            # self.assertEqual(json_string, page.to_json())

    def test_sem1_class_507(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem1_507.jpg')
        with open('resources_json/out_sem1_507.json', 'w') as test_file:
            test_file.write(page.to_json())
            # json_string = test_file.read()
            # self.assertEqual(json_string, page.to_json())

    def test_sem2_class_507(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem2_507.jpg')
        with open('resources_json/out_sem2_75.json', 'w') as test_file:
            test_file.write(page.to_json())
        #     json_string = test_file.read()
        #     self.assertEqual(json_string, page.to_json())

    def test_sem2_optional_info3(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem2_opinfoan3.jpg')
        with open('resources_json/out_sem2_opinfoan3.json', 'w') as test_file:
            test_file.write(page.to_json())
            # json_string = test_file.read()
            # self.assertEqual(json_string, page.to_json())

    def test_sem2_tutoriat_mate(self):
        test_dir_path = 'resources_img/'
        page = extract_classes_data(test_dir_path + 'out_sem2_tutoriat_mate.jpg')
        with open('resources_json/out_sem2_tutoriat_mate.json', 'w') as test_file:
            test_file.write(page.to_json())
            # json_string = test_file.read()
            # self.assertEqual(json_string, page.to_json())


if __name__ == '__main__':
    unittest.main()
