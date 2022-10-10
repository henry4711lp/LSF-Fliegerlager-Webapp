import json

from tabulate import tabulate


def get_table(data):
    tabulate.PRESERVE_WHITESPACE = True
    return tabulate(data, headers=['Datum', '     Anzahl'], tablefmt='html', colalign=("left", "right"), numalign="right")
