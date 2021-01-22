# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 13:11:45 2021

@author: jacob.hester
"""

import os
import glob
import pandas as pd 

# load in dataframes and concatenate together
path = (
    "C:/Users/jacob.hester/Documents/Python_scripts/"\
    "Historical_beef_cattle_prices/data/processed"
    )
raw_files_path = os.path.join(path, "*.csv")
df_list = []
for f in glob.glob(raw_files_path):
    print(f)
    df = pd.read_csv(f, index_col=None, header=0)
    df_list.append(df)
df = pd.concat(df_list, ignore_index = True)

# exploratory analysis -------------------------------------------------------

# check data types
df.dtypes

# rename Hd Cnt col and change type 
# NOTE: column was read in as object type because of commas in head counts
df.rename(columns = {'Hd Cnt' : 'Hd_cnt'}, inplace = True)
df['Hd_cnt'] = df['Hd_cnt'].str.replace(',', '')
data_types_dictionary = {'Hd_cnt' : float}
df = df.astype(data_types_dictionary)

# things to look at:
# 1 - overall sales per month over time 


