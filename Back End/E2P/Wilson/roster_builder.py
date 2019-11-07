# from pdb import set_trace
import string
from numpy import in1d, vectorize
from .codes_joint import *
from pandas import read_excel

class RosterBuilder(object):
    def __init__(self, input):
        self.output = input.copy()
        self.LL_earnings_overrides = []

    def get_table(self):
        return self.output

    def get_roster_type(self):
        return self.roster_type

    def get_order_type(self):
        return self.order_type

    def get_LL_earnings_overrides(self):
        return self.LL_earnings_overrides

    def choose_roster_type(self, roster_type):
        result = roster_type
        if result == 'B':
            print('  >>  ------ DON\'T FORGET TO REMOVE LL REVERSALS. ------')
        self.roster_type = result

    def confirm_order_type(self):
        self.order_type = ROSTER_DEFAULTS[self.roster_type]['order_type']

    def confirm_ticker_set(self, all_tickers, list_of_tickers):
        if self.roster_type not in ['A', 'F']:
            if all_tickers == True:
                self.tickers = ['--ALL']
            else:
                self.tickers = list_of_tickers
        else:
            if all_tickers == True:
                self.tickers = ['--ALL']
            else:
                self.tickers = list_of_tickers

    def remove_unneeded_tickers(self):
        if self.tickers != ['--ALL']:
            only_selected = self.output.loc[in1d(self.output.ticker.values, self.tickers), :]
            if len(only_selected) > 0:
                self.output = only_selected
                response = {'code':None}
                return response
            else:
                message = "There were no trades in your Excel books for any of these tickers: " + str(self.tickers)
                response = {'code': 'no_trades', 'message': message}
                return response
        response = {'code':None}
        return response 

    def impose_half_option(self):
        if self.roster_type == 'G':
            self.output.quantity = vectorize(int)(self.output.quantity / 2)

    def confirm_LL_cap(self, ll_caps_on):
        if ll_caps_on == 0:
            self.LL_cap_status = 'OFF'
        else:
           self.LL_cap_status = 'ON'

    def update_quantity_for_LL_choice(self):
        # making an extra copy of this field because it will be overwritten if LL cap is on, but we'll need it again for earnings exit override
        self.output['qty_full_backup'] = self.output.quantity
        if self.LL_cap_status == 'ON':
            self.output['LL_leftover_value'] = (
                self.output.quantity - self.output.qty_LL_on) * self.output.price
            self.output['cut_qty_to_LL_thold'] = (self.output.strategy != 'primero') | (
                self.output.LL_leftover_value > MIN_LL_LEFTOVER_VALUE)
            self.output.loc[self.output.cut_qty_to_LL_thold,
                            'quantity'] = self.output.loc[self.output.cut_qty_to_LL_thold, 'qty_LL_on']
        # if some trade quantities got replaced by zero (LL), remove those rows
        self.output = self.output[self.output.quantity > 0]

    def add_description(self,custom_message):
        if self.roster_type == 'A':
            result = 'Full rebalance on close with VWAP/MOC'
        elif self.roster_type == 'B':
            result = 'Limit on open'
        elif self.roster_type == 'C':
            result = 'Limit regular during mkt hours'
        elif self.roster_type == 'D':
            result = 'Limit manual (LL)'
        elif self.roster_type == 'E':
            result = 'VWAP'
        elif self.roster_type == 'F':
            result = 'MOC'
        elif self.roster_type == 'G':
            result = 'Limit regular 50%'
        else:
            result = 'Custom:'

        if self.LL_cap_status == 'ON':
            result += ' LL capped '
        else:
            result += ' LL free '

        result += ''.join([i for i in custom_message if i in string.printable])
        self.output['description'] = result
        
    def override_LL_earnings_exits(self, earnings_exit):
        if self.LL_cap_status == 'ON':
            earnings_exits = earnings_exit
            if len(earnings_exits) > 0:
                LL_trades = self.output.loc[self.output.low_liquidity == 1, 'ticker'].values.tolist()
                LL_override_tickers = list(set(earnings_exits).intersection(set(LL_trades)))
                self.output.loc[in1d(self.output.ticker, LL_override_tickers), 'quantity'] = self.output.loc[in1d(self.output.ticker, LL_override_tickers), 'qty_full_backup']
                self.output.loc[in1d(self.output.ticker, LL_override_tickers),'description'] = EARNINGS_LL_OVERRIDE_TAG

                if len(LL_override_tickers) > 0:
                    self.LL_earnings_overrides = LL_override_tickers
                    print('  >>  OK, check this out... here is what we did (rightmost quantity is the one that will be submitted)')
                    print(self.output.loc[in1d(self.output.ticker, LL_override_tickers), ['strategy', 'ticker', 'low_liquidity', 'direction_human', 'qty_LL_on', 'quantity']])

    def remove_active_orders(self, exclude):
        to_exclude = exclude
        if len(to_exclude) > 0:
            self.output = self.output.loc[in1d(self.output.ticker.values, to_exclude, invert=True), :]

    def add_routes(self):
        if self.roster_type == 'A':
            self.output['route'] = ROUTES['VWAP']
            self.output.loc[self.output.strategy =='jump', 'route'] = ROUTES['MOC']
        else:
            self.output['route'] = ROUTES[self.order_type]

    def add_schema(self):
        def f(direction, book, strategy, ticker, send_to_roster):
            if send_to_roster:
                if direction in ['5', '10']:
                    dir_string = 'SHORT'
                    direction_digit = '2'
                else:
                    dir_string = 'LONG'
                    direction_digit = '1'
                if strategy == 'consolidated':
                    perm = 'COMBO - ' + ticker + ' - ' + dir_string
                    temp = STRATEGY_CODES['combo'][book] + ' - ' + direction_digit + ' NA'
                    alloc_sheet_string = STRATEGY_CODES['combo'][book] + ' - ' + direction_digit
                else:
                    perm = temp = alloc_sheet_string = STRATEGY_CODES[strategy][book] + \
                        ' - ' + dir_string
            else:
                perm = temp = alloc_sheet_string = 'ERROR DONT SEND'
            return (perm, temp, alloc_sheet_string)

        s = vectorize(f)(self.output.direction, self.output.book,
                         self.output.strategy, self.output.ticker, self.output.send_to_roster)
        self.output['schema_permanent'] = s[0]
        self.output['schema_temporary'] = s[1]
        self.output['alloc_sheet_string'] = s[2]

    def add_pipe_codes(self):
        def f(direction, book, strategy, alloc_Jump, alloc_Primero, alloc_Sloth):
            if strategy == 'consolidated':
                if direction in ['5', '10']:
                    dir_string = '2'
                else:
                    dir_string = '1'
                result = '|' + STRATEGY_CODES['primero'][book] + ',' + dir_string + ',' + str(alloc_Primero)
                result += '|' + STRATEGY_CODES['jump'][book] + ',' + dir_string + ',' + str(alloc_Jump)
                result += '|' + STRATEGY_CODES['sloth'][book] + ',' + dir_string + ',' + str(alloc_Sloth)
                result += '|,,'
                return result
            else:
                return ''
        self.output['pipe_code'] = vectorize(f)(self.output.direction, self.output.book, self.output.strategy,
                                                self.output.alloc_Jump, self.output.alloc_Primero, self.output.alloc_Sloth)

    def sort(self):
        self.output = self.output.sort_values(by=['strategy', 'book', 'ticker', 'send_to_roster'])

    def execute(self, roster_type, all_tickers, list_of_tickers, ll_caps_on, custom_message, earnings_exit, exclude):
        self.choose_roster_type(roster_type)
        self.confirm_order_type()
        self.confirm_ticker_set(all_tickers, list_of_tickers)
        response = self.remove_unneeded_tickers()
        if response['code'] == 'no_trades':
            return response
        self.impose_half_option()
        self.confirm_LL_cap(ll_caps_on)
        self.update_quantity_for_LL_choice()
        self.add_description(custom_message)
        self.override_LL_earnings_exits(earnings_exit)
        self.remove_active_orders(exclude)
        self.add_routes()
        self.add_schema()
        self.add_pipe_codes()
        self.sort()
        response = {'code': None, 'self': self}
        return response
