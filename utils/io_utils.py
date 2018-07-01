import csv
import os
import glob
import logging


def create_date_path(base_path, run_time):
    create_directory(base_path)
    date_path = os.path.join(base_path, '{:%Y%m%d_%H%M%S}'.format(run_time))
    create_directory(date_path)

    return date_path


def read_quora_csv_file(quora_file_path):
    logging.info('Loading Quora questions file...')

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
        logging.info('Directory created: ' + dir_path)


# Temporary, ugly, function to get a sample file.
def read_sample_file(base_path, sample_size, run_number):
    sample_questions = []

    file_path = base_path + '/question_pairs_subset_' + str(sample_size) + '_' + str(run_number) + '.csv'

    with open(file_path, 'r') as questions_file:
        reader = csv.reader(questions_file)
        for i, row in enumerate(reader):
            sample_questions.append(row)

    return sample_questions


# Temporary, ugly, function to get a distance file.
def read_distances_file(base_path, technique, run_number):
    distances = []

    file_name = base_path + '/computeDistance_' + technique + '_' + str(run_number) + '_*.csv'  # I don't mind the date.
    for filename in glob.glob(file_name):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # This has header, skipping it
            for i, row in enumerate(reader):
                distances.append(row)

    return distances
