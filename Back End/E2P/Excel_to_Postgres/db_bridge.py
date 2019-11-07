# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 16:31:50 2018

@author: HP 840
"""

# imports all libraries to be used in our code
from . import db_bridge_helpers
import os
import pandas as pd
import numpy as np
import psycopg2
import sys
from datetime import datetime as dt
from datetime import timedelta

# imports credentials from db_bridge_helpers
credentials = db_bridge_helpers.getCredentials()

# creates a tunnel between database and python through which data will be exchanged
conn = psycopg2.connect(database=credentials['database'], user=credentials['user'], password=credentials['password'],
                        host=credentials['host'], port=credentials['port'])
print("Database Connected....")
cursor = conn.cursor()


# Our main Class
class ExcelToPostgres:
    # moves all data to a variable array from excel sheet
    def insertNewDataAfterCompany(self, get_ticker_name, excel_record, com_id):
        values = []
        for index5 in range(len(excel_record.index)):
            for names in excel_record.iloc[index5]:
                values.append(names)

        # copies months and years from excel to variables month and year
        months = []
        year = []
        for mnth_year in excel_record.index:
            if mnth_year == '-':
                months.append('-')
                year.append('-')
            else:
                my = mnth_year.split()
                months.append(my[0])
                year.append(my[1])

        # loop runs until all values are inserted in database from excel
        for number in range(len(months)):
            is_active = True
            most_recent = False

            # gets current datetime
            dateTime = dt.now()

            # inserts data into database
            query = db_bridge_helpers.query1
            
            data_builder = "(com_id,is_active,most_recent,months[number],year[number],dateTime,"
            for loop in range(160):
                data_builder +=  'values[%s]'%loop + "," 
    
            data_builder += ')'   
            data = data_builder[:-2] + data_builder[-1:]
            breakpoint()
            cursor.execute(query, eval(data))
            print("New Row Inserted")
            conn.commit()

            # after inserting data of first row, deletes first row values
            if len(values) > 161:
                del values[:160]

        return


    # First transform our excel sheet, then delete the columns,rows which are not important, renames columnns
    # to month,year, removes null/empty columns from our data frame
    def pre_processing(self, df, file_name):
        df = df.transpose()
        del df[0]
        del df[1]
        del df[2]
        df.drop(df.index[0], inplace=True)
        df.drop(df.index[1:9], inplace=True)
        df = df.rename(columns=df.iloc[0])
        df.drop(df.index[0], inplace=True)
        df = df.loc[:, df.columns.notnull()]

        # deletes the given columns
        del df['Balance Sheet']
        del df['Supplemental']
        del df['Cash Flow']
        del df['Operating Activities']
        del df['Differnce from Previous Quarter']
        del df['Investing Activities']
        del df['Financing Activities']
        del df['TTM Cap Ex actual']

        # select the rows ending with month and year, other rows are ignored
        df_new = df[(df.index.str.contains('16')) & ~(df.index.str.contains('Unnamed')) |
                    (df.index.str.contains('17')) & ~(df.index.str.contains('Unnamed')) |
                    (df.index.str.contains('18')) & ~(df.index.str.contains('Unnamed')) |
                    (df.index.str.contains('19')) & ~(df.index.str.contains('Unnamed')) |
                    (df.index.str.contains('20')) & ~(df.index.str.contains('Unnamed')) |
                    (df.index.str.contains('21')) & ~(df.index.str.contains('Unnamed')) |
                    (df.index.str.contains('22')) & ~(df.index.str.contains('Unnamed')) |
                    (df.index.str.contains('23')) & ~(df.index.str.contains('Unnamed')) |
                    (df.index.str.contains('24')) & ~(df.index.str.contains('Unnamed')) |
                    (df.index.str.contains('-')) & ~(df.index.str.contains('<-Insert Column'))]
        df_new = df_new.replace('-', -9999)
        df_new = df_new.fillna(-9999)
        df = df_new

        # renames rows to its actual values
        for num, rowNames in enumerate(df.index.values):
            if rowNames.endswith('.1'):
                df.index.values[num] = rowNames[:-2]

        #selects only the columns required for our script
        if 'Healthcare' in file_name:
            df1 = df[db_bridge_helpers.excel_columns_healthcare]
        else:
            df1 = df[db_bridge_helpers.excel_columns]
        
        # returns dataframe after whole processing is done
        return df1


    # This funtion is called when we need to compare excel sheet and database columns. It selects months and year
    # from database and appends to to a single variable to get month year
    def getDatesFromDatabase(self, data_from_database, get_ticker_name, excel_record, com_id):
        try:
            month = list(data_from_database[4])
            year = list(data_from_database[5])
        except:
            return

        date = []
        for index in range(len(month)):
            date.append(month[index] + year[index])

        database_row_names = []
        for names in date:
            database_row_names.append(" ".join(names.split()))

        return database_row_names


    # This function is called to insert new values from excel into database when new rows are detected in excel sheet
    # which were previously not existing in database
    def insertRowsIfNotFound(self, database_row_names, excel_record, index3, com_id):
        
        check_database_row = pd.DataFrame(data=database_row_names)
        if check_database_row[0].str.contains('-').any() == True:

            values = []
            for names in excel_record.iloc[index3]:
                values.append(names)

            month = '-'
            year = '-'
            my = excel_record.index[index3].split()

            dateTime = dt.now()

            query = db_bridge_helpers.query2            
            
            data_builder = "(my[0],my[1],dateTime,"

            for loop in range(len(values)):
                data_builder += 'values[%s]'%loop + ","

            data_builder += 'com_id,month,year)'
            data = data_builder
            breakpoint()
            cursor.execute(query, eval(data))
            print("Dash row updated with month and year name")
            conn.commit()

        else:
            values = []
            for names in excel_record.iloc[index3]:
                values.append(names)

            if '-' in excel_record.index[index3]:
                my = ['-', '-']
            else:
                my = excel_record.index[index3].split()

            is_active = True
            most_recent = False

            # gets current datetime
            dateTime = dt.now()

            # below 4 lines are basic sql queries which are then executed.            
            query = db_bridge_helpers.query3
            
            data_builder = "(com_id,is_active,most_recent,my[0],my[1],dateTime,"
            for loop in range(len(values)):
                data_builder +=  'values[%s]'%loop + "," 
    
            data_builder += ')'   
            data = data_builder[:-2] + data_builder[-1:]
    
            breakpoint()
            cursor.execute(query, eval(data))
            print("Dash row Inserted")
            conn.commit()


    #T This function call other functions
    def execute(self,path,Excel_Files_Names):
        userComments = []

        # appends name of file and destination of source path
        excel_files = []
        for files in range(len(Excel_Files_Names)):
            path_of_file = os.path.join(path, Excel_Files_Names[files])
            excel_files.append(path_of_file)

        # opens file one by one in loop
        for index in range(len(Excel_Files_Names)):
            print("\nOpening file: ", Excel_Files_Names[index], "\n")
            # on demand argument means to only get the sheets name and do not load whole document
            xls = pd.ExcelFile(excel_files[index], on_demand=True)
            sheets = xls.sheet_names
            print("Sheets Found: ", sheets, "\n")

            # ignores these files
            for ids, names in enumerate(sheets):
                exists = False
                
                # opens the file in python
                try:
                    # reads excel sheet one by one
                    excel_record = xls.parse(sheets[ids], skiprows=9)

                    # passes that excel sheet to our funtion to clean the data
                    excel_record = ExcelToPostgres.pre_processing(self, excel_record, Excel_Files_Names[index])

                    # file is again called but without skipping any rows to get company name from first column in excel sheet
                    getCompanyName = xls.parse(sheets[ids], header=None)
                except KeyError:
                    continue
                else:
                    # after getting company name, stores in in variable 'name_of_company'
                    name_of_company = getCompanyName[1].iloc[0]

                    if pd.isna(name_of_company) == True:
                        name_of_company = ''
                        
                    get_ticker_name = getCompanyName.iloc[7][2]
                    print("---------------------------------------")

                    # prints name of company on screen
                    print("Company Name: ", name_of_company)
                    print("Ticker ID: ", get_ticker_name)

                    # runs query to get all company names in database and stores it in panda dataframe
                    query = "select ticker_id from company;"
                    cursor.execute(query)
                    fetch_ticker_names_database = cursor.fetchall()
                    company_names_database_record = pd.DataFrame(data=fetch_ticker_names_database)
                    exists = False
                    if len(company_names_database_record):
                        for index1, names in enumerate(company_names_database_record[0]):
                            if str(names).strip().lower() == str(get_ticker_name).strip().lower():
                                exists = True
                                com_id = index1 + 1
                                break

                            # if it doesnt exsits this part will run
                    if exists == False:
                        # inserts company name in database; company table
                        message = ("Ticker ID {} Not Found...Please Insert into Database Record").format(get_ticker_name)
                        print(message)
                        # data = {
                        #             'message': message
                        #         }
                        # return data
                        continue


                    # if company name exists in database this part will run
                    else:
                        print("Company exists in database")
                        print("company id in database = ", com_id)

                        # this is a basic sql query that fetches all data from database according to given condition
                        query = "select * from fund where co_id = '%s' and is_active = true order by id asc;"
                        data = [com_id]
                        cursor.execute(query, data)
                        fetch_data = cursor.fetchall()

                        # converts data into a dataframe
                        data_from_database = pd.DataFrame(data=fetch_data)

                        # converts data into dataframe
                        data_from_database_timeperiod = pd.DataFrame(data=fetch_data)

                        # this function is called to get all months, year from database for corresponding company
                        database_row_names = ExcelToPostgres.getDatesFromDatabase(self, data_from_database, get_ticker_name,
                                                                                excel_record, com_id)

                        # converts the results to dataframe again
                        database_row_name = pd.DataFrame(data=database_row_names)
                        data_from_database.drop(data_from_database.columns[0:8], axis=1, inplace=True)

                        # checks whether the excel row also exists in database and stores boolean result into variable row_exists
                        row_exists = []
                        for index2 in range(len(excel_record.index)):
                            try:
                                row_exists.append(database_row_name[0].str.contains(excel_record.index[index2].replace(" ","")))
                            except:
                                ExcelToPostgres.insertNewDataAfterCompany(self, get_ticker_name, excel_record, com_id)
                                break
                        
                        # the row exists in database or not
                        for index3, names in enumerate(row_exists):
                            
                            # if row exists this part will run
                            if row_exists[index3].any() == True:
                                # gets row no in database for matching row in excel
                                row_index = np.where(list(row_exists[index3]))[0]
                                print(excel_record.index[row_index][0], " exists in DB and Excel on Row no: ",int(row_index[0]))

                                b = excel_record.index[row_index]
                                try:
                                    database_location = np.where(database_row_name[0].str.contains(b[0].replace(" ","")))[0]
                                    database_location = int(database_location)
                                except:
                                    pass

                                # stores excel sheet single row in database to be compared with database values
                                a = excel_record.iloc[row_index]
                                counter = 0
                                for excel_value,dbase_value in zip(a.iloc[0], data_from_database.iloc[database_location]):

                                    # if values are not matching it means file has been updated
                                    counter = counter + 1
                                    
                                    if float(excel_value) != float(dbase_value):
                                        
                                        print("\nRow is:", b[0])
                                        print("Excel: ", float(excel_value), " Database: ", float(dbase_value), " location: ", counter)
                                       
                                        # checks timedelta between excel rows and database rows to get when was the row last updated and converts it to no. of days
                                        currentTime = dt.now()
                                        preUpdateTime = data_from_database_timeperiod[[6]].iloc[int(row_index)]
                                        time_difference = currentTime - preUpdateTime
                                        time_difference_in_days = time_difference / timedelta(days=1)
                                        for a in time_difference_in_days:
                                            timediff = a
                                        print("Time Difference = ", int(timediff), "days")

                                        # gets current time
                                        dateTime = dt.now()

                                        # splits month,year into array
                                        f = b[0].split()

                                        # splits row values into single array
                                        values = []
                                        for names in excel_record.iloc[int(row_index)]:
                                            values.append(names)

                                        # checks if time difference for excel and database is greater than 10
                                        if timediff > 10:
                                            print("\nAppending to row beacause time diff is: ", timediff)
                                            userComments.append({
                                                'excel_files': excel_files[index],
                                                'sheet_name': sheets[ids],
                                                'company_name': name_of_company,
                                                'ticker_name': get_ticker_name,
                                                'old_value': float(dbase_value),
                                                'new_value': float(excel_value),
                                                'time_difference': int(timediff),
                                                'location': counter,
                                                'co_id': com_id,
                                                'period_ending_month': f[0],
                                                'period_ending_year': f[1],
                                                'dateTime': dateTime,
                                                'comments': "",
                                                'values': values
                                                })

                                        # if time difference is less than 10
                                        else:
                                            # will update database row with new values from excel sheet for matching month year in database,excel
                                            query = db_bridge_helpers.query5
                                            
                                            data_builder = "(dateTime,"

                                            for loop in range(len(values)):
                                                data_builder += 'values[%s]'%loop + ","
                                            
                                            data_builder += 'com_id,f[0],f[1])'
                                            data = data_builder
                                            # prints that row is updated with new data on users screen
                                            cursor.execute(query, eval(data))
                                            conn.commit()
                                            print("Row Updated with New Data")
                                            print("-------------------------")

                                        # once it finds that values are changed it will not further check for dissimiliar values nd update or insert new rows and break the loop
                                        break
                                    
                            # if row doesnt exits this part will run which calls a funtion which inserts values into database
                            else:
                                ExcelToPostgres.insertRowsIfNotFound(self, database_row_names, excel_record, index3, com_id)

                        # after checking all rows this will be the last part of our srcipt. It chekcs which is the most recent row in our database and mark most_recent column as true
                        if excel_record.index.str.contains('-').any() == True:
                            monthYear = excel_record.index[len(excel_record) - 2]
                        else:
                            monthYear = excel_record.index[len(excel_record) - 1]

                        monthYear = monthYear.split()
                        most_recent_month = monthYear[0]
                        most_recent_year = monthYear[1]

                        # after finding most recent row in our database from excel sheet updates the other rows to false in database
                        boolean = True
                        query = "update fund set most_recent = False where co_id= '%s' and is_active = %s;"
                        data = (com_id, boolean)
                        cursor.execute(query, data)
                        conn.commit()

                        # after finding most recent row in our database from excel sheet updates the corresponding row to true in database
                        query = "update fund \
                                set most_recent=True \
                                where co_id= '%s' and period_ending_month = %s and period_ending_year = %s and is_active = True;"
                        data = (com_id, most_recent_month, most_recent_year)
                        cursor.execute(query, data)
                        conn.commit()

                        # prints on users screen
                        print("Most Recent Row updated to True")

                    
        if len(userComments) == 0:
            message = "\n\nHooray...Sheets Inserted/Updated Successfully."
            print(message)
            data = {
                    'message': message
                    }
            return data 
        else:
            message = "\n\nPlease add the comments to complete transactions"
            data =  {
                    'message': message,
                    'data': userComments
                    }
            return data

    
# Main line of our file which starts whole script
def execute(excel_file_names):
    data = ExcelToPostgres().execute(db_bridge_helpers.path, excel_file_names)
    return data


def updateConflictedRows(data):
    updateRows = data
    for items in updateRows:

        #if user has provided comments so row will be updated otherwise row won`t be updated
        if items['comments']:
            # updates previous row already in database with comment
            query = "Update fund\
                        set is_active=false, most_recent=false, comments = %s \
                        where co_id = '%s' and period_ending_month = %s and period_ending_year = %s and is_active = true;"
            data = (items['comments'], int(items['co_id']), items['period_ending_month'], items['period_ending_year'])
            cursor.execute(query, data)
            conn.commit()
            print("Updated to False")

            # inserts new row with latest timestamp and new data
            is_active = True
            most_recent = False

            query = db_bridge_helpers.query4
            
            data_builder = "(items['co_id'],is_active,most_recent,items['period_ending_month'],items['period_ending_year'],items['dateTime'],"
            for loop in range(len(items['values'])):
                data_builder +=  "items['values'][%s]"%loop + "," 

            data_builder += ')'   

            data = data_builder[:-2] + data_builder[-1:]

            cursor.execute(query, eval(data))
            print("New Row Inserted")
            print("----------------")
            conn.commit()
    
    message = "All Corresponding Rows Have Been Updated"
    return message


def updateCompanies():
    file_dir = os.path.join(db_bridge_helpers.path,'companies.xlsx')
    df = pd.read_excel(file_dir)
    df.columns = ['sector','ticker_id','name','active']
    query = "INSERT INTO public.""company""(sector,ticker_id,name,active) Values (%s,%s,%s,%s)"
    for row in df.itertuples():
        data = (row[1],row[2],row[3],row[4])
        cursor.execute(query,data)
        conn.commit()
    message = "Companies Updated"
    return message
    
# <---------------------------------------------------------------end of script--------------------------------------------------------------- #
