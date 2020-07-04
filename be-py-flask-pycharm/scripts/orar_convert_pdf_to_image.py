import os
import shutil

from pdf2image import convert_from_path


def convert_pdf_to_images(pdf_name):
    print("Deleting old Images")
    folder = 'resources/Images'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    print("Starting PDF to JPEG Conversion")
    convert_from_path('resources/' + pdf_name,
                      thread_count=4,
                      dpi=300,
                      output_folder='resources/Images',
                      fmt="jpeg")
    print("Ended PDF to JPEG Conversion")
