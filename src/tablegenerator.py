import logging
from tabulate import tabulate


def get_table(data):
    """
    This function uses the `tabulate` library to convert the given data into an HTML table.
    If an IndexError is raised, a message is logged with the `logging` module and the function returns 0.
    """
    tabulate.PRESERVE_WHITESPACE = True
    try:
        table = tabulate([v for v in data.items()], headers=['Datum', '     Anzahl Windenstarts'], tablefmt='html', colalign=("left", "right"),
                         numalign="right")
    except IndexError:
        logging.error("Empty Table")
        table = 0
    return table

def get_table_food(data):
    """
    This function uses the `tabulate` library to convert the given data into an HTML table.
    If an IndexError is raised, a message is logged with the `logging` module and the function returns 0.
    """
    tabulate.PRESERVE_WHITESPACE = True
    try:
        table = tabulate(data, headers=['Datum', 'Anzahl Veggie', 'Anzahl Normal', 'Anzahl Kinder Veggie', 'Anzahl Kinder Normal'], tablefmt='html', colalign=("left", "right"),
                         numalign="right")
    except IndexError:
        logging.error("Empty Table")
        table = 0
    return table
