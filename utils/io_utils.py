import csv
import os
from utils import general_utils as gu


def read_quora_csv_file(quora_file_path):
    gu.print_screen('Loading Quora questions file...')

    all_questions = []

    with open(quora_file_path, 'r') as questions_file:
        reader = csv.reader(questions_file)
        next(reader)
        for i, row in enumerate(reader):
            all_questions.append(row)

    return all_questions


def write_csv_quora_sample(file_path, element_list):
    with open(file_path, 'w') as csv_file:
        writer = csv.writer(csv_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for element in element_list:
            writer.writerow(element)


def create_directory(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        gu.print_screen('Directory created: ' + dir_path)
