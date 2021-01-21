# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 09:34:07 2021

@author: jacob.hester
"""
import pandas as pd 

# create empty lists for dataframes and blank line numbers
dataframe_collection = []
z_blank_line_numbers = []

# loop to work through directory
def reshape_fwfs(fwf_file):
    
    '''
        This function reshapes the fixed width files provided by the AL
    agricultural service. 
      
    '''
    # get total lines
    with open(fwf_file) as f:
        file_by_line = f.readlines()
        file_by_line = [x.strip() for x in file_by_line] 
        total_lines = len(file_by_line)
    
    # get line breaks and remove header text in files
    blank_line_numbers = []   
    for i in range(len(file_by_line)):
        if file_by_line[i] == '':
            blank_line_numbers.append(i) 
    blank_line_numbers = blank_line_numbers[3:]
    
    # get date from each text file 
    df1 = pd.read_table(
        fwf_file,
        header = None,
        nrows = 4,
        )
    df1 = df1.loc[[3]]
    year_string = str.strip(df1.iloc[0, 0])
    year_val = [int(s) for s in year_string.split() if s.isdigit()]
    year_val = year_val[0]
    
    # create zip list of breaks    
    for x in range(len(blank_line_numbers)):  
        
        z_blank_line_numbers = zip(
            blank_line_numbers, blank_line_numbers[1:] + [total_lines - 1]
            )
        z_blank_line_numbers = [list(x) for x in z_blank_line_numbers]
        
    # loop over file and create dataframes
    for y in range(len(z_blank_line_numbers)):
        
        for i in range(1): 
                
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
                fwf_file,
                header = None,
                skiprows = z_blank_line_numbers[y][0],
                )
            df = df.iloc[0:2, ]
            str_1 = str.strip(df.iloc[0, 0])
            str_2 = str.strip(df.iloc[1, 0])
            cat_type_col = str_1 + ': ' + str_2
            
            df = pd.read_fwf(
                fwf_file,
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
            
            df = pd.concat(dataframe_collection)
        
    return dataframe_collection


            
