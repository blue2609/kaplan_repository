# from typing_extensions import Required
from helper_modules.create_sql_table import create_table_from_csv
from helper_modules.create_sql_table import create_table_from_excel
from helper_modules.dataframe import get_csv_dataframe
from pprint import pprint
import re
import argparse
from csv import DictWriter 
import os

def parse_arguments():
    # parse the arguments from command line
    parser = argparse.ArgumentParser()

    # parser.add_argument('--folderPath',required=True,help='specify subject absolute folder path in which excel/CSV files are located in')
    parser.add_argument('--folderPath',help='specify subject absolute folder path in which excel/CSV files are located in')
    parser.add_argument('--filePath',help='specify the file that should be imported to SQL Server Table')
    parser.add_argument('--scanFolder',help='should be executed first before even trying to import CSV files into SQL Server Database. This flag is used to scan all CSV files (but not Excel files for now) and detect any possible error when reading them using Python Pandas library',action='store_true')
    parser.add_argument('--configFile',help="Pass the name of the ini file (without the <.ini>) which contains the settings for SQL server database the script must connect to")
    return parser.parse_args()

def main():

    args = parse_arguments()

    # create output table creation log if it doesn't exist
    log_file_columns = [
                            'sql_error_category',
                            'sql_error_message',
                            'sql_table_name',
                            'excel_error_category',
                            'excel_error_message',
                            'csv_error_category',
                            'csv_error_message',
                            'file_name',
                            'file_path',
                            'root_dir_name',
                            'sheet_name',
                        ]


    # Create table_creation_log.csv if it doesn't exist
    if not os.path.exists('table_creation_log.csv'):
        with open('table_creation_log.csv','w',newline='') as table_creation_log:
            dict_writer_obj = DictWriter(table_creation_log,log_file_columns)
            dict_writer_obj.writeheader()

    table_creation_log = open('table_creation_log.csv','a',newline='')
    dict_writer_obj = DictWriter(table_creation_log,log_file_columns)
    
    if args.filePath and os.path.exists(args.filePath):

        subjectName = os.path.basename(os.path.dirname(args.filePath))
        subjectName = re.sub('\s+','',subjectName).upper()

        if re.search('\.xlsx$|\.xls$',args.filePath):
            excel_creation_log_list = create_table_from_excel(args.filePath,subjectName,args.configFile)
            for excel_creation_log in excel_creation_log_list:
                if excel_creation_log:
                    dict_writer_obj.writerow(excel_creation_log)

        # -- if the file is a csv file, execute this code block below
        if re.search('\.csv$',args.filePath):
            csv_creation_log = create_table_from_csv(args.filePath,subjectName,args.configFile)
            if csv_creation_log:
                dict_writer_obj.writerow(csv_creation_log)
                
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
                                # table_creation_log_dict = create_table_from_csv(filePath,subjectName,args.configFile,scanFolder=True)
                                table_creation_log_dict = get_csv_dataframe(filePath,return_dataframe_object=False)
                                if table_creation_log_dict:
                                    table_creation_log_dict['filePath'] = filePath
                                    pprint(table_creation_log_dict)

                        else:
                            #  -- if the file is an excel file, execute this code block below -- 
                            if re.search('\.xlsx$|\.xls$',fileName):
                                filePath = os.path.join(currentPath,fileName)
                                excel_creation_log_list = create_table_from_excel(filePath,subjectName,args.configFile)
                                for excel_creation_log in excel_creation_log_list:
                                    if excel_creation_log:
                                        dict_writer_obj.writerow(excel_creation_log)
                            
                            # -- if the file is a csv file, execute this code block below
                            if re.search('\.csv$',fileName):
                                filePath = os.path.join(currentPath,fileName)
                                csv_creation_log = create_table_from_csv(filePath,subjectName,args.configFile)
                                if csv_creation_log:
                                    dict_writer_obj.writerow(csv_creation_log)
                            
        else:
            print("The directory doesn't exist or the path specified is not a directory")
            exit()
        
    table_creation_log.close()


if __name__ == '__main__':
    main()
