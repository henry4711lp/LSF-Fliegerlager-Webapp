import logging
from tabulate import tabulate


def get_table(data):
    """
    This function uses the `tabulate` library to convert the given data into an HTML table.
    If an IndexError is raised, a message is logged with the `logging` module and the function returns 0.
    """
    tabulate.PRESERVE_WHITESPACE = True
    try:
        table = tabulate(data, headers=['Datum', '     Anzahl'], tablefmt='html', colalign=("left", "right"),
                         numalign="right")
    except IndexError:
        logging.error("Empty Table")
        table = 0
    return table
