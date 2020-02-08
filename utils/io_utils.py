import csv
import os
import glob
from datetime import datetime
from utils import general_utils as gu
from shutil import copyfile


def copy_pair_file_to_experiment_folder(input_file, dest_path):
    pairs_path = dest_path + '/pairs'
    create_directory(pairs_path)
    copyfile(input_file, os.path.join(pairs_path, os.path.basename(input_file)))


def get_or_create_experiment_path(results_path, sample_size, samples_number, k, clustering_runs, in_progress_experiment_path):
    if in_progress_experiment_path:
        experiment_path = results_path + '/' + in_progress_experiment_path
    else:
        experiment_path = build_experiment_path(results_path, sample_size, samples_number, k, clustering_runs)
        create_directory(experiment_path)

    return experiment_path


def get_current_result_path(experiment_path, sample_size, run):
    final_path = experiment_path + '/' + str(sample_size) + '_' + str(run)
    create_directory(final_path + '/distances')

    gu.print_screen('Results are going to be save in: ' + final_path)
    return final_path


def get_number_of_files_in_dir(directory):
    return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])


def build_samples_folder(samples_folder, technique, sample_size, number_of_samples):
    return samples_folder + "/" + technique + "/" + str(sample_size) + "_" + str(number_of_samples)


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
        os.makedirs(dir_path)
        gu.print_screen('Directory created: ' + dir_path)


def read_csv_file(path):
    data_set = []

    with open(path, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            data_set.append(row)

    return data_set


def build_question_path(base_path, sample_size, run_number):
    return os.path.join(base_path, 'question_pairs_subset_' + str(sample_size) + '_' + str(run_number) + '.csv')


def build_experiment_path(results_path, sample_size, samples_number, k, clustering_runs):
    size_string = 'samples_size_' + str(sample_size)
    sample_string = '_count_' + str(samples_number)
    clustering_string = '_k_' + str(k)
    clustering_runs_string = '_runs_' + str(clustering_runs)
    timestamp = '_' + datetime.now().strftime("%Y%m%d%H%M")

    return os.path.join(results_path, size_string + sample_string + clustering_string + clustering_runs_string + timestamp)


def read_sample_file(base_path, sample_size, run_number):
    sample_questions = []

    file_path = build_question_path(base_path, sample_size, run_number)

    with open(file_path, 'r') as questions_file:
        reader = csv.reader(questions_file)
        for i, row in enumerate(reader):
            sample_questions.append(row)

    return sample_questions


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
