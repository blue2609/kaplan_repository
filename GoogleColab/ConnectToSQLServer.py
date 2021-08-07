%%capture

# ------------------------------------------------
# Install Microsoft SQL Server ODBC Driver 2017
# ------------------------------------------------
!curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
!curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
!sudo apt-get update
!sudo ACCEPT_EULA=Y apt-get -q -y install msodbcsql17

!sudo apt-get install unixodbc-dev
!pip install pyodbc

# --------------------------------------------------------
# Import the SQL Server data to the 'df' pandas dataframe 
# --------------------------------------------------------
import pyodbc 
import pandas as pd

# ------------------------------------------------------------
# ------ HOW DO WE MANAGE THIS CREDENTIAL -------------------
# ------------------------------------------------------------

server= SERVER_ENDPOINT
database= DB_NAME
username='admin'
password= DB_PASSWORD

# Create Connection
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

tableName = 'some_tableName' 
sqlString = f'''
SELECT * FROM [dbo].[{tableName}]
'''
# cursor.execute(''' 
# SELECT * FROM [dbo].[tableName];
# ''')

# for row in cursor.fetchall():            
#     print(row)

# cursor.close()
df = pd.read_sql(sqlString,cnxn)
cnxn.close(