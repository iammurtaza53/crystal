from G6.__init__ import client
import json

def lambda_pick_stocks(strategyData):
    response = client.invoke(FunctionName='devPickStocks',InvocationType='RequestResponse',LogType='None',Payload = json.dumps(strategyData))
    response = json.loads(response['Payload'].read())
    if response['status'] == 200:
        local_decision = [values for values in response['result'].values()]
        return local_decision
    return None
