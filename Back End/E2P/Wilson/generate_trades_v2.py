from pandas import concat, read_csv

# params and reference (mapping of Excel columns etc.)
from .codes_joint import *

# collections of stuff that don't qualify for own class
from . import helpers
from . import UI

# from pdb import set_trace

# custom classes, each in own file
from .file_reader import FileReader
from .trade_generator import TradeGenerator
from .roster_builder import RosterBuilder
from .roster_writer import RosterWriter


import pandas as pd
pd.set_option('display.max_columns', 500)


def confirm_strategy():
    temp_dict = {'1' : 'primero', '2' : 'jump', '3' : 'sloth', '4' : ['primero', 'jump', 'sloth']}
    message = 'We\'ll generate rosters for Primero, Jump and Sloth. Hit Enter to accept, or type strategy you need, ' \
        + '(1 for Primero, 2 for Jump, 3 for Sloth, 4 for all three)  >>   '
    code = UI.get_multiple_choice_input(message, list(temp_dict.keys()), '4')
    return temp_dict[code]

def load_from_books(path):
    table = []
    strat_selected = confirm_strategy()
    for i in [j for j in SOURCE_FILES.values() if j['strat'] in strat_selected]:
        curr_table = FileReader(dict = i, curr_folder = path).execute()
        table.append(curr_table)

    assert sum([list(table[i]) == list(table[0]) for i in range(len(table))]) == len(table), \
        'Mismatch between column names, make sure all "_file_columns" dictionaries have same keys in same order'
    return concat(table, ignore_index = True)
    
def main():
    # changes curr div to argv[1] if any provided AND return argv[1] so we can pass it to classes. can be used for debugging
    # curr_dir = helpers.set_working_dir()
    
    # UI.greeting()
    trades_from_Excel = load_from_books(CURRENT_PATH)
    trades_for_roster = TradeGenerator(trades_from_Excel).execute()
    roster = RosterBuilder(trades_for_roster).execute()
    RosterWriter(roster, CURRENT_PATH).execute()
    UI.show_done_message()

    # for testing
    # while True:
    #     roster = RosterBuilder(trades_for_roster).execute()
    #     RosterWriter(roster, CURRENT_PATH).execute()
    #     UI.show_done_message()
        
    #     again = UI.get_multiple_choice_input('Wanna try to create a different roster? No reload time... (0 for No, 1 or Enter for Yes)  >>   ', ['0', '1'], ['1'])
    #     if again == '0':
    #         break

main()


# ----------------------------------------------------------------------
# for testing

# tt = FileReader(SOURCE_FILES['primero'], CURRENT_PATH)
# tt.load_from_excel()
# tt.rename_columns()
# tt.add_computed_columns()
# tt.clean_up()
# oo = tt.table


# trades_from_Excel = load_from_books(CURRENT_PATH)
# trades_for_roster = TradeGenerator(trades_from_Excel).execute()
# roster = RosterBuilder(trades_for_roster).execute()
# set_trace()