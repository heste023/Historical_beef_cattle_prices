# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 09:34:07 2021

@author: jacob.hester
"""
import pandas as pd 

# read in file 
file = "C:/Users/jacob.hester/Documents/Python_scripts/Cattle_prices/2005AverageCattlePrices.txt"
with open(file) as f:
    file_by_line = f.readlines()
    file_by_line = [x.strip() for x in file_by_line] 
    total_lines = len(file_by_line)
    
blank_line_numbers = []   
for i in range(len(file_by_line)):
    if file_by_line[i] == '':
        blank_line_numbers.append(i) 
blank_line_numbers = blank_line_numbers[3:]

# step 2 - get date from .txt file 
df1 = pd.read_table(
    file,
    header = None,
    nrows = 4,
    )
df1 = df1.loc[[3]]
year_string = str.strip(df1.iloc[0, 0])
year_val = [int(s) for s in year_string.split() if s.isdigit()]
year_val = year_val[0]

dataframe_collection = []
z_blank_line_numbers = []

for x in range(len(blank_line_numbers)):  
    
    z_blank_line_numbers = zip(blank_line_numbers, blank_line_numbers[1:] + [total_lines - 1])
    z_blank_line_numbers = [list(x) for x in z_blank_line_numbers]

z_length = len(z_blank_line_numbers)

for y in range(z_length): 
    
    col_specs = [
        (0, 15), 
        (15, 22), 
        (22, 31), 
        (31, 40), 
        (40, 49), 
        (49, 58),
        (58, 67), 
        (67, 76), 
        (76, 85), 
        (85, 94), 
        (94, 103), 
        (103, 112), 
        (112, 121), 
        (121, 130),
        (130, 139)
        ]
    
    col_names = (
        'Weight_group',
        'Hd Cnt', 
        'Jan', 
        'Feb', 
        'Mar', 
        'Apr', 
        'May', 
        'Jun', 
        'Jul', 
        'Aug', 
        'Sep', 
        'Oct', 
        'Nov', 
        'Dec', 
        'Avg',
        )
    
    df = pd.read_table(
        file,
        header = None,
        skiprows = z_blank_line_numbers[y][0],
        )
    df = df.iloc[0:2, ]
    str_1 = str.strip(df.iloc[0, 0])
    str_2 = str.strip(df.iloc[1, 0])
    cat_type_col = str_1 + ': ' + str_2
    
    df = pd.read_fwf(
        file,
        colspecs = col_specs,
        skiprows = z_blank_line_numbers[y][0] + 4,
        skipfooter = total_lines - z_blank_line_numbers[y][1] - 1,
        header = None,
        names = col_names,
        )
    
    # add columns and shift to the left of the df
    df['Year'] = year_val
    df['Type'] = cat_type_col
    first_col = 'Year'
    second_col = 'Type'
    first_col_df = df.pop(first_col)
    second_col_df = df.pop(second_col)
    df.insert(0, first_col, first_col_df)
    df.insert(1, second_col, second_col_df)
    
    dataframe_collection.append(df)
        
# see if all dfs are the same shape 
shapes_list = []
collection_len = len(dataframe_collection)
for i in range(collection_len): 
    #for y in range(len(dataframe_collection)):
        df_shape = dataframe_collection[i].shape
        shapes_list.append(df_shape)

# add an index to each element 
len_shapes_list = len(shapes_list)
ind_element = range(0, len_shapes_list)
z_list = zip(shapes_list, ind_element)
z_list = [list(x) for x in z_list]

# check indices and shapes
for z in z_list: 
    print(z)

# concat dfs 
df = pd.concat(dataframe_collection)

