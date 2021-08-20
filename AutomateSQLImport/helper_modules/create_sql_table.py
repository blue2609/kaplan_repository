from helper_modules.sql_query import createTableQueryString,insertValuesQueryString
from helper_modules.dataframe import getSQLTableStructure
import pandas as pd
import numpy as np
import chardet
import re
import pyodbc
import numpy as np
import configparser
from pathlib import Path

def createSQLTable(dataframeObject,sqlTableName,config_file):

    # read db_config.ini
    db_config = configparser.ConfigParser()
    # db_config.read('./config/db_config.ini')
    db_config.read(f'./config/{config_file}.ini')

    sql_table_creation_log = {
        'sql_error_category':None,
        'sql_error_message':None,
        'sql_table_name':None
    }

    ######################################################### 
    # Connect to Microsoft SQL Server
    ######################################################## 

    db_name = db_config['DB_CONFIG']['db_name']
    db_schema = db_config['DB_CONFIG']['db_schema'] 
    server_name = db_config['DB_CONFIG']['server_name'] 
    trusted_connection = db_config['DB_CONFIG']['windows_authentication'] 
    
    conn = pyodbc.connect(fr'''Driver={{SQL Server}};
                            Server={server_name};
                            Database={db_name};
                            Trusted_Connection={trusted_connection};''')
    cursor = conn.cursor()
    cursor.fast_executemany = True

    # only create the table if there is no table with the same name in the database
    if cursor.tables(table=sqlTableName,tableType = 'TABLE').fetchone() is None:



        # -- Create the table -- 
        createTableString = createTableQueryString(db_name,db_schema,sqlTableName,getSQLTableStructure(dataframeObject)[0])
        try:
            cursor.execute(createTableString)
            cursor.commit()

        except pyodbc.ProgrammingError as pyodbcProgrammingError:
            sql_table_creation_log['sql_error_category'] = 'SQL Table Creation'
            sql_table_creation_log['sql_error_message'] = pyodbcProgrammingError
            cursor.close()
            conn.close()
            return sql_table_creation_log

        # create a list of dataframes in chunks
        no_of_split = int(np.ceil(dataframeObject.shape[0]/ 500))
        dataframe_chunks = np.array_split(dataframeObject,no_of_split)


        for index,each_dataframe in enumerate(dataframe_chunks):
            # insertValueString = insertValuesQueryString(db_name,db_schema,tableName,each_dataframe)
            insertValueString = insertValuesQueryString(db_name,db_schema,sqlTableName,each_dataframe)

            try:
                cursor.execute(insertValueString)
                cursor.commit()
            except pyodbc.ProgrammingError as pyodbcProgrammingError:
                sql_table_creation_log['sql_error_category'] = 'SQL Insert Value'
                sql_table_creation_log['sql_error_message'] = pyodbcProgrammingError
                cursor.close()
                conn.close()
                return sql_table_creation_log

    cursor.close()
    conn.close()
    sql_table_creation_log['sql_table_name'] = sqlTableName
    return sql_table_creation_log  # should return None, None if this line is executed

# ===========================================================
# Generate SQL Server Table from an excel file
# =========================================================
def create_table_from_excel(excel_file_path,root_dir_name,config_file):
    fileName = Path(re.sub('_{2,}','_',re.sub('\s+|-+','_',excel_file_path))).stem.upper()

    excel_table_creation_log = {
       'excel_error_category':None,
       'excel_error_message':None ,
       'file_name':f'{fileName}.xlsx',
       'file_path':excel_file_path,
       'root_dir_name':root_dir_name,
       'sheet_name':None
    }
    
    excelFile = pd.ExcelFile(excel_file_path)
    for sheetName in excelFile.sheet_names:

        dataframeObject = excelFile.parse(sheet_name=sheetName)
        sheetName = re.sub('_{2,}','_',re.sub('\s+|-+','_',sheetName))
        sheetName = re.sub('\(|\)','',sheetName)
        excel_table_creation_log['sheet_name'] = sheetName

        if not dataframeObject.empty:

            sqlTableName = root_dir_name + '_' + fileName + '_' + sheetName
            sql_table_creation_log = createSQLTable(dataframeObject,sqlTableName,config_file)
            excel_table_creation_log.update(sql_table_creation_log)

        return excel_table_creation_log

# ===========================================================
# Generate SQL Server Table from a CSV file
# =========================================================
def create_table_from_csv(csv_file_path,root_dir_name,config_file,scanFolder=False):

    fileName = re.sub('_{2,}','_',re.sub('\s+|-+','_',Path(csv_file_path).stem))

    # create a dictionary to keep track of success and errors
    csv_table_creation_log = {
       'csv_error_category':None,
       'csv_error_message':None ,
       'file_name':f'{fileName}.csv',
       'file_path':csv_file_path,
       'root_dir_name':root_dir_name,
    }

    # read the first 100KB of the file to 
    # detect the encoding of the file 
    with open(csv_file_path,'rb') as file:
        detectedEncoding = chardet.detect(file.read(100000))['encoding']

    try:
        dataframeObject = pd.read_csv(csv_file_path,encoding=detectedEncoding)

    # =======================================
    # print errors and do return the function
    # =======================================
    except pd.errors.ParserError as dfStructureError:
        csv_table_creation_log['csv_error_category'] = 'CSV file structure error'
        csv_table_creation_log['csv_error_message'] = dfStructureError
        return csv_table_creation_log
        
    except UnicodeDecodeError as encodingError:
        csv_table_creation_log['csv_error_category'] = 'CSV dataframe encoding error'
        csv_table_creation_log['csv_error_message'] = encodingError
        return csv_table_creation_log

    except pd.errors.EmptyDataError as emptyError:
        csv_table_creation_log['csv_error_category'] = 'CSV file is empty'
        csv_table_creation_log['csv_error_message'] = emptyError
        return csv_table_creation_log
        
    # in case where scanFolder == True, don't create a SQL Table
    if scanFolder == False:

        sqlTableName = root_dir_name + '_' + fileName 
        sql_table_creation_log = createSQLTable(dataframeObject,sqlTableName,config_file) 
        csv_table_creation_log.update(sql_table_creation_log)
        return csv_table_creation_log

        

