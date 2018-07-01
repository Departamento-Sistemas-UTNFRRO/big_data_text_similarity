import csv
import logging


def get_logger(logging_file):
    logger = logging.getLogger(logging_file)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('[%(levelname)s] [%(asctime)-15s] [%(filename)s] %(message)s')
        ch.setFormatter(formatter)

        logger.addHandler(ch)

    return logger


# Ver si esto se sigue necesitando.
def define_first_row(previous_path):
    """
    This starts the computation from other than the first row of the file, when needed.
    :param previous_path: saved results.
    :return: row when the computation has to start.
    """
    first_row = 0

    if previous_path is not None:
        with open(previous_path) as previous_runs:
            reader = csv.reader(previous_runs)
            next(reader)  # Ignores the header

            for _ in reader:
                first_row += 1

    return first_row
