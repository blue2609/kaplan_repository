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


