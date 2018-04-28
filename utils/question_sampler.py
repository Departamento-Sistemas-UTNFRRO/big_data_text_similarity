import os
import random
from utils import general_utils as gu
from utils import io_utils

COL_QUESTION_ID = 0
COL_QUESTION_1 = 1
COL_QUESTION_2 = 2
COL_DUPLICATE_INDICATOR = 3


def generate_sample(all_questions, questions_size, sample_path):
    questions, questions_data, duplicate_questions_count = sample_questions(all_questions, questions_size)

    if questions_size:
        is_good_sample = evaluate_sample(questions_size, duplicate_questions_count)
        if is_good_sample:
            save_sample_file(questions_data, questions_size, sample_path)
        else:
            gu.print_screen('Sample not good enough for statistics purposes. Running again.')
            questions, questions_data = generate_sample(all_questions, questions_size, sample_path)  # Recursive call.
    else:
        save_sample_file(questions_data, questions_size, sample_path)

    return questions, questions_data


def sample_questions(all_questions, questions_size):
    gu.print_screen('Generating a sample of ' + str(questions_size) + ' questions.')
    questions = []
    duplicate_questions_count = 0

    # Random sample only if questions_size is not zero.
    questions_data = all_questions if not questions_size else random.sample(all_questions, questions_size)

    for i, row in enumerate(questions_data):
        questions_data[i] = [i] + row
        questions.append(row[COL_QUESTION_1])
        questions.append(row[COL_QUESTION_2])
        duplicate_questions_count += int(row[COL_DUPLICATE_INDICATOR])

    return questions, questions_data, duplicate_questions_count


def evaluate_sample(questions_size, duplicate_questions_count):
    """
    Get rid of samples which the duplication rate is lower than 35% or greater than 75%.
    """
    duplicate_rate = duplicate_questions_count / questions_size
    gu.print_screen('Duplicated question quantity: '
                    + str(duplicate_questions_count) + '/' + str(questions_size) + '. Rate: ' + str(duplicate_rate))
    return 0.45 < duplicate_rate < 0.55


def save_sample_file(questions_data, questions_size, sample_path):
    sample_full_path = os.path.join(sample_path, 'question_pairs_subset_' + str(questions_size) + ".csv")
    io_utils.write_csv_file(sample_full_path, questions_data)
