# Written by Sumit Khanna
# License: AGPLv3
# https://battlepenguin.com

from rich.table import Table
from rich.console import Console


def print_cards(cards):
    table = Table(title='Contacts')
    table.add_column('Name')
    table.add_column('Numbers')
    table.add_column('Categories')
    for c in cards:
        nums = ', '.join('{}:{}'.format(k, v) for k, v in c['numbers'].items())
        table.add_row(c['full_name'], nums, ','.join(c['tags']))
    console = Console()
    console.print(table)


def print_cat_counts(cats):
    table = Table(title='Categories')
    table.add_column('Category')
    table.add_column('Num Entries')
    for c in cats.keys():
        table.add_row(c, str(len(cats[c])))
    console = Console()
    console.print(table)
