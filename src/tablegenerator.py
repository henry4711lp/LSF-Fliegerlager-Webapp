import logging

from tabulate import tabulate


def get_table(data):
    tabulate.PRESERVE_WHITESPACE = True
    try:
        table = tabulate(data, headers=['Datum', '     Anzahl'], tablefmt='html', colalign=("left", "right"), numalign="right")
    except IndexError:
        logging.error("Empty Table")
        table = 0
    return table
