from pandas import read_excel
from numpy import vectorize

CURRENT_PATH = 'E2P/Wilson/source_files/'
SOFTWARE_PATH = 'E2P/Wilson/excel_files/'
OUTPUT_PATH = 'output/'

BBT_trade_codes = {'long' : {'BUY' : '1', 'SELL' : '2'}, 'short' : {'BUY' : '10', 'SELL' : '5'}}
DIRECTION_CODES = {'BBT' : BBT_trade_codes}
DIRECTION_CODES_REVERSE = {'1' : 'Buy', '2' : 'Sell', '5' : 'Sell Short', '10' : 'Buy to Cover'}

MIN_LL_LEFTOVER_VALUE = 25000

CONSOLIDATION_CASES = {'J': [['Buy', 'Buy'], ['Sell', 'Sell'], ['Buy to Cover', 'Buy to Cover'], ['Sell Short', 'Sell Short']],
    # 'K' : [['Buy', 'Buy to Cover'], ['Buy to Cover', 'Buy']],             K type not suppored ty the OMS as of 10/15/18
    'L' : [['Buy', 'Sell'], ['Sell', 'Buy'], ['Buy to Cover', 'Sell Short'], ['Sell Short', 'Buy to Cover']]}

FLIP_CONS_CASES = {
    'F1' : {'Sell' : 1, 'Sell Short' : 2},
    'F2' : {'Sell' : 2, 'Sell Short' : 1},
    'F3' : {'Sell' : 2, 'Sell Short' : 2},
    'F4' : {'Buy' : 2, 'Buy to Cover' : 1},
    'F5' : {'Buy' : 1, 'Buy to Cover' : 2},
    'F6' : {'Buy' : 2, 'Buy to Cover' : 2}}


# old_primero_file_cells = {'first_row' : 7, 'cols_to_load' : 82, 'univ_size' : (0, 6)}
primero_file_cells = {'first_row' : 11, 'cols_to_load' : 82, 'univ_size' : (4, 7)}
jump_file_cells = {'first_row' : 11, 'cols_to_load' : 82, 'univ_size' : (5, 4)}
sloth_file_cells = {'first_row' : 11, 'cols_to_load' : 82, 'univ_size' : (4, 8)}

SOURCE_FILES = {
    # old files, keeping just in case
    # 'consumer' : {'file': 'BELS Research Consumer.xlsx', 'strat' : 'primero', 'cells' : old_primero_file_cells},
    # 'technology' : {'file': 'BELS Research Technology.xlsx', 'strat' : 'primero', 'cells' : old_primero_file_cells},
    # 'industrials' : {'file': 'BELS Research Industrials.xlsx', 'strat' : 'primero', 'cells' : old_primero_file_cells},
    'primero' : {'file': 'BELS_strategy_PRIMERO.xlsx', 'strat' : 'primero', 'cells' : primero_file_cells},
    'jump' : {'file': 'BELS_strategy_JUMP.xlsx', 'strat' : 'jump', 'cells' : jump_file_cells},
    'sloth' : {'file': 'BELS_strategy_SLOTH.xlsx', 'strat' : 'sloth', 'cells' :sloth_file_cells}
}

# strat codes are linked to `book` field which is pulled from portfolio_mapping
# 'CFSTPL' does not exist, here only for testing
primero_strat_codes = {'staples' : 'CFSTPL', 'discretionary' : 'CFCONS', 'healthcare' : 'CFHLTH', 'technology' : 'CFTECH', 'industrials' : 'CFINDU'}
jump_strat_codes = {'staples' : 'JPSTPL', 'discretionary' : 'JPCONS', 'healthcare' : 'JPHLTH', 'technology' : 'JPTECH', 'industrials' : 'JPINDU'}
sloth_strat_codes = {'staples' : 'SLSTPL', 'discretionary' : 'SLCONS', 'healthcare' : 'SLHLTH', 'technology' : 'SLTECH', 'industrials' : 'SLINDU', 'financials' : 'SLFINA', 'REIT' : 'SLREIT'}
combo_strat_codes = {'staples' : 'STPL', 'discretionary' : 'CONS', 'healthcare' : 'HLTH', 'technology' : 'TECH', 'industrials' : 'INDU'}
# has to have all strategies + "combo" - its lenght is used in trade_generator#add_consolidation_tags
STRATEGY_CODES = {'primero' : primero_strat_codes, 'jump' : jump_strat_codes, 'sloth' : sloth_strat_codes, 'combo' : combo_strat_codes}

# probaly won't need this one
ROSTER_CODES = {'roster': {'A' : 'MOC_full', 'B' : 'MOC_LL_half', 'C' : 'LMT_half_EARNINGS', 'D' : 'LMT_LL_leftovers',  'E' : 'LMT_full_OTHER'},
    'csv' : {'A' : 'MOC-VWAP', 'B' : 'LOO', 'C' : 'LMT_regular', 'D' : 'LMT_LL', 'E' : 'VWAP', 'F' : 'MOC', 'G' : 'LMTreg50pct'}}

# standard MOC (used prior to 1/22/19) is 'MLCO3-MC'
ROUTES = {'MOC' : 'MLCO3-QMOC-C', 'LMT regular' : 'MLCO3-CAPLS', 'LMT manual' : 'LMT_LL', 'LOO' : 'MLCO3-LO', 'VWAP' : 'MLCO3-VWAP-MMOC', 'LMT regular 50pct' : 'MLCO3-CAPLS'}

ROSTER_DEFAULTS = {
    'A' : {'order_type': 'MOC/VWAP', 'LL_cap_status' : 'ON'},
    'B' : {'order_type': 'LOO', 'LL_cap_status' : 'OFF'},
    'C' : {'order_type': 'LMT regular', 'LL_cap_status' : 'OFF'},
    'D' : {'order_type': 'LMT manual', 'LL_cap_status' : 'OFF'},
    'E' : {'order_type': 'VWAP', 'LL_cap_status' : 'OFF'},
    'F' : {'order_type': 'MOC', 'LL_cap_status' : 'ON'},
    'G' : {'order_type': 'LMT regular 50pct', 'LL_cap_status' : 'OFF'}
}

EARNINGS_LL_OVERRIDE_TAG = 'earnings exit LL cap override'

def load_portfolio_mapping():
    sheet = read_excel(CURRENT_PATH + 'portfolio_mapping.xlsx', sheet_name = '1', usecols = 7)
    sheet = sheet.iloc[:, 3:6]
    sheet.columns = ['broker_ticker', 'fs_ticker', 'book']
    sheet.broker_ticker = vectorize(str)(sheet.broker_ticker)
    sheet.broker_ticker = vectorize(str.upper)(sheet.broker_ticker)
    sheet.fs_ticker = vectorize(str)(sheet.fs_ticker)
    sheet.fs_ticker = vectorize(str.upper)(sheet.fs_ticker)
    return sheet

PORTFOLIO_MAPPING = load_portfolio_mapping()
