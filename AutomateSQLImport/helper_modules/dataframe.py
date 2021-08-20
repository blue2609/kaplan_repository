import pandas as pd
import numpy as np
from collections import namedtuple
import numpy as np
import re

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
        # dataframe[columnName][empty_cells_indexes] = 'NULL' 
        dataframe.loc[empty_cells_indexes,columnName] = 'NULL' 

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



# ******************************************************************
# Function to convert he dataframe data types to SQL Data Types 
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