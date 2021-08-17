import pandas as pd
import numpy as np


#================================================
# CREATING A TEST Dataframe
#================================================

def create_test_df():
	test_df = pd.DataFrame({'Column_1':['Stanley','Leonhard','Setiawan',None],
				'Column_2':['22','This is it','random',None],
				'Column_3':['11/22/2017','12/20/2018','09/05/2020',None],
				'Column_4':['10/27/2015','12/15/2016','10/31/2015',None]})

	test_df['Column_5'] = pd.Series(['Jan','Feb','Mar',None])
	test_df['Column_6'] = pd.Series(['January','February','March',None])
	test_df['Column_7'] = [22,None,'',None]
	test_df['Column_8'] = [3.5,0.05,999.4,None]
	test_df['Column_9'] = ['15:00','03:00','09:00',None]
	test_df['Column_10'] = ['   ',' stanley this ',' ',"\n \t some'String"] 

	return test_df

