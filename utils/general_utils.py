from datetime import datetime


def print_screen(message):
    print('[' + datetime.now().strftime('%H:%M:%S') + '] ' + message)
