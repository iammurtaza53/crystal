# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 16:07:18 2018

@author: HP 840
"""
import os
from . import db_strings

query1 = db_strings.query1
query2 = db_strings.query2
query3 = db_strings.query3
query4 = db_strings.query4
query5 = db_strings.query5
excel_columns = db_strings.excel_columns
excel_columns_healthcare = db_strings.excel_columns_healthcare

#Database Credentials
def getCredentials(): 
    credentials = {
            'database' : 'funds',
            'user' : 'postgres',
            'password' : 'admin',
            'host' : 'localhost',
            'port' : '5432',
            }
    return credentials


# path to the directory where our excel files are stored
path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'excel_files')



