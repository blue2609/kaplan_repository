# from typing_extensions import Required
import pandas as pd
import numpy as np
import chardet
# import subprocess
import re
import pyodbc
from collections import namedtuple
import numpy as np
import argparse
from pathlib import Path
import os

#================================================
# Function Definitions
#================================================

'''  **********************************************************************
 Function to find out data type of a dataframe column (Pandas Series Object) 
**********************************************************************'''

def findDataType(dataFrameColumn):
    try:
        column = pd.to_numeric(dataFrameColumn)
        dataType=column.dtype.name
    except:
        column = dataFrameColumn.astype('str')
        # dataType = column.dtype.name
        dataType ='string' 

        # try:
        #     column = pd.to_datetime(dataFrameColumn)
        #     dataType='datetime'
        # except:
        #     # column = dataFrameColumn.astype('string')
        #     # dataType = column.dtype.name
        #     column = dataFrameColumn.astype('str')
        #     dataType = 'string' 
        # else:
        #     if (column.dt.floor('d') == column).all():
        #         dataType = 'date'
        #     elif (column.dt.date == pd.Timestamp('now')).all():
        #         dataType = 'time'
        #     else:
        #         # dataType=column.dtype.name
        #         dataType='string'
    finally:
        return dataType


# ******************************************************************
# Function to convert the dataframe data types to SQL Data Types 
# ********************************************************************

def getSQLTableStructure(dataframe):
    sqlTableStructure = {}
    sqlColumn = namedtuple('sqlColumn',[
         'sqlDataType',
         'noOfNulls',
         'allowNull'
    ])

    dataFrameStructure = getDataframeStructure(dataframe)
    for columnName,namedTupleObj in dataFrameStructure.items():

        #-----------------------------------------------------
        # Parse integer to its corresponding data type in SQL
        #-----------------------------------------------------
        if 'int' in namedTupleObj.dataType:  

            #get the number of bits used 
            no_of_bits = re.search('\d+',namedTupleObj.dataType).group()

            if no_of_bits == '32':
                sqlDataType = 'int'
            elif no_of_bits == '64':
                sqlDataType = 'bigint'
            elif no_of_bits == '16':
                sqlDataType = 'smallint'
            elif no_of_bits == '8':
                sqlDataType = 'tinyint'

        elif 'float' in namedTupleObj.dataType:

            sqlDataType = 'float'

        elif 'date' == namedTupleObj.dataType:

            sqlDataType = 'date'

        elif 'time' == namedTupleObj.dataType:

            sqlDataType = 'time'

        elif 'datetime' in namedTupleObj.dataType:

            sqlDataType = 'datetime'

        elif 'string' == namedTupleObj.dataType:

            # get the max number of bytes required for this column
            max_col_size = dataframe[columnName].apply(
                                    lambda eachValue: len(str(eachValue).encode('UTF-8'))
                                ).max()

            # check if all rows in the column are of the same string length 
            all_column_same_size = dataframe[columnName].apply(
                                            lambda eachValue: len(str(eachValue).encode('UTF-8')) == max_col_size
                                        ).all()

            
            if all_column_same_size:
                sqlDataType = f'char({max_col_size})'
            else:
                max_col_size = ((max_col_size * 2) + 9) // 10 * 10
                sqlDataType = f'varchar({max_col_size})'

            # need more functionality here to detect fixed string column

        # add a new sqlColumn to sqlTableStructure dictionary
        # based on the converted data type
        sqlTableStructure[columnName] = sqlColumn(sqlDataType=sqlDataType,
                                                  noOfNulls=namedTupleObj.noEmptyCells,
                                                  allowNull=namedTupleObj.allowNull)
    
    return (sqlTableStructure,dataFrameStructure)


# ****** 
# Get Data type for each column of pandas dataframe
#  ******

def getDataframeStructure(dataframe):
    sql_table_structure = {}
    sqlColumn = namedtuple('sqlColumn',[
        'dataType',
        'noEmptyCells',
        'allowNull' 
    ])

    for columnName in dataframe.columns:

        column = dataframe[columnName]

        # Get the row indexes which contain empty value/empty string or None/Null
        empty_cells_indexes = column[(column.isna()) | 
                                     (column == '') |
                                     (column == np.inf) |
                                     (column.astype(str).str.isspace())].index
        
        # assign 'NULL' string to column values that are either:
        # - a 'None'
        # - an empty string ''
        # - just a string that contains whitespaces '    '
        # - 'inf' which indicates positive or negative infinite (usually float) value
        dataframe[columnName][empty_cells_indexes] = 'NULL' 

        allowNull = '' if empty_cells_indexes.size > 0 else 'NOT NULL' 

        # drop the empty_cells_indexes from the column (if there's any)
        cleaned_column = column.drop(labels=empty_cells_indexes)

        # ----------------------------------------------------- 
        # make a best guess what the data type of the column is 
        # ----------------------------------------------------- 

        sql_table_structure[columnName] = sqlColumn(dataType=findDataType(cleaned_column),
                                                    noEmptyCells=empty_cells_indexes.size,
                                                    allowNull=allowNull)
        
    # return a dictionary containing the implied basic SQL Table Structure
    return sql_table_structure


# ===========================================================
# Generate the SQL String which will create a table
# =========================================================

def createTableQueryString(dbName,schema,tableName,sqlTableStructure):
    queryString = f'CREATE TABLE {dbName}.{schema}.{tableName}('
    
    for columnName,sqlColumn in sqlTableStructure.items():
        queryString += f'\n"{columnName}" {sqlColumn.sqlDataType} {sqlColumn.allowNull},'
    
    queryString += ');'
    return queryString


# ===========================================================
# Generate SQL query to insert values into database talbe
# =========================================================

def insertValuesQueryString(dbName,schema,tableName,dataframe):
    
    # get a list of columnNames from dataframe
    columnNamesList = ','.join([f'"{columnName}"' for columnName in dataframe.columns]) 
    queryString = f'INSERT INTO {dbName}.{schema}.{tableName} ({columnNamesList}) \n SELECT * FROM (VALUES \n' 
    
    for index,*values in dataframe.itertuples():
        if index == dataframe.index[-1]:
            queryString += '(' + ','.join(["'" + str(value).replace("'","''") + "'" 
                                           if str(value) != 'NULL' else 'NULL'
                                           for value in values]) + f')\n)AS temp ({columnNamesList});'
        else:
            queryString += '(' + ','.join(["'" + str(value).replace("'","''") + "'"
                                           if str(value) != 'NULL' else 'NULL' 
                                           for value in values]) + '),\n'
    return queryString

def createSQLTable(dataframeObject,sqlTableName):

    ######################################################### 
    # Connect to Microsoft SQL Server
    ######################################################## 

    dbName = 'MBAN'
    schema = 'dbo'
    conn = pyodbc.connect(f'''Driver={{SQL Server}};
                            Server=KA-PF14P8C2\SQLEXPRESS;
                            Database={dbName};
                            Trusted_Connection=yes;''')
    cursor = conn.cursor()
    cursor.fast_executemany = True

    # only create the table if there is no table with the same name in the database
    if cursor.tables(table=sqlTableName,tableType = 'TABLE').fetchone() is None:


    # print(getSQLTableStructure(dataframeObject))

    # -- Create the table -- 
    # createTableString = createTableQueryString(dbName,schema,tableName,getSQLTableStructure(dataframeObject)[0])
        createTableString = createTableQueryString(dbName,schema,sqlTableName,getSQLTableStructure(dataframeObject)[0])
        # print(createTableString)
        try:
            cursor.execute(createTableString)
            cursor.commit()
        except pyodbc.ProgrammingError as pyodbcProgrammingError:
            print(f'Table Creation Error: {sqlTableName}')
            print(pyodbcProgrammingError)
            cursor.close()
            conn.close()
            return
        # create a list of dataframes in chunks
        no_of_split = int(np.ceil(dataframeObject.shape[0]/ 500))
        dataframe_chunks = np.array_split(dataframeObject,no_of_split)


        for index,each_dataframe in enumerate(dataframe_chunks):
            # insertValueString = insertValuesQueryString(dbName,schema,tableName,each_dataframe)
            insertValueString = insertValuesQueryString(dbName,schema,sqlTableName,each_dataframe)

            try:
                cursor.execute(insertValueString)
                cursor.commit()
            except pyodbc.ProgrammingError as pyodbcProgrammingError:
                print(f'Table Inserting Value Error: {sqlTableName}')
                print(pyodbcProgrammingError)
                cursor.close()
                conn.close()
                return

    cursor.close()
    conn.close()

# ===========================================================
# Generate SQL Server Table from an excel file
# =========================================================
def create_table_from_excel(excel_file_path,root_dir_name,fileName):
    excelFile = pd.ExcelFile(excel_file_path)
    for sheetName in excelFile.sheet_names:

        dataframeObject = excelFile.parse(sheet_name=sheetName)
        if not dataframeObject.empty:
            sheetName = re.sub('_{2,}','_',re.sub('\s+|-+','_',sheetName))
            sheetName = re.sub('\(|\)','',sheetName)
            fileName = Path(re.sub('_{2,}','_',re.sub('\s+|-+','_',excel_file_path))).stem.upper()
            sqlTableName = root_dir_name + '_' + fileName + '_' + sheetName

            createSQLTable(dataframeObject,sqlTableName)

def create_table_from_csv(csv_file_path,root_dir_name,fileName,scanFolder=False):

    # read the first 100KB of the file to 
    # detect the encoding of the file 
    with open(csv_file_path,'rb') as file:
        detectedEncoding = chardet.detect(file.read(100000))['encoding']

    try:
        dataframeObject = pd.read_csv(csv_file_path,encoding=detectedEncoding)

    # =======================================
    # print errors and do return the function
    # =======================================
    except pd.io.common.ParserError as dfStructureError:
        print(f'{csv_file_path} has error in its table structure')
        print(str(dfStructureError))
        return
        
    except UnicodeDecodeError as encodingError:
        print(f'{csv_file_path} has error in encoding')
        print(encodingError)
        return

    except pd.io.common.EmptyDataError:
        print(f'{csv_file_path} is empty')
        return
        
    # in case where scanFolder == True, don't create a SQL Table
    if scanFolder == False:
        fileName = re.sub('_{2,}','_',re.sub('\s+|-+','_',Path(csv_file_path).stem))
        sqlTableName = root_dir_name + '_' + fileName 

        createSQLTable(dataframeObject,sqlTableName) 

#================================================
# CREATING A TEST Dataframe
#================================================

# test_df = pd.DataFrame({'Column_1':['Stanley','Leonhard','Setiawan',None],
#                         'Column_2':['22','This is it','random',None],
#                         'Column_3':['11/22/2017','12/20/2018','09/05/2020',None],
#                         'Column_4':['10/27/2015','12/15/2016','10/31/2015',None]})

# test_df['Column_5'] = pd.Series(['Jan','Feb','Mar',None])
# test_df['Column_6'] = pd.Series(['January','February','March',None])
# test_df['Column_7'] = [22,None,'',None]
# test_df['Column_8'] = [3.5,0.05,999.4,None]
# test_df['Column_9'] = ['15:00','03:00','09:00',None]
# test_df['Column_10'] = ['   ',' stanley this ',' ',"\n \t some'String"] 



# --------------------------------
# main part of the program
# --------------------------------

def main():
    # parse the arguments from command line
    parser = argparse.ArgumentParser()
    # parser.add_argument('--folderPath',required=True,help='specify subject absolute folder path in which excel/CSV files are located in')
    parser.add_argument('--folderPath',help='specify subject absolute folder path in which excel/CSV files are located in')
    parser.add_argument('--filePath',help='specify the file that should be imported to SQL Server Table')
    parser.add_argument('--scanFolder',help='should be executed first before even trying to import CSV files into SQL Server Database. This flag is used to scan all CSV files (but not Excel files for now) and detect any possible error when reading them using Python Pandas library',action='store_true')
    args = parser.parse_args()

    if args.filePath:
        if os.path.exists(args.filePath):

            subjectName = os.path.basename(os.path.dirname(args.filePath))
            subjectName = re.sub('\s+','',subjectName).upper()

            if re.search('\.xlsx$|\.xls$',args.filePath):
                create_table_from_excel(args.filePath,subjectName)

            # -- if the file is a csv file, execute this code block below
            if re.search('\.csv$',args.filePath):
                create_table_from_csv(args.filePath,subjectName)
                
    else:
        if os.path.exists(args.folderPath) and os.path.isdir(args.folderPath):
            subjectName = os.path.basename(os.path.normpath(args.folderPath))
            subjectName = re.sub('\s+','',subjectName).upper()

            # iterate through the directory recursively (includes sub-directory)
            for currentPath,dir_list,file_list in os.walk(args.folderPath):
                if '__MACOSX' not in currentPath:
                    for fileName in file_list:
                        # check if fileName ends in either:
                        # - .xlsx
                        # - .xls
                        # - .csv
                        # Basically we only want to detect excel and csv files

                        if args.scanFolder:
                            if re.search('\.csv$',fileName):
                                filePath = os.path.join(currentPath,fileName)
                                create_table_from_csv(filePath,subjectName,fileName,scanFolder=True)

                        else:
                            #  -- if the file is an excel file, execute this code block below -- 
                            if re.search('\.xlsx$|\.xls$',fileName):
                                filePath = os.path.join(currentPath,fileName)
                                create_table_from_excel(filePath,subjectName,fileName)
                            
                            # -- if the file is a csv file, execute this code block below
                            if re.search('\.csv$',fileName):
                                filePath = os.path.join(currentPath,fileName)
                                create_table_from_csv(filePath,subjectName,fileName)
        else:
            print("The directory doesn't exist or the path specified is not a directory")
            exit()

if __name__ == '__main__':
    main()
