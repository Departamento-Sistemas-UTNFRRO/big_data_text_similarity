import csv
import os
from utils import general_utils as gu


def write_csv_file(file_path, element_list):
    with open(file_path, 'w') as csv_file:
        for element in element_list:
            writer = csv.writer(csv_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(element)


def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        gu.print_screen('Directory created: ' + dir_path)
