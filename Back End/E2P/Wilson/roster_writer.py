from .helpers import *
from .codes_joint import *
from datetime import datetime
from pandas import DataFrame
# from pdb import set_trace
from numpy import vectorize

class RosterWriter(object):
    def __init__(self, roster, curr_folder):
        self.set_curr_folder(curr_folder)
        self.messages = []
        self.table = roster.get_table()
        self.roster_type = roster.get_roster_type()
        self.order_type = roster.get_order_type()
        self.LL_earnings_overrides = roster.get_LL_earnings_overrides()
        self.LL_cap_status = roster.LL_cap_status

    def set_curr_folder(self, folder):
        self.curr_folder = folder + OUTPUT_PATH

    def timestamp(self):
        return datetime.now().strftime('%m-%d-%y_%H%M')

    def save_roster(self):
        wb = load_workbook(self.curr_folder + 'trade roster - template.xlsx', data_only=True)
        sheet = wb['roster']
        write_column_xlsx(sheet, 'a', 3, self.table.send_to_roster)
        write_column_xlsx(sheet, 'b', 3, self.table.route)
        write_column_xlsx(sheet, 'c', 3, self.table.strategy)
        write_column_xlsx(sheet, 'd', 3, self.table.book)
        write_column_xlsx(sheet, 'e', 3, self.table.ticker)
        write_column_xlsx(sheet, 'f', 3, self.table.actual_shares)
        write_column_xlsx(sheet, 'g', 3, self.table.target_shares)
        write_column_xlsx(sheet, 'h', 3, self.table.direction_human)
        write_column_xlsx(sheet, 'i', 3, self.table.quantity)
        write_column_xlsx(sheet, 'j', 3, self.table.price, update_to_currency = True)
        write_column_xlsx(sheet, 'k', 3, self.table.limit_price)
        write_column_xlsx(sheet, 'l', 3, self.table.quantity * self.table.price, update_to_currency = True)
        write_column_xlsx(sheet, 'm', 3, self.table.NAV_diff)
        write_column_xlsx(sheet, 'n', 3, self.table.rank_long)
        write_column_xlsx(sheet, 'o', 3, self.table.rank_avg)
        write_column_xlsx(sheet, 'p', 3, self.table.rank_short)
        write_column_xlsx(sheet, 'q', 3, self.table.todays_price_return)
        write_column_xlsx(sheet, 'r', 3, self.table.next_report_date)
        write_column_xlsx(sheet, 's', 3, self.table.cfo_growth)
        write_column_xlsx(sheet, 't', 3, self.table.pct_of_20d_ATV)
        write_column_xlsx(sheet, 'u', 3, self.table['20d_ATV'])
        write_column_xlsx(sheet, 'v', 3, self.table.rank_vs_15d_avg)
        write_column_xlsx(sheet, 'w', 3, self.table.reversal)
        write_column_xlsx(sheet, 'x', 3, self.table.low_liquidity)
        write_column_xlsx(sheet, 'y', 3, self.table.description)
        write_column_xlsx(sheet, 'z', 3, self.table.cons_type)
        write_column_xlsx(sheet, 'aa', 3, self.table.cons_id)
        write_column_xlsx(sheet, 'ab', 3, self.table.alloc_Primero)
        write_column_xlsx(sheet, 'ac', 3, self.table.alloc_Jump)
        write_column_xlsx(sheet, 'ad', 3, self.table.send_to_sheet)

        if self.order_type == 'MOC':
            filename = (self.curr_folder + 'BDC_trade_sheet_EOD_' + self.timestamp() + '.xlsx')
        else:
            filename = (self.curr_folder + 'BDC_trade_sheet_' + self.timestamp() + '.xlsx')
        wb.save(filename)
        print()
        message = 'Trade sheet saved to ' + filename + '.'
        # # print(message)
        self.messages.append(message)


    # until Phil confirms combo schema, we're using CF "GENERAL" schema for consolidated trades
    def save_csv_temporary(self):
        temp = self.table.loc[self.table.send_to_roster, :].copy()
        result = DataFrame({'schema' : temp.schema_temporary})
        result['ticker'] = temp.broker_ticker
        result['exec_strategy'] = temp.route
        result['side'] = temp.direction
        result['qty'] = temp.quantity
        if self.order_type in ['LOO', 'LMT regular', 'LMT manual', 'LMT regular 50pct']:
            result['lmt_price'] = self.table.limit_price
        filename = (self.curr_folder + 'BDC_trade_roster_GEN_' + ROSTER_CODES['csv'][self.roster_type] + '_' + self.timestamp() + '.csv')
        result.to_csv(filename, index = False, header = False)
        message = 'OMS roster ' + self.order_type + ' saved to ' + filename + '.'    
        # # print(message)
        self.messages.append(message)

    def save_csv_permanent(self, route_filter = 'all'):
        temp = self.table.loc[self.table.send_to_roster, :]
        if route_filter != 'all':
            temp = temp.loc[temp.route == ROUTES[route_filter], :]

        result = DataFrame({'schema' : temp.schema_permanent})
        result['ticker'] = temp.broker_ticker
        result['exec_strategy'] = temp.route
        result['side'] = temp.direction
        result['qty'] = temp.quantity
        # once Phil confirms that pipe codes work, append pipe code to limit price (and "" if none)
        if self.order_type in ['LOO', 'LMT regular', 'LMT manual', 'LMT regular 50pct']:
            result['lmt_price'] = self.table.limit_price
        temp.loc[temp.pipe_code == '-1', 'pipe_code'] = ''
        result['pipe_code'] = temp.pipe_code
        filename = (self.curr_folder + 'BDC_trade_roster_combo_' + route_filter + '_' + self.timestamp() + '.csv')
        result.to_csv(filename, index = False, header = False)
        message = 'OMS roster ' + self.order_type + ' saved to ' + filename + '.'
        # print(message)
        self.messages.append(message)

    # temporary, until combo schema is functional
    def save_allocations(self):
        temp = self.table.loc[self.table.strategy == 'consolidated', :].copy()
        if temp.shape[0] > 0:
            result = DataFrame({'ticker' : temp.broker_ticker})
            result['strategy_code'] = temp.alloc_sheet_string
            result['qty'] = temp.quantity
            result['Primero'] = temp.alloc_Primero
            result['Jump'] = temp.alloc_Jump
            result['Sloth'] = temp.alloc_Sloth
            
            filename = (self.curr_folder + 'post-trade_allocation_' + self.timestamp() + '.csv')
            result.to_csv(filename, index = False, header = True)
            message = 'Trade allocation saved to ' + filename + '.'
            # print(message)
            self.messages.append(message)

    def save_LL_list(self):
        LL = self.table.loc[self.table.low_liquidity == 1, ['strategy', 'book', 'ticker']]
        sections = set(LL.strategy) - {'consolidated'}
        LL_filename = (self.curr_folder + 'LL_leftovers_' + self.timestamp() + '.txt')
        combined_list = []
        with open(LL_filename, 'w') as f:
            print('All LL trades - for reconciliation:', file = f)
            for section in sections:
                LL_section = LL.loc[LL.strategy == section, :]
                print('----------------------------------------------------------', file = f)
                print('STRATEGY: ' + section, file = f)
                for book in set(LL_section.book):
                    ticker_list = list(LL_section.loc[LL_section.book == book, 'ticker'])
                    combined_list.extend(ticker_list)
                    ticker_list = ' '.join(sorted(ticker_list))
                    print(book + ' : ' + ticker_list, file = f)
            print('----------------------------------------------------------', file = f)
            print('All LL trades ex earnings exits - for trading next morning:', file = f)
            combined_list = list(set(combined_list) - set(self.LL_earnings_overrides))
            combined_list = ' '.join(sorted(combined_list))
            print(combined_list, file = f)
        message = ' LL leftovers for tomorrow morning saved to ' + LL_filename + '.'
        # print(message)
        self.messages.append(message)

    def execute(self):
        self.save_roster()

        if self.roster_type == 'A':
            # temporary, while we have to send Jump to Merrill separately and not consolidate,
            # EOD trades will create two separate csv files
            self.save_csv_permanent('MOC')
            self.save_csv_permanent('VWAP')
        else:
            self.save_csv_temporary()

        self.save_allocations()

        if (self.roster_type in ['A', 'E', 'F']) & (sum(self.table.low_liquidity) > 0) & (self.LL_cap_status == 'ON'):
            self.save_LL_list()

        return self.messages
        # self.save_csv()
        # self.save_csv_permanent()
