import json
import pandas as pd
import devStratA as devA
import devStratB as devB

def lambda_handler(event,context):
    strategy = event['strategy']
    params = event['params']
    df = pd.DataFrame(event['df'])
    allocations = pd.DataFrame(event['allocations'])
    
    if strategy == 'A':
        result = devA.StratA(df=df,allocations=allocations,params=params).get_all_data()
        return {'result': result['local_decision'].to_dict(),'status':200}
    else:
        result= devB.StratB(df=df,allocations=allocations,params=params).get_all_data()
        return {'result':result['local_decision'].to_dict(),'status':200}
