from polidoro_terminal.size import size, columns, rows
from polidoro_terminal.manipulation import erase_lines, up_lines, clear_to_end_of_line
from polidoro_terminal import cursor
from polidoro_terminal.color import Color
from polidoro_terminal.format import Format
from polidoro_terminal.getch import getch, getche

NAME = 'polidoro_terminal'
VERSION = '0.1.0'

__all__ = ['size', 'columns', 'rows', 'erase_lines', 'up_lines', 'clear_to_end_of_line', 'cursor', 'Color',
           'Format', 'getch', 'getche']
