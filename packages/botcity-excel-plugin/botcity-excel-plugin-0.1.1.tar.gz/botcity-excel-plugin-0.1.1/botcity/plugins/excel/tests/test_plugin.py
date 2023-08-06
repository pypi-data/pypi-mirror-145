import os

import numpy as np

from botcity.plugins.excel import BotExcelPlugin

cur_dir = os.path.abspath(os.path.dirname(__file__))


reference = [
    ['Name', 'Mana', 'Price', 'Mana/Price', 'Where to Buy'],
    ['Small Mana Potion', 150, 4, 37.5, 'Ginkgo'],
    ['Strong Mana Potion', 300, 12, 25, 'Bicheon'],
    ['Great Mana Potion', 600, 36, 16.66666667, 'Snake Pit']
]

sorted1 = [
    ['Name', 'Mana', 'Price', 'Mana/Price', 'Where to Buy'],
    ['Great Mana Potion', 300, 36, 16.66666667, 'Snake Pit'],
    ['Strong Mana Potion', 300, 12, 25, 'Bicheon'],
    ['Small Mana Potion', 150, 4, 37.5, 'Ginkgo'],
]

sorted2 = [
    ['Name', 'Mana', 'Price', 'Mana/Price', 'Where to Buy'],
    ['Small Mana Potion', 150, 4, 37.5, 'Ginkgo'],
    ['Strong Mana Potion', 300, 12, 25, 'Bicheon'],
    ['Great Mana Potion', 300, 36, 16.66666667, 'Snake Pit'],
]


def test_read():
    """
    Reading tests.

    Performs:
        get_cell(),
        get_row(),
        get_column(),
        get_range(),
        as_list()
    """
    bot = BotExcelPlugin().read('Test Read.xlsx')
    assert bot.get_cell('D', 3) == 25
    assert bot.get_row(3) == reference[2]
    assert bot.get_column('C') == [row[2] for row in reference]
    assert bot.get_range('B2:C4') == [row[1:3] for row in reference[1:4]]
    assert bot.as_list() == reference


def test_write():
    """
    Writing tests.

    Performs:
        add_row(),
        add_rows(),
        add_column(),
        add_columns(),
        write(),
        read(),
        clear(),
        as_list(),
    """
    bot = BotExcelPlugin()
    assert bot.add_row(reference[0][:2]).as_list() == [reference[0][:2]]
    assert bot.add_rows([row[:2] for row in reference[1:]]).as_list() == [row[:2] for row in reference]
    assert bot.add_column([row[2] for row in reference]).as_list() == [row[:3] for row in reference]
    assert bot.add_columns([[row[3] for row in reference], [row[4] for row in reference]]).as_list() == reference
    assert bot.write('Test Write.xlsx').read('Test Write.xlsx').as_list() == reference
    assert bot.clear().write('Test Write.xlsx').read('Test Write.xlsx').as_list() == []


def test_modify():
    """
    Modify tests.

    Performs:
        clear(),
        set_range(),
        set_cell(),
        sort(),
        sort(multiple columns),
        as_list()
    """
    bot = BotExcelPlugin().clear('Página1').clear('New Sheet')
    assert bot.set_range(reference).as_list() == reference
    assert bot.set_cell('B', 4, 300).get_cell('B', 4) == 300
    assert bot.set_cell('A', 1, 'AC', 'New Sheet').get_cell('A', 1, 'New Sheet') == 'AC'
    assert bot.sort('C', False).as_list() == sorted1
    assert bot.sort(['B', 'C'], True).as_list() == sorted2


def test_destroy():
    """
    Test

    Performs:
        set_range(),
        clear_range(),
        remove_row(),
        remove_rows(),
        remove_column(),
        remove_columns(),
        as_list(),
    """
    bot = BotExcelPlugin()
    assert bot.set_range(reference).as_list() == reference
    assert bot.clear_range('A1:B1').get_row(1) == [np.nan, np.nan, 'Price', 'Mana/Price', 'Where to Buy']
    assert bot.remove_row(1).as_list() == reference[1:]
    assert bot.remove_rows([1, 2]).as_list() == [reference[3]]
    assert bot.remove_column('A').as_list() == [reference[3][1:]]
    assert bot.remove_columns(['A', 'B']).as_list() == [reference[3][3:]]
    assert bot.clear().as_list() == []


def test_sheets():
    """
    Tests with different sheets.

    Performs:
        list_sheets(),
        create_sheet(),
        set_active_sheet(new sheet),
        clear(new sheet),
        get_cell(new sheet),
        set_cell(new sheet)
        remove_sheet()

    """
    # Init
    bot = BotExcelPlugin()

    # Create sheet
    if bot.list_sheets().count('New Sheet') > 0:
        bot.remove_sheet('New Sheet')
    assert bot.create_sheet('New Sheet').list_sheets().count('New Sheet') > 0

    # Set Active Sheet
    bot.set_active_sheet('New Sheet')
    assert bot.set_cell('A', 1, 'AC').get_cell('A', 1) == 'AC'
    assert bot.clear().as_list() == []

    # Sheet as Parameter
    bot.set_active_sheet()
    assert bot.set_cell('A', 1, 'AC', 'New Sheet').get_cell('A', 1, 'New Sheet') == 'AC'
    assert bot.clear('New Sheet').as_list('New Sheet') == []

    # Remove Sheet
    assert bot.remove_sheet('New Sheet').list_sheets().count('New Sheet') == 0


def test_range():
    # Add_rows
    bot = BotExcelPlugin().add_rows(reference)
    assert bot.get_range('') == reference
    assert bot.get_range('1') == [reference[0]]
    assert bot.get_range('1:2') == reference[:2]
    assert bot.get_range('A') == [[row[0]] for row in reference]
    assert bot.get_range('A:B') == [row[:2] for row in reference]
    assert bot.get_range('A1:B1') == [reference[0][:2]]
    assert bot.get_range('A1:B2') == [row[:2] for row in reference[:2]]
