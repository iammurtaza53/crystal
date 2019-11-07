from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from E2P.models import Company, Fund, DailyRanks

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import render
from django.core import serializers

from .Excel_to_Postgres import db_bridge
from .Excel_to_Postgres import test_update_DB_files
from .Wilson import main
from .G6 import G6
from .DTableUpdater import DTableUpdater

import pandas as pd
import json
import datetime
import requests

class CompanyResource(ModelResource):
    class Meta:
        queryset = Company.objects.all().order_by('id')
        resource_name = 'companyDetails'
        include_resource_uri = False
        limit = 0
        authentication = Authentication()
        authorization = Authorization()
 

class FundResource(ModelResource):
    class Meta:
        queryset = Fund.objects.all()
        resource_name = 'fund'
        fields = ['is_net_income','most_recent']
        filtering = {
            'most_recent' : ['icontains']
        }


@api_view(['GET'])
def getG6Table(request):
    g6 = G6()
    df = g6.get_main_table()
    return Response(df, status=status.HTTP_200_OK)


@api_view(['GET'])
def generate(request):
    data = {
        'selected': request.GET.getlist('selected[]'),
        'consolidate': request.GET['consolidate'],
        'roster_type': request.GET['roster_type'],
        'all_tickers': request.GET['all_tickers'],
        'all_tickers_textfield': request.GET['all_tickers_textfield'],
        'll_caps_on': request.GET['ll_caps_on'],
        'earnings_exit': request.GET['earnings_exit'],
        'exclude': request.GET['exclude'],
        'custom_message': request.GET['custom_message'],
    }

    for key in list(data):
        if data[key] == 'false':
            del data[key]

    for values in data['selected']: 
        data[values.lower()] = values

    del data['selected']

    response =  main.main(data)
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
def getStrategies(request):
    strategy = request.GET['strategy']
    g6 = G6()
    g6.execute()
    
    if strategy == 'A':
        df = g6.strat_A_df
    if strategy == 'B':
        df = g6.strat_B_df

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
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getPNL(request):    
    g6 = G6()
    df = g6.get_pnl()
    data = {'df':df}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET','POST'])
def updateDb(request):
    if request.method == 'GET':
        file_names = request.GET.getlist('excel_files[]')
        # print(file_names)
        # print("Running Script to get files from Dropbox")
        # test_update_DB_files.update_dropbox_files(file_names,scope='fund_data')
        # print("Files Synced...")
        data = db_bridge.execute(file_names)
        return Response(data, status=status.HTTP_200_OK) 

    if request.method == 'POST':
        data = request.data['data']
        message = db_bridge.updateConflictedRows(data) 
        return Response(message, status=status.HTTP_200_OK) 


@api_view(['GET','POST'])
def getLastUpdateTime(request):
    url = './input_data/dbUpdateTime.json'
    if request.method == 'GET':
        with open(url) as jsonfile:
            dbUploadTime = json.load(jsonfile)
        timeDb = dbUploadTime['time']
        time = {'time': timeDb}
        return Response(time, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        data = {'time': datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")}
        with open(url, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=4, ensure_ascii=False)
        return Response({'success':"Updated"}, status=status.HTTP_200_OK)


@api_view(['GET','POST'])
def allocations(request):
    if request.method == 'GET':
        g6 = G6()
        data = g6.get_allocations()
        return Response(data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data

        allocations = {
            'portfolio': data['portfolio'],
            'within': {
                'primero': {
                    'CONS': data['within']['primero'][0],
                    'INDU': data['within']['primero'][1],
                    'STPL': data['within']['primero'][2],
                    'TECH': data['within']['primero'][3]
                },
                'jump': {
                    'CONS': data['within']['jump'][0],
                    'INDU':data['within']['jump'][1],
                    'STPL': data['within']['jump'][2],
                    'TECH': data['within']['jump'][3]                  
                }
            },
            'target':{
                'primero': {
                    'lmv': data['target']['primero'][0],
                    'CONS': data['target']['primero'][2],
                    'INDU': data['target']['primero'][3],
                    'STPL': data['target']['primero'][4],
                    'TECH': data['target']['primero'][5]
                },
                'jump': {
                    'lmv': data['target']['jump'][0],
                    'CONS': data['target']['jump'][2],
                    'INDU': data['target']['jump'][3],
                    'STPL': data['target']['jump'][4],
                    'TECH': data['target']['jump'][5]
                }
            },
            'strategy_allocations_pct': {
                'primero': {
                    'pct': data['strategy_allocations']['primero'][0]
                },
                'jump': {
                    'pct': data['strategy_allocations']['jump'][0]
                }
            }
        }
        
        with open('./input_data/allocations.json', 'w') as jsonfile:
            json.dump(allocations, jsonfile, indent=4)

        return Response(True, status=status.HTTP_200_OK)


@api_view(['GET','POST'])
def getParams(request):
    if request.method == 'GET':
        g6 = G6()
        data = g6.get_params()
        return Response(data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data
        
        with open('./input_data/strategyParams.json', 'w') as jsonfile:
            json.dump(data, jsonfile, indent=4)

        return Response(True, status=status.HTTP_200_OK)


@api_view(['GET'])
def getPositionsCount(request):
    g6 = G6()
    data = g6.get_positions_count()
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def checkLogin(request):
    credentials = request.data['data']
    url = './input_data/passwordManager.json'
    with open(url) as jsonfile:
        savedCredentials = json.load(jsonfile)
    
    for user in savedCredentials:
        if user['username'] == credentials['username']:
            if user['password'] == credentials['password']:
                return Response(True, status=status.HTTP_200_OK)

    return Response(False, status=status.HTTP_200_OK)


@api_view(['POST'])
def updateCompanyTable(request):
    data = request.data['data']
    if 'newRows' in data:
        newRows = request.data['data']['newRows']
        url = 'http://18.222.131.208:8100/E2P/api/companyDetails/'
        header = {"Content-type": "application/json"}
        for values in newRows:
            newRow = json.dumps(values)
            print(newRow)
            requests.post(url, data=newRow, headers=header)
    
    if 'editRows' in data:
        editRows = request.data['data']['editRows']
        for values in editRows:
            editRow = values
            id = editRow.pop('id')
            url = 'http://18.222.131.208:8100/E2P/api/companyDetails/{}/'.format(id)
            header = {"Content-type": "application/json"}
            editRow = json.dumps(editRow)
            requests.patch(url, data=editRow, headers=header)
 
    return Response(True, status=status.HTTP_200_OK)


@api_view(['GET'])
def getDailyRanksTable(request):
    strategy = request.GET['strategy']
    queryset  = DailyRanks.objects.values('ticker','date',strategy).order_by('ticker','date')
    data = pd.DataFrame(list(queryset))
    data.reset_index(drop=True, inplace=True)
    df = pd.DataFrame()
    data['ticker'] = data['ticker'].str.strip()
    tickers = data['ticker'].unique()
    df = df.reindex(columns = tickers)
    df['date'] = data['date'].unique()

    for ticker in tickers:
        values = data[data['ticker'] == ticker][strategy]
        df[ticker] = values.tolist()
    
    index = df.index
    col = df.columns.tolist()
    col.pop()
    col.insert(0,'date')

    # parse datetimes to string for json object
    df['date'] = df['date'].astype(str)
        
    # create another dataframe for deviations
    df2 = pd.DataFrame()
    g6 = G6()
    g6.execute()
    df2['yield_rank'] = g6.strat_A_df['yield_rank'].tolist()
    values = df.iloc[-1].tolist()
    values.pop()
    df2['last_row'] = values
    df2['last_row'] = df2['last_row'].astype(float)
    df2['Diff'] = round(df2['yield_rank'],2) - round(df2['last_row'],2)
    del df2['last_row']
    df2 = df2.transpose()
    df2.rename({'yield_rank':'Live Summary'},inplace=True)
    df2.reset_index(inplace=True)
    col2 = df2.columns

    # loads dataframe into json
    df = df.to_json(orient='records', double_precision=2)
    df = json.loads(df)

    for values in zip(df,index): 
        values[0]['index']=values[1]

    columns = []
    for values in col:
        columns.append({'text':values, 'value':values, 'sortable':False}) 



    # loads dataframe into json
    df2 = df2.to_json(orient='records', double_precision=2)
    df2 = json.loads(df2)

    columns2 = []
    for values in col2:
        columns2.append({'text':values, 'value':values, 'sortable':False}) 


    data = {
        'df': df,
        'columns': columns,
        'df2': df2,
        'columns2': columns2
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def updateFundFiles(request):
    test_update_DB_files.update_dropbox_files(scope='fund_data')
    return Response("Files Updated Successfully..", status=status.HTTP_200_OK)


@api_view(['GET'])
def updateCompanies(request):
    message = db_bridge.updateCompanies()
    return Response(message, status=status.HTTP_200_OK)


@api_view(['GET'])
def updateDailyRanks(request):
    DTableUpdater().execute(10)
    message = "Table Updated Successfully"
    return Response(message, status=status.HTTP_200_OK)
