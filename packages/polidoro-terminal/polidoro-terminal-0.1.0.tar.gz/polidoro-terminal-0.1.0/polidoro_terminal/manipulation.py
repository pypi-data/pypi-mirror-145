import os


def tput(cmd):
    os.system(f'tput {cmd}')


def clear_to_end_of_line():
    tput('el')


def clear_to_end_of_screen():
    tput('ed')


def up_lines(lines=1):
    tput(f'cuu {lines}')


def move_left(quantity=1):
    tput(f'cub {quantity}')


def move_right(quantity=1):
    tput(f'cuf {quantity}')


def erase_lines(lines=1):
    for _l in range(lines):
        up_lines()
        clear_to_end_of_line()
