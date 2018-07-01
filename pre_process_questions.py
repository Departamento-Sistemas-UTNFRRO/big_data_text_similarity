import argparse
import csv
import re
from datetime import datetime
import config
import utils.general_utils as gu

logger = gu.get_logger(__name__)


def remove_special_delimiters(text):
    # Removes special characters that are at the beginning of the sentence,
    # at the end, or next to a space. It also separates words in the form word1/word2
    sentence = filter(None, re.split('^\W+|\W+\s\W+|\W+$|/', text))
    return ' '.join(sentence)


def remove_formulas(text):
    # Removes formulas between [math] and [code] tags
    sentence = filter(None, re.split('\[math\].*\[/math\]|\[code\].*\[/code\]', text))
    return ' '.join(sentence)


def replace_numbers(text):
    numbers = {'0': 'zero',
               '1': 'one',
               '2': 'two',
               '3': 'three',
               '4': 'four',
               '5': 'five',
               '6': 'six',
               '7': 'seven',
               '8': 'eight',
               '9': 'nine'}

    refactored_text = ''
    for character in text:
        if re.match('[0-9]', character):
            refactored_text += numbers[character] + ' '
        else:
            refactored_text += character

    return refactored_text


def clean_text(text):
    text = text.lower()
    text = remove_formulas(text)
    text = replace_numbers(text)
    text = remove_special_delimiters(text)

    return text


def start(raw_quora_path, quora_path):
    start_time = datetime.now()
    logger.info('Starting script.')

    with open(raw_quora_path, 'r') as tsv_in, open(quora_path, 'w') as csv_out:
        reader = csv.reader(tsv_in, delimiter='\t')
        writer = csv.writer(csv_out)

        for row in reader:
            question_pair_id = row[config.raw_quora_file.get("pair_id")]
            if question_pair_id.isdigit() and question_pair_id != '0' and int(question_pair_id) % 1000 == 0:
                logger.info('First ' + question_pair_id + ' pairs pre-processed.')

            writer.writerow([question_pair_id,
                             clean_text(row[config.raw_quora_file.get("question1")]),
                             clean_text(row[config.raw_quora_file.get("question2")]),
                             row[config.raw_quora_file.get("duplicate_indicator")]])

    logger.info('Pre-process questions finished. Total time: ' + str(datetime.now() - start_time))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cleaning of raw question files')
    parser.add_argument('-q', dest='quora_path', required=True)
    parser.add_argument('-r', dest='results_path', required=True)
    args = parser.parse_args()

    start(args.quora_path, args.results_path)
