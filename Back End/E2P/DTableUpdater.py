from E2P.G6 import G6
from E2P.models import DailyRanks
from datetime import datetime
from django_pandas.io import read_frame
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:admin@localhost:5432/funds')

class DTableUpdater():

    def __init__(self):
        pass
        
    def execute(self,lookback):
        g6 = G6()
        result = g6.get_minimized_table()
        minimized_table = result['min_A']
        #get previous lookup dates from database where record exists
        get_dates_from_database = DailyRanks.objects.order_by('-date').distinct('date').values('date')[:lookback-1]
        
        #convert to dataframe
        dates_dataframe = read_frame(get_dates_from_database)
        
        #loook for the date from which we will query
        date_lookup = dates_dataframe['date'][-1:].values
        
        #get all records since that data which will be our no. of days for lookup
        daily_rank  = DailyRanks.objects.filter(date__gte=date_lookup[0]).values('company_id','ticker','rank')
        
        #convert to dataframe
        comp = []
        tick = []
        rk = []
        for values in daily_rank:
            comp.append(values['company_id'])
            tick.append(values['ticker'])
            rk.append(values['rank'])

        daily_rank = pd.DataFrame()
        daily_rank['company_id'] = comp
        daily_rank['ticker'] = tick
        daily_rank['rank'] = rk

        #convert to float
        daily_rank['rank']  = daily_rank['rank'].astype(float)
        
        # #initilizae global variable for our use
        # global minimized_table
        
        #concat table from G6 and dataframe
        df = pd.concat([daily_rank,minimized_table], axis=0, ignore_index=True, sort=True)
        df = df.fillna(0)
       
        #combine columns from df and G6
        df['comb_rank'] = df['rank'] + df['yield_rank']
        df['ticker'] = df['ticker'].str.strip()

        #create a lookalike database table
        db_table = minimized_table.copy(deep=True)
        db_table['rank_5d_avg'] = list(df.groupby('ticker')['comb_rank'].mean())
        db_table['company_id'] = df['company_id'].unique()[:-1]
        db_table['company_id'] = db_table['company_id'].astype(int)
        db_table['most_recent']  = 'True'
        db_table['date'] = datetime.now().date()
        #update all rows in databse to False
        DailyRanks.objects.filter(most_recent=True).update(most_recent=False)
        #order columns like database
        db_table = db_table[['company_id','ticker','date','net_income','market_cap','most_recent','earnings_yield','yield_rank','rank_5d_avg']]
        #rename columns names
        db_table.columns = ['company_id','ticker','date','net_income','market_cap','most_recent','yield','rank','rank_5d_avg']
        
        #round off values
        db_table['market_cap'] = round(db_table['market_cap'],2)
        db_table['yield'] = round(db_table['yield'],4)
        db_table['rank'] = round(db_table['rank'],2)
        db_table['rank_5d_avg'] = round(db_table['rank_5d_avg'],2)
       
        #delete row for current date if it already exists
        DailyRanks.objects.filter(date=datetime.now().date()).delete()
        
        #insert into database
        db_table.to_sql('daily_ranks', con=engine, if_exists='append', index=False)

        return db_table 