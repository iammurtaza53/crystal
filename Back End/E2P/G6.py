from E2P.strategy_A import StrategyA
from E2P.strategy_B import StrategyB
import pandas as pd
from numpy import inf, vectorize
import numpy as np
import json
from datetime import date, datetime, timedelta
import calendar
from E2P.params import LL_threshold,LL_20d_atv_threshold
from E2P.aws_lambda import lambda_pick_stocks

class G6:

    def __init__(self):
        self.df = pd.DataFrame()
        self.params_A = {}
        self.params_B = {}
        pass

    def load_market_data(self):
        self.df['price'] = list(pd.read_excel('./input_data/input_market_data.xlsx').price.values)
        self.df['ticker'] = list(pd.read_excel('./input_data/input_market_data.xlsx').ticker.values)  
        self.df.set_index('ticker', drop=False, inplace=True)
        del self.df.index.name
        self.df['book'] = list(pd.read_excel('./input_data/input_ticker_name.xlsx').book.values)  
        self.df['name'] = list(pd.read_excel('./input_data/input_ticker_name.xlsx').name.values)
        self.df['market_cap'] = list(pd.read_excel('./input_data/input_market_data.xlsx').market_cap.values)
        self.df['active_events_and_earnings'] = list(pd.read_excel('./input_data/input_market_data.xlsx').active.values)
        self.df['short_interest_pct_of_float'] = list(pd.read_excel('./input_data/input_market_data.xlsx').short.values)
        self.df['20_day_avg_volume'] = list(pd.read_excel('./input_data/input_market_data.xlsx').day_20_avg_volume.values)
        self.df['days_to_cover'] = list(pd.read_excel('./input_data/input_market_data.xlsx').days.values)
        self.df['short_interest_pct_of_float'] = list(pd.read_excel('./input_data/input_market_data.xlsx').short.values)
        self.df['last_report_date'] = list(pd.read_excel('./input_data/input_market_data.xlsx').date.values)
    
    def get_params(self):
        with open('./input_data/strategyParams.json') as jsonfile:
            parameters = json.load(jsonfile)

        self.params_A = {
                        'LONG_PARAMS': parameters['primero_long'],
                        'SHORT_PARAMS': parameters['primero_short'],
                        'params': parameters['PRIMERO']
                        }
        
        self.params_B = {
                        'LONG_PARAMS': parameters['jump_long'] ,
                        'SHORT_PARAMS': parameters['jump_short'],
                        'params': parameters['JUMP']
                        }           

        return parameters

    def load_fund_data(self):
        self.df['net_income']= list(pd.read_excel('./input_data/input_net_income.xlsx').net_income.values)

    def load_sector_allocations(self):
        allocations = self.get_allocations()
        df_A = allocations['sector_allocations']['primero']
        df_A['SHORT'] = allocations['target']['primero']['smv']
        df_A = df_A.to_frame()
        df_A.columns = [1]
        df_B = allocations['sector_allocations']['jump']
        df_B['SHORT'] = allocations['target']['primero']['smv']
        df_B = df_B.to_frame()
        df_B.columns = [1]
        self.sector_allocations_A = df_A
        self.sector_allocations_B = df_B

    def load_positions(self):
        self.df['position_strat_A'] = list(pd.read_excel('./input_data/input_positions.xlsx').shares_A.values)
        self.df['position_strat_B'] = list(pd.read_excel('./input_data/input_positions.xlsx').shares_B.values)

    def initiate_strategies(self):
        self.strat_A = StrategyA(self.df, self.sector_allocations_A, self.params_A)
        self.strat_B = StrategyB(self.df, self.sector_allocations_B, self.params_B)

    def get_initial_picks(self):
        data_A = {'df':self.df.to_dict(),'params':self.params_A,'allocations':self.sector_allocations_A.to_dict(),'strategy':'A'}
        data_B = {'df':self.df.to_dict(),'params':self.params_B,'allocations':self.sector_allocations_B.to_dict(),'strategy':'B'}
        self.df['initial_pick_strat_A'] = lambda_pick_stocks(data_A)
        self.df['initial_pick_strat_B'] = lambda_pick_stocks(data_B)
        
    def find_conflicts(self):
        conflicts = []
        for conflict in zip(self.df['initial_pick_strat_A'], self.df['initial_pick_strat_B']):
            if conflict[0] != conflict[1]:
                if not (conflict[0] and conflict[1]):
                    conflicts.append(False)
                elif conflict[0] == 'conflict':
                    conflicts.append(False)
                elif conflict[1] == 'conflict':
                    conflicts.append(False)
                else:
                    conflicts.append(True)
            else:
                conflicts.append(False)

        self.df.loc[:,'conflict'] =  conflicts

    def get_post_conflict_allocations(self):
        strat_A_alloc_return = self.strat_A.allocate(self.df)
        self.df.loc[:, 'strat_A_alloc_initial_shares'] = strat_A_alloc_return['shares']
        self.df.loc[:, 'strat_A_alloc_initial_dollars'] = strat_A_alloc_return['dollars']

        strat_B_alloc_return = self.strat_B.allocate(self.df)
        self.df.loc[:, 'strat_B_alloc_initial_shares'] = strat_B_alloc_return['shares']
        self.df.loc[:, 'strat_B_alloc_initial_dollars'] = strat_B_alloc_return['dollars']
        
    def compute_position_caps(self):
        df = pd.DataFrame(columns=[])
        df['total_dollar_allocations'] = self.df['strat_A_alloc_initial_dollars'] + self.df['strat_B_alloc_initial_dollars']

        df['pct_of_total_A'] = self.df['strat_A_alloc_initial_dollars'] / df['total_dollar_allocations'] 
        df['pct_of_total_A'] = df['pct_of_total_A'].fillna(0)
        df['pct_of_total_B'] = self.df['strat_B_alloc_initial_dollars'] / df['total_dollar_allocations'] 
        df['pct_of_total_B'] = df['pct_of_total_B'].fillna(0)
        
        df['total_quota_20_pct_of_20d_ATV'] = self.df['20_day_avg_volume'] * self.df['price'] * LL_20d_atv_threshold
        self.df['max_position_size_A'] = (df['total_quota_20_pct_of_20d_ATV'] * df['pct_of_total_A']).apply(lambda i: round(i, 2))
        self.df['max_position_size_B'] = (df['total_quota_20_pct_of_20d_ATV'] * df['pct_of_total_B']).apply(lambda i: round(i, 2))

    def get_initial_trades(self):
        self.df.loc[:,'strat_A_trade_initial'],self.positions_count_A = self.strat_A.create_trades_initial(max_position_size=self.df.max_position_size_A)
        self.df.loc[:,'strat_B_trade_initial'],self.positions_count_B = self.strat_B.create_trades_initial(max_position_size=self.df.max_position_size_B)

    def compute_trade_caps(self):
        df = pd.DataFrame()
        df['stratA_qty_before_LL_cap'] = self.df['strat_A_trade_initial'].astype(np.float64)
        df['stratB_qty_before_LL_cap'] = self.df['strat_B_trade_initial'].astype(np.float64)
        df['total_abs_quantity'] = abs(df['stratA_qty_before_LL_cap']) + abs(df['stratB_qty_before_LL_cap'])
        df['20_day_avg_volume'] = self.df['20_day_avg_volume']

        LL_trade = []
        for values in zip(df['20_day_avg_volume'], df['total_abs_quantity']):
            if values[1] > values[0] * LL_threshold:
                LL_trade.append(1)
            else:
                LL_trade.append(0)
        df['LL_trade'] = LL_trade

        df['LL_cap_joint'] = round(df['20_day_avg_volume'] * LL_threshold, 0)

        A = abs(df['stratA_qty_before_LL_cap']) / df['total_abs_quantity']
        A[A == -inf] = 0
        A = A.fillna(0)
        df['trade_share_of_A'] = A

        B = abs(df['stratB_qty_before_LL_cap']) / df['total_abs_quantity']
        B[B == -inf] = 0
        B = B.fillna(0)
        df['trade_share_of_B'] = B

        capped_A = []
        for value in zip(df['LL_trade'], df['stratA_qty_before_LL_cap'], df['LL_cap_joint'], df['trade_share_of_A']):
            if value[0] != 1:
                capped_A.append(abs(value[1]))
            else:
                capped_A.append(round(value[2] * value[3], 0))
        self.df.loc[:,'trade_size_max_A'] = vectorize(int)(capped_A)

        capped_B = []
        for value in zip(df['LL_trade'], df['stratB_qty_before_LL_cap'], df['LL_cap_joint'], df['trade_share_of_B']):
            if value[0] != 1:
                capped_B.append(abs(value[1]))
            else:
                capped_B.append(round(value[2] * value[3], 0))
        self.df.loc[:,'trade_size_max_B'] = vectorize(int)(capped_B)

    def add_earnings_exit_flag(self):
        df = pd.DataFrame()

        df['active_manual'] = list(pd.read_excel('./input_data/input_earnings_suspensions.xlsx').active_manual.values)
        
        self.df.reset_index(inplace=True)
        
        df['ticker'] = self.df['ticker']

        df.loc[:,'position_strat_A'] = self.df['position_strat_A']

        df.loc[:,'position_strat_B'] = self.df['position_strat_B']

        df['curr_pos_strat_A'] = np.where(df['position_strat_A'], 1, 0)

        df['curr_pos_strat_B'] = np.where(df['position_strat_B'], 1, 0)

        conditions = [(df['curr_pos_strat_A'] == 0) & (df['curr_pos_strat_B'] == 0)]
        choices = [0]
        df['have_a_position'] = np.select(conditions, choices, default=1)

        conditions = [(df['active_manual'] == 0) & (df['have_a_position'] == 1)]
        choices = [1]
        df['earnings_exit_trade'] = np.select(conditions, choices, default=0)

        #appending to self.df
        self.all_earnings_overrides = list(df.query('earnings_exit_trade==1')['ticker'])
        self.df['earnings_exit_trade'] = df['earnings_exit_trade']
        self.df['active_manual'] = df['active_manual']
        self.df.set_index('ticker', drop=False, inplace=True)
        del self.df.index.name

    def get_final_trades(self):
        self.strat_A_df = self.strat_A.create_trades_final(self.df.trade_size_max_A, self.all_earnings_overrides)
        self.strat_B_df = self.strat_B.create_trades_final(self.df.trade_size_max_B, self.all_earnings_overrides)

    def execute(self):
        self.load_market_data()
        self.get_params()
        self.load_fund_data()
        self.load_sector_allocations()
        self.load_positions()
        self.initiate_strategies()
        self.get_initial_picks()
        self.find_conflicts()
        self.get_post_conflict_allocations()
        self.compute_position_caps()
        self.get_initial_trades()
        self.compute_trade_caps()
        self.add_earnings_exit_flag()
        self.get_final_trades()
        return self.df

    def get_minimized_table(self):
        self.execute()
        minimized_table_A = self.strat_A.generate_minimized_table()
        minimized_table_B = self.strat_B.generate_minimized_table()
        minimized_table_A.reset_index(drop=True, inplace=True)
        minimized_table_B.reset_index(drop=True, inplace=True)
        tables = {
            'min_A': minimized_table_A,
            'min_B': minimized_table_B
        }
        return tables

    def get_positions_count(self):
        self.execute()
        A = self.positions_count_A
        B = self.positions_count_B
        A = A.transpose()
        del A['TOTAL']
        B = B.transpose()
        del B['TOTAL']
        col_A = ['longA','shortA']
        col_B = ['longB','shortB']
        A.columns = col_A
        B.columns = col_B
        C = A.join(B)
        C['TOTAL_LONG'] = C['longA'] + C['longB']
        C['TOTAL_SHORT'] = C['shortA'] + C['shortB']
        data = {'positions_count': C}
        return data

    def get_main_table(self):
        df = self.execute()  
        index = df.index
        col = df.columns
        df = df.to_json(orient='records', double_precision=2)
        df = json.loads(df)
        for values in zip(df,index): values[0]['index']=values[1]
        columns = []
        for values in col:columns.append({'text':values, 'value':values, 'sortable':False}) 
        data = {
            'df': df,
            'columns': columns
        }
        return data

    def get_pnl(self):
        self.execute()
        
        columns_A = ['cur_A','tar_A','trade_A']
        columns_B = ['cur_B','tar_B','trade_B']
        columns_total = ['cur_total','tar_total','trade_total']
        columns_pnl = ['return','strat_A','strat_B','total']

        A = self.strat_A_df[['actual_shares','target_shares','trade_shares']]
        A.columns = columns_A
        
        B = self.strat_B_df[['actual_shares','target_shares','trade_shares']]
        B.columns = columns_B

        df = A.join(B)

        total_actual_shares = self.strat_A_df['actual_shares'] + self.strat_B_df['actual_shares']
        total_target_shares = self.strat_A_df['target_shares'] + self.strat_B_df['target_shares']
        total_trade_shares = self.strat_A_df['trade_shares'] + self.strat_B_df['trade_shares']
        total = pd.concat([total_actual_shares,total_target_shares,total_trade_shares], axis=1)
        total.columns = columns_total

        df = df.join(total)

        returns = list(pd.read_excel('./input_data/input_returns.xlsx').returns.values)
        
        today_pnl_A = []
        today_pnl_B = []
        
        for values in zip(self.strat_A_df['actual_shares'],self.strat_B_df['actual_shares'],self.strat_A_df['price'],returns):
            today_pnl_A.append((values[0]*values[2]*values[3]) / (1+values[3]))
            today_pnl_B.append((values[1]*values[2]*values[3]) / (1+values[3]))
        
        total_pnl = pd.Series(today_pnl_A) + pd.Series(today_pnl_B)
        todays_pnl = pd.concat([pd.Series(returns),pd.Series(today_pnl_A),pd.Series(today_pnl_B),pd.Series(total_pnl)], axis=1)
        todays_pnl.columns = columns_pnl
        
        todays_pnl['strat_A'] = todays_pnl['strat_A'].apply(lambda x:round(x,2))
        todays_pnl['strat_B'] = todays_pnl['strat_B'].apply(lambda x:round(x,2))
        todays_pnl['total'] = todays_pnl['total'].apply(lambda x:round(x,2))
        todays_pnl = todays_pnl.set_index(df.index)
        df = df.join(todays_pnl)
        index = df.index
        df = df.to_json(orient='records', double_precision=2)
        df = json.loads(df)
        for values in zip(df,index): values[0]['index']=values[1]
        return df

    def get_allocations(self):
        with open('./input_data/allocations.json') as jsonfile:
            allocations = json.load(jsonfile)

        portfolio = allocations['portfolio']
        strategy_allocations = pd.DataFrame(allocations['strategy_allocations_pct'])
        strategy_allocations.loc['dollars'] = (strategy_allocations.loc['pct'] / 100) * portfolio

        within = pd.DataFrame(allocations['within'])
        within.loc['total'] = within.sum()

        target = pd.DataFrame(allocations['target'])
        a = (target['primero'] * within['primero']) / 100
        a = a.drop(['lmv','total'])
        a = a.sum()
        b = (target['jump'] * within['jump']) / 100
        b = b.drop(['lmv','total'])
        b= b.sum()
        target.loc['smv'] = [a,b]
        target = target.reindex(['lmv','smv','CONS','INDU','STPL','TECH'])

        sector_allocations = pd.DataFrame()
        sector_allocations['primero'] = (within['primero'] / 100) * strategy_allocations['primero']['dollars']
        sector_allocations['jump'] = (within['jump'] / 100) * strategy_allocations['jump']['dollars']
        sector_allocations.drop('total', inplace=True)
        sector_allocations.loc['total'] = sector_allocations.sum()

        allocations_portfolio = pd.DataFrame()
        allocations_portfolio['primero'] = (sector_allocations['primero'] / portfolio) * 100
        allocations_portfolio['jump'] = (sector_allocations['jump'] / portfolio) * 100
        allocations_portfolio.drop('total', inplace=True)
        allocations_portfolio.loc['total'] = allocations_portfolio.sum()

        lmv_allocations = pd.DataFrame()
        lmv_allocations['primero'] = (within['primero'] / 100) * strategy_allocations['primero']['dollars']
        lmv_allocations['jump'] = (within['jump'] / 100) * strategy_allocations['jump']['dollars']
        lmv_allocations.drop('total', inplace=True)
        lmv_allocations.loc['total'] = lmv_allocations.sum()

        smv_allocations = pd.DataFrame()
        smv_allocations['primero'] = (within['primero'] / 100) * (target['primero'] / 100) * strategy_allocations['primero']['dollars']
        smv_allocations['jump'] = (within['jump'] / 100) * (target['jump'] / 100) * strategy_allocations['jump']['dollars']
        smv_allocations.drop(['total','lmv','smv'], inplace=True)
        smv_allocations.loc['total'] = smv_allocations.sum()

        data = {
            'portfolio': portfolio,
            'strategy_allocations': strategy_allocations,
            'within': within,
            'target': target,
            'sector_allocations': sector_allocations,
            'allocations_portfolio': allocations_portfolio,
            'lmv_allocations': lmv_allocations,
            'smv_allocations': smv_allocations
        }
        return data