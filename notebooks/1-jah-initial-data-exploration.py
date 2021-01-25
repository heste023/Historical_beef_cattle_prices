# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 13:11:45 2021

@author: jacob.hester
"""

import os
import glob
import pandas as pd 
import altair as alt
import altair_viewer

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

# check for missing values 
df.isnull().sum()

# look at overall sales per year 
sales_per_yr_df = df.groupby(['Year'])['Hd_cnt'].sum()
sales_per_yr_df = pd.DataFrame(sales_per_yr_df)
sales_per_yr_df.reset_index(inplace = True)
sales_per_yr_df.head()
alt.renderers.enable('altair_viewer')
bar = alt.Chart(sales_per_yr_df).mark_bar(size = 20).encode(
    x = 'Year', 
    y = alt.Y('Hd_cnt', axis = alt.Axis(title = 'Head Count'))
).properties(
        title = {
            "text" : "Overall Sales Per Year",
            "subtitle" : "Beef Cattle Sales in Alabama"}
        )
bar.show()

# look at overall prices compared to sales per year 





