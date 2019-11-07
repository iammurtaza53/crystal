from E2P.models import DailyRanks
from django_pandas.io import read_frame
import pandas as pd
import numpy as np
from decimal import Decimal

class TradingStrategy:
    def __init__(self):
        self.df = pd.DataFrame()
        pass

    def generate_local_trades(self):
        return self

    def get_local_trades(self):
        local_trades = self.generate_local_trades()
        return local_trades

    def get_hist_ranks(self,tickers,which_hist_rank):
        daily_rank  = DailyRanks.objects.filter(most_recent=True,ticker__in=tickers).values('ticker',which_hist_rank)
        df = read_frame(daily_rank)
        print(df)

    def pick_stocks(self):
        pass

    def allocate(self):
        pass

    def enforce_position_caps(self):
        long = ['1' if position =='LONG' else "0" for position in self.df['target_position']]
        self.df['long_count'] = long

        short = ['1' if position =='SHORT' else "0" for position in self.df['target_position']]
        self.df['short_count'] = short

        self.df['20d_atv_threshold'] = self.df['max_position_size']

        def get_variable_positions_count(self):
            positions_count = pd.DataFrame(
                columns=['CONS', 'STPL', 'TECH', 'INDU', 'TOTAL'], index=['LONG', 'SHORT', 'TOTAL'])
            unique = ['CONS', 'STPL', 'TECH', 'INDU']

            long = [len(self.df.loc[(self.df['book'] == unique[index]) & (
                self.df['long_count'] == '1')]) for index in range(len(unique))]
            short = [len(self.df.loc[(self.df['book'] == unique[index]) & (
                self.df['short_count'] == '1')]) for index in range(len(unique))]
            total = [long[i] + short[i] for i in range(len(unique))]

            long.append(sum(long))
            short.append(sum(short))
            total.append(sum(total))
            positions_count.loc['LONG'] = long
            positions_count.loc['SHORT'] = short
            positions_count.iloc[2] = total
            return positions_count

        self.positions_count = get_variable_positions_count(self)

        self.df['unadjusted_allocation'] = self.df.alloc_initial_dollars

        above_20d_threshold = []
        for value in zip(self.df['unadjusted_allocation'], self.df['20d_atv_threshold']):
            if value[0] > value[1]:
                above_20d_threshold.append(1)
            else:
                above_20d_threshold.append(0)

        self.df['above_20d_threshold'] = above_20d_threshold

        excess_long_value = []
        for values in zip(self.df['long_count'], self.df['above_20d_threshold'], self.df['unadjusted_allocation'], self.df['20d_atv_threshold']):
            excess_long_value.append(int(values[0])*values[1]*(values[2]-values[3]))
        self.df['excess_long_value'] = excess_long_value

        excess_short_value = []
        for values in zip(self.df['short_count'], self.df['above_20d_threshold'], self.df['20d_atv_threshold'], self.df['unadjusted_allocation']):
            excess_short_value.append((int(values[0])*values[1]*(values[2]-values[3])) * (-1))
        self.df['excess_short_value'] = excess_short_value

        def table_ll_distrib(self):
            df_table = pd.DataFrame(columns=['CONS', 'TECH', 'INDU', 'STPL'])

            cons_long = self.df.loc[(self.df['book'] == 'CONS') & (
                self.df['target_position'] == 'LONG')]['excess_long_value'].sum()
            cons_short = self.df.loc[(self.df['book'] == 'CONS') & (
                self.df['target_position'] == 'SHORT')]['excess_short_value'].sum()
            tech_long = self.df.loc[(self.df['book'] == 'TECH') & (
                self.df['target_position'] == 'LONG')]['excess_long_value'].sum()
            tech_short = self.df.loc[(self.df['book'] == 'TECH') & (
                self.df['target_position'] == 'SHORT')]['excess_short_value'].sum()
            indu_long = self.df.loc[(self.df['book'] == 'INDU') & (
                self.df['target_position'] == 'LONG')]['excess_long_value'].sum()
            indu_short = self.df.loc[(self.df['book'] == 'INDU') & (
                self.df['target_position'] == 'SHORT')]['excess_short_value'].sum()
            stpl_long = self.df.loc[(self.df['book'] == 'STPL') & (
                self.df['target_position'] == 'LONG')]['excess_long_value'].sum()
            stpl_short = self.df.loc[(self.df['book'] == 'STPL') & (
                self.df['target_position'] == 'SHORT')]['excess_short_value'].sum()

            long = [cons_long, tech_long, indu_long, stpl_long]
            short = [cons_short, tech_short, indu_short, stpl_short]

            df_table.loc['LONG'] = long
            df_table.loc['SHORT'] = short

            return df_table

        ll_distrib_table = table_ll_distrib(self)

        def table_ll_pos(self):
            df_table = pd.DataFrame(columns=['CONS', 'TECH', 'INDU', 'STPL'])

            cons_long = self.df.loc[(self.df['book'] == 'CONS') & (
                self.df['target_position'] == 'LONG')]['above_20d_threshold'].sum()
            cons_short = self.df.loc[(self.df['book'] == 'CONS') & (
                self.df['target_position'] == 'SHORT')]['above_20d_threshold'].sum()
            tech_long = self.df.loc[(self.df['book'] == 'TECH') & (
                self.df['target_position'] == 'LONG')]['above_20d_threshold'].sum()
            tech_short = self.df.loc[(self.df['book'] == 'TECH') & (
                self.df['target_position'] == 'SHORT')]['above_20d_threshold'].sum()
            indu_long = self.df.loc[(self.df['book'] == 'INDU') & (
                self.df['target_position'] == 'LONG')]['above_20d_threshold'].sum()
            indu_short = self.df.loc[(self.df['book'] == 'INDU') & (
                self.df['target_position'] == 'SHORT')]['above_20d_threshold'].sum()
            stpl_long = self.df.loc[(self.df['book'] == 'STPL') & (
                self.df['target_position'] == 'LONG')]['above_20d_threshold'].sum()
            stpl_short = self.df.loc[(self.df['book'] == 'STPL') & (
                self.df['target_position'] == 'SHORT')]['above_20d_threshold'].sum()

            long = [cons_long, tech_long, indu_long, stpl_long]
            short = [cons_short, tech_short, indu_short, stpl_short]

            df_table.loc['LONG'] = long
            df_table.loc['SHORT'] = short

            return df_table

        ll_pos_table = table_ll_pos(self)

        def get_extra_allocation(self, ll_distrib_table, ll_pos_table):
            extra_allocation = []
            for index, value in enumerate(self.df['above_20d_threshold']):
                if value == 1:
                    extra_allocation.append(-(self.df['excess_short_value'][index] + self.df['excess_long_value'][index]))
                else:
                    book = self.df['book'][index]
                    if self.df['target_position'][index] == 'LONG':
                        extra_allocation.append(ll_distrib_table[book]['LONG'] / (self.positions_count[book]['LONG'] - ll_pos_table[book]['LONG']))
                    else:
                        if self.df['target_position'][index] == 'SHORT':
                            extra_allocation.append(ll_distrib_table[book]['SHORT'] / (self.positions_count[book]['SHORT'] - ll_pos_table[book]['SHORT']))
                        else:
                            extra_allocation.append(0)
            return extra_allocation

        self.df['extra_allocation'] = get_extra_allocation(self, ll_distrib_table, ll_pos_table)

        self.df['ADTV_20d'] = self.df['20_day_avg_volume']

        self.df['alloc_adjusted'] = self.df['unadjusted_allocation'] + self.df['extra_allocation']
        self.df['alloc_adjusted'] = round(self.df['alloc_adjusted'],2)

        self.df['alloc_adj_pct_20d_ADTV'] = self.df['alloc_adjusted'] / (self.df['20_day_avg_volume'] * self.df['price'])

    def compute_capped_trades(self):
        self.df = self.compute_yield_rank_and_long_short_includes(self.df)
        self.df = self.compute_localdecision_long_short_count(self.df)

        # here mini tables are created
        self.positions_count = self.get_variable_positions_count(self.df)
        tgt_usd = self.get_tgt_usd(self.df, self.positions_count)
        tgt_wgt = self.get_tgt_wgt(self.df, tgt_usd)

        self.df['target_shares'] = np.vectorize(self.get_target_shares)(self.df['target_position'], self.df['alloc_adjusted'], self.df['price'])
        # compute variables
        avg_size_long = (tgt_wgt.loc['LONG']).mean()
        avg_size_short = -(tgt_wgt.loc['SHORT']).mean()
        long_reb_thold = avg_size_long * self.params['LONG_PARAMS']
        short_reb_thold = avg_size_short * self.params['SHORT_PARAMS']

        self.df = self.compute_differences(self.df)
        self.df = self.compute_action_and_impliedshares(self.df, long_reb_thold, short_reb_thold)

        self.df['trade_direction'] = self.df['action']
        self.df['trade_shares'] = self.df['difference']
        self.df['trade_value'] = self.df['price'] * self.df['trade_shares']
        shares = []
        for value in self.df['trade_value']:
            shares.append(float(round(Decimal(value),2)))
        self.df['trade_value'] = shares

    def create_trades_initial(self, max_position_size):
        self.df['max_position_size'] = max_position_size
        self.enforce_position_caps()
        self.compute_capped_trades()
        return self.df.trade_shares, self.positions_count

    def create_trades_final(self, trade_size_max, overrides):
        self.df['trade_size_max'] = trade_size_max

        new_target = []
        for index, values in enumerate(self.df['ticker']):
            if values in list(overrides):
                new_target.append(0)
            else:
                new_target.append(self.df['target_shares'][index])
        self.df['target_shares'] = new_target

        new_position = []
        for index, values in enumerate(self.df['ticker']):
            if values in list(overrides):
                new_position.append('')
            else:
                new_position.append(self.df['target_position'][index])
        self.df['target_position'] = new_position

        direction = []
        trade_shares = []
        trade_size_max = []
        for value in zip(self.df['target_shares'],self.df['actual_shares'],self.df['trade_direction'],self.df['trade_shares'],self.df['trade_size_max']):
            if value[0] == 0:
                if value[1] == 0:
                    direction.append('')
                    trade_shares.append(0)
                    trade_size_max.append(abs(value[1]))
                elif value[1] > 0:
                        direction.append('SELL')
                        trade_shares.append(value[1])
                        trade_size_max.append(abs(value[1]))
                elif value[1] < 0:
                    direction.append('BUY')
                    trade_shares.append(abs(value[1]))
                    trade_size_max.append(abs(value[1]))
            else:
                direction.append(value[2])
                trade_shares.append(value[3])
                trade_size_max.append(value[4])
            
        self.df['trade_direction'] = direction
        self.df['trade_shares'] = trade_shares
        self.df['trade_value'] = self.df['price'] * self.df['trade_shares']
        self.df['trade_size_max'] = trade_size_max
                    
        return self.df
