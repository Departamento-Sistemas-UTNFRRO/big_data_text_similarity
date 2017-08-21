import argparse
import csv
import re
from datetime import datetime
from utils import general_utils as gu


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


def remove_special_delimiters(text):
    # Removes special characters that are at the begining of the sentence,
    # at the end, or next to a space. It also separates words in the form word1/word2
    sentence = filter(None, re.split('^\W*|\W*\s\W*|\W*$|/', text))
    return ' '.join(sentence)


def clean_text(text):
    text = text.lower()
    text = remove_formulas(text)
    text = replace_numbers(text)
    text = remove_special_delimiters(text)

    return text


if __name__ == '__main__':
    start_time = datetime.now()

    parser = argparse.ArgumentParser(description='Limpia las preguntas')
    parser.add_argument('-quora', dest='quora_path', required=True)
    parser.add_argument('-results', dest='results_path', required=True)
    args = parser.parse_args()

    quora_path = args.quora_path
    results_path = args.results_path

    gu.print_screen('Starting script.')

    with open(quora_path, 'r') as tsv_in, open(results_path, 'w') as csv_out:
        reader = csv.reader(tsv_in, delimiter='\t')
        writer = csv.writer(csv_out)

        for row in reader:
            id = row[0]
            if id.isdigit() and id != '0' and int(id) % 1000 == 0:
                gu.print_screen('First ' + id + ' pairs pre-processed.')

            result = [
                id,                  # Pair ID
                clean_text(row[3]),  # Question 1
                clean_text(row[4]),  # Question 2
                row[5]               # Duplicate
            ]

            writer.writerow(result)

    gu.print_screen('Script finished. Total time: ' + str(datetime.now() - start_time))