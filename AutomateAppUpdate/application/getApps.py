import subprocess
import pandas as pd
from datetime import datetime

'''
This script is used to get a list of all applications installed on Windows Server 
WITHOUT Chocolatey. Not everything can be obtained with Chocolatey. 
'''

def getMBATSApps():
    

def getChocoPkgs():
    chocolateyPackages = [
        'Tableau-Desktop',
        # 'powerbi',
        # 'r.project',
        # 'r.studio',
        # 'rapidminer',
    ]

    

    # csvFileName = 'AllAppsList'
    # csvFilePath = f'./application/{csvFileName}.csv'
    # subprocess.run([r'powershell',r'./application/PowershellScript/getAllAppsInstalled.ps1',csvFilePath],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)

    # appToMonitor = [
    # 'Tableau',
    # 'Spotfire',
    # 'Power',
    # 'Chrome',
    # 'SQL Server Management Studio',
    # 'Office'
    # ]

    # # -------------------------------------------- 
    # # Work with Pandas dataframe from here on 
    # # -------------------------------------------- 

    # appsList_df = pd.read_csv( csvFilePath,
    #                             parse_dates=['InstallDate'],
    #                             date_parser = lambda x: pd.to_datetime(x,format='%Y%m%d',errors='ignore')
    #                         )

    # print(appsList_df.info())


    # # drop all empty rows 
    # appsList_df.dropna(how='all',inplace=True)

    # # drop duplicate rows where all columns have the same value
    # appsList_df.drop_duplicates(keep='first',inplace=True,ignore_index=True)

    # MBATS_apps_df = pd.concat([appsList_df[appsList_df['Name'].str.contains(appName)] 
    #                         for appName in appToMonitor])
    
    # MBATS_apps_df.to_csv('MBATSAppsList.csv',index=False)

    # return MBATS_apps_df 


# if __name__ == '__main__':
#     getMBATSApps()

