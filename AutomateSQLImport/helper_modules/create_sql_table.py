from helper_modules.sql_query import createTableQueryString,insertValuesQueryString
from helper_modules.dataframe import getSQLTableStructure
from helper_modules.dataframe import get_csv_dataframe
import pandas as pd
import numpy as np
import chardet
import re
import pyodbc
import numpy as np
import configparser
from pathlib import Path

# ==========================================================
# Convert date dataframe columns to string 
# ==========================================================
def convert_datecol_to_string(df_obj):
    for column_name in df_obj.select_dtypes('datetime').columns:
        df_obj[column_name] = df_obj[column_name].astype('str')
    return df_obj

def connect_to_db(config_file):

    # read db_config.ini
    db_config = configparser.ConfigParser(interpolation=None)
    db_config.read(f'./config/{config_file}.ini')

    ######################################################### 
    # Connect to Microsoft SQL Server
    ######################################################## 

    db_name = db_config['DB_CONFIG']['db_name']
    db_schema = db_config['DB_CONFIG']['db_schema'] 
    server_name = db_config['DB_CONFIG']['server_name'] 
    trusted_connection = db_config['DB_CONFIG']['windows_authentication'] 

    if trusted_connection == 'yes':
        connection_string = (fr'''Driver={{SQL Server}};
                                Server={server_name};
                                Database={db_name};
                                Trusted_Connection={trusted_connection};''')
    else:
        user_name = db_config['DB_CONFIG']['user_name']
        password = db_config['DB_CONFIG']['password']

        connection_string = (fr'''Driver={{SQL Server}};
                                Server={server_name};
                                Database={db_name};
                                UID={user_name};
                                PWD={password}''')
    
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.fast_executemany = True
    return db_name,db_schema,conn,cursor

def sql_table_exists(config_file,sqlTableName):
    *_,cursor = connect_to_db(config_file) 
    if cursor.tables(table=sqlTableName,tableType = 'TABLE').fetchone() is None:
        return False
    else:
        return True

def createSQLTable(dataframeObject,sqlTableName,config_file):

    sql_table_creation_log = {
        'sql_error_category':None,
        'sql_error_message':None,
        'sql_table_name':None
    }

    db_name,db_schema,conn,cursor = connect_to_db(config_file)

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

    excelFile = pd.ExcelFile(excel_file_path)

    # create a list of dictionaries
    list_of_excel_log = []

    for sheetName in excelFile.sheet_names:
        sql_sheet_name= re.sub('_{2,}','_',re.sub('\s+|-+','_',sheetName))
        sql_sheet_name= re.sub('\(|\)','',sql_sheet_name)
        sqlTableName = root_dir_name + '_' + fileName + '_' + sql_sheet_name

        if sql_table_exists(config_file,sqlTableName):
            list_of_excel_log.append(None)
        else:
            excel_table_creation_log = {
                'excel_error_category':None,
                'excel_error_message':None ,
                'file_name':f'{fileName}.xlsx',
                'file_path':excel_file_path,
                'root_dir_name':root_dir_name,
                'sheet_name':None
            }

            dataframeObject = excelFile.parse(sheet_name=sheetName)
            dataframeObject = convert_datecol_to_string(dataframeObject)

            excel_table_creation_log['sheet_name'] = sheetName

            if not dataframeObject.empty:
                sql_table_creation_log = createSQLTable(dataframeObject,sqlTableName,config_file)
                excel_table_creation_log.update(sql_table_creation_log)
                list_of_excel_log.append(excel_table_creation_log)

    return list_of_excel_log 



# ===========================================================
# Generate SQL Server Table from a CSV file
# =========================================================
def create_table_from_csv(csv_file_path,root_dir_name,config_file,scanFolder=False):

    fileName = re.sub('_{2,}','_',re.sub('\s+|-+','_',Path(csv_file_path).stem))
    sqlTableName = root_dir_name + '_' + fileName 

    if sql_table_exists(config_file,sqlTableName):
        return None
    else:
        # create a dictionary to keep track of success and errors
        csv_table_creation_log = {
            'csv_error_category':None,
            'csv_error_message':None ,
            'file_name':f'{fileName}.csv',
            'file_path':csv_file_path,
            'root_dir_name':root_dir_name,
        }

        output = get_csv_dataframe(csv_file_path)
        if isinstance(output,pd.DataFrame):
            dataframeObject = output
            sql_table_creation_log = createSQLTable(dataframeObject,sqlTableName,config_file) 
            csv_table_creation_log.update(sql_table_creation_log)
        elif isinstance(output,dict): 
            csv_table_creation_log.update(output)
            
        return csv_table_creation_log

        

