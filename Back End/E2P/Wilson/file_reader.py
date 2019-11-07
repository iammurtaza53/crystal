from pandas import read_excel, read_csv
from string import ascii_lowercase
from numpy import vectorize
from .codes_joint import *
from . import UI
import datetime
from sys import exit

class FileReader(object):

    def __init__(self, dict, curr_folder):
        self.filename = dict['file']
        self.curr_folder = curr_folder
        self.strat = dict['strat']
        self.cols = self.read_excel_col_codes(self.strat)
        self.cells = dict['cells']
        self.first_row = self.cells['first_row']
        self.univ_size = self.cells['univ_size']
        self.cols_to_load = self.cells['cols_to_load']

    def read_excel_col_codes(self, strategy):
        csv = read_csv(SOFTWARE_PATH + 'excel_columns.csv')
        result = {csv.item[i] : csv.loc[i, strategy] for i in range(csv.shape[0])}
        return result

    def load_from_excel(self):
        print('Loading ' + self.filename + '... hang on...')
        fn = self.curr_folder + self.filename
        sheet = read_excel(fn, sheet_name='Summary', usecols=self.cols_to_load, header=None)
        if self.strat == 'primero':
            reconcile_time = read_excel('./excel_files/input_positions.xlsx')
            reconcile_time = reconcile_time['dateTime'][0]
            now = datetime.datetime.now()
            max_delta = datetime.timedelta(hours = 1.5)
            if now - reconcile_time > max_delta:
                message = "That\'s interesting... The time is now " + now.strftime("%H:%M:%S") + " and last time you reconciled positions was at " +  reconcile_time.strftime("%H:%M:%S") + " Didn\'t you just tell me that you have reconciled AND SAVED positions? You have actually TYPED the entire word 'reconciled' to confirm that."
                response = { 'code':'limit_exceed',
                             'message':message
                             }
                return response

        univ_size = sheet.iloc[self.univ_size]
        last_row = self.first_row - 1 + univ_size
        table = sheet.copy().iloc[self.first_row - 1 : last_row, :]
        table.columns = sheet.iloc[self.first_row - 2, :]
        self.table = table
        response = {'code': 'done'}
        return response

    def rename_columns(self):
        excel_colnames = [p + i for p in ['', 'a', 'b'] for i in ascii_lowercase]
        excel_colnames.extend(('ca', 'cb', 'cc', 'cd', 'ce'))
        assert len(excel_colnames) == self.cols_to_load + 1, 'Mismatch between cols_to_load and Excel colnames, fix dictionary and/or "rename_columns" method of FileReader'

        # if there are any blank columns (because of mismatch in Primero vs Jump files), add dummy columns so it doesn't throw an error
        if self.table.shape[1] < len(excel_colnames):
            for i in range(1, len(excel_colnames) - self.table.shape[1] + 1):
                self.table['extra_' + str(i)] = ['--'] * self.table.shape[0]
        self.table.columns = excel_colnames
        
        self.table = self.table.loc[:, list(self.cols.values())]
        self.table.columns = self.cols.keys()

    def add_computed_columns(self):
        self.table['strategy'] = self.strat
        
    def clean_up(self):
        f = vectorize(lambda x: True if x == 'SELL' or x == 'BUY' else False)
        self.table = self.table[f(self.table.direction)]
        self.table.ticker = vectorize(str)(self.table.ticker)
        self.table.ticker = vectorize(str.upper)(self.table.ticker)

    def check_for_data_errors(self):
        # nan only allowed in Target Position, everything else should have a value
        cols = list(self.table)
        cols.remove('tgt_position')
        for i in cols:
            if self.table.loc[:,i].isnull().values.any():
                UI.error_exit('Your Excel file has an error in "' + self.strat + '" file, "' + i + '" column. Fix it and try again.')

    def execute(self):
        response = self.load_from_excel()
        if response['code'] is 'limit_exceed':
            return response
        self.rename_columns()
        self.add_computed_columns()
        self.clean_up()
        self.check_for_data_errors()
        response = {'code':None, 'table':self.table }
        return response
