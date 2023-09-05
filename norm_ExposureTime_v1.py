#!/usr/bin/env python3

import os
import glob
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import fabio

os.system("clear")

print("##############################################################")
print("# This script do the following:                              #")
print("# 1. Select multiple edf files (select directory).           #")
print("# 2. Select multiple circle files (enter to the directory).  #")
print("# 3. Normalize I(q) column in each circle file.              #")
print("##############################################################")
print("\n")

############################################################################
# inputs:
pattern="ExposureTime"                              # pattern
operation="division"                                # operation
number_column=1                                     # this choose the second column

############################################################################
# create a list of edf file:
root = tk.Tk()
root.withdraw()
edf_dir_path=filedialog.askdirectory()              # interactive to choose a directory, create the root path to the df directory
edf_list=glob.glob(edf_dir_path + "/*.edf")         # create a list of path for every .edf file

# create a un dataframe with filename and patterna values:
edf_filename_list=[]                                # empty list to append
edf_name_list=[]                                    # empty list to append
pattern_value_list=[]                               # empty list to append
for edf_path in edf_list:
    edf_filename=os.path.basename(edf_path)         # get filename with path (with .edf extension)
    edf_name=edf_filename.split(".")[0]             # get filename without path
    header=fabio.open(edf_path).header              # get header, this is a list
    header_k=fabio.open(edf_path).header_keys       # get header keys, this is a list
    pattern_value=float(header[pattern])            # choose a pattern, this is define at the beggining of the script
    
    # append data to create list and then a data frame
    edf_filename_list.append(edf_filename)          # append
    edf_name_list.append(edf_name)                  # append
    pattern_value_list.append(pattern_value)        # append

df_edf=pd.DataFrame({"edf_filename": edf_filename_list,
pattern: pattern_value_list
})
print("These are the edf files:")
print("\n")
print(df_edf)
print("\n")

#exit()

############################################################################
# create a dataframe with circles files:
circle_dir_path=filedialog.askdirectory()           # interactive to choose a directory, create the root path to the circle directory
circle_list=glob.glob(circle_dir_path + "/" "*{0}_circles_*[!_N-pattern].dat", recursive=True)  # create a list of path for every .dat file

circle_filename_list=[]                             # empty list to append
circle_name_list=[]                                 # empty list to append
for circle_path in circle_list:
    circle_filename=os.path.basename(circle_path)   # get filename with path (with .edf extension)
    circle_name=circle_filename.split(".")[0]       # get filename without path
    
    # append data to create list and then a data frame
    circle_filename_list.append(circle_filename)    # append
    circle_name_list.append(circle_name)            # append

df_circles=pd.DataFrame({"circle_filename": circle_filename_list}) # create a data frame with path to avery circles file

print("These are ther circles.dat files:")
print(df_circles)

############################################################################
# these are operation avalaible:
def choose_operation(x, operation, pattern_value):
    if operation == "addition":
        result= x + pattern_value
        return result
                
    if operation == "subtraction":
        result= x - pattern_value
        return result
                
    if operation == "multiplication":
        result= x * pattern_value
        return result
                
    if operation == "division":
        result= x / pattern_value
        return result

############################################################################
# apply the operations on a column:
new_filename_list=[]            # empty list to append
pattern_value_list=[]           # empty list to append

list_of_circle_files=df_circles["circle_filename"]                                       # list of path to every circles files
for circle_filename in list_of_circle_files:
    df=pd.read_csv(circle_dir_path +  "/" + circle_filename, comment="#", sep="\s+")     # get data as dataframe
    column_options=list(df.columns)                                                      # column option for the circler file
    column=column_options[number_column]                                                 # choose a column, the second columnn, this is defined at the begining of the script
    name=circle_filename.split("{0}")[0]                                                 # e.g. 20230413_0_00026.edf
    pattern_value=df_edf.loc[df_edf["edf_filename"] == name, pattern].iloc[0]            # get pattern value evaluating the circle filaneme into the first dataframe
    df[column]=df[column].apply(choose_operation, operation=operation, pattern_value=pattern_value) # operate on column
    df.rename(columns={column: column + "_" + operation + "_" + pattern}, inplace=True)  # rename a column

    # export the new data
    new_filename= circle_dir_path + "/" + circle_filename + "_" + operation + "_" + pattern + ".dat" # create a new file
    new_filename_for_table=circle_filename + "_" + operation + "_" + pattern + ".dat"                # create a new file

    new_file=df.to_csv(new_filename, sep="\t", index=False, float_format="%.5f", na_rep="nan")       # create a new file and save

    # append data
    new_filename_list.append(new_filename_for_table)
    pattern_value_list.append(pattern_value)

df_edf_circle=pd.DataFrame({"new_filename": new_filename_list,
pattern: pattern_value_list
})

print("These are the circles.dat files:")
#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
print(df_edf_circle)

############################################################################
exit()
