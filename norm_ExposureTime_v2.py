#!/usr/bin/env python3

"""
norm_ExposureTime_v1.py - Script for data nomarlizationm from SAXS.

Description:
This module contains a collection of custom functions for various data manipulation and analysis tasks.
It is designed to work with libraries such as tkinter, qtpy, matplotlib, numpy and scipy.

Author: Wilson Tarraga [wilson14t17@gmail.com]
Date: September 10, 2023
Version: 1.0

Dependencies:
- tkinter (for GUI components)
- favio (for working with edf files)
- pandas (for data analysis)
- glob (for working with directories)
- os (for working with bash tools)

Usage:
1. Make sure you have Python 3.6 or later installed.
2. Install the required packages using pip:
   #pip install tkinter favio pandas glob h5py

"""

import tkinter as tk
#from tkinter import filedialog
from qtpy.QtWidgets import QApplication, QFileDialog
import fabio
import pandas as pd
import glob
import os
import pandas as pd

os.system("clear")

print("##############################################################")
print("# This script do the following:                              #")
print("# 1. Select multiple edf files (select directory).           #")
print("# 2. Select multiple circle files (enter to the directory).  #")
print("# 3. Normalize I(q) column in each circle file.              #")
print("##############################################################")
print("\n")

#-------------------------------------------------------------------------------
# Inputs:
pattern = "ExposureTime"                              # pattern
operation = "division"                                # operation
number_column = 1                                     # this choose the second column

#-------------------------------------------------------------------------------
# Functions:
#-------------------------------------------------------------------------------

#--------------------------------#
# Operation avalaibles:          #
#--------------------------------#
def choose_operation(x, operation, pattern_value):
    '''
    Funtions available:
    
    Parameters:
        - x(float): the variable to apply the operation.
        - operation: the operation.
        - pattern_value: the numerical value on which to apply the function.

    Returns:
        - return the operation.
    '''
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

#--------------------------------#
# Open tkinter:                  #
#--------------------------------#
def open_tkinter(main_text):
    '''
    Displays a GUI window with options.
    
    Parameters:
        - main_text (str): text to be shown in GUI window 
        -
    Returns:
        - display GUI window with text.
    '''
    
    # Function to handle the "Select directory" button click:
    def select_directory():
        directory = select_directory_qtpy()  # Call the QtPy directory selection function
        if directory:
            path_var.set(directory)
            root.destroy()                   # Close the Tkinter window after selecting the directory
    
    # Create the main graphical user interface (GUI) window:
    root = tk.Tk()                           # Main application window
    root.title("Working with circle Files")  # Set the title of the window
    
    # Create a label to display the instruction:
    main_text = main_text
    
    label = tk.Label(root, text=main_text)
    label.pack(padx=50, pady=50)                  # Add some padding
    
    # Create a button to select the edf directory:
    select_button = tk.Button(root, text="Select circle Directory", command=select_directory)
    select_button.pack(pady=50)
    
    # Variable to store the selected EDF directory:
    path_var = tk.StringVar()
    
    # Start the main GUI event loop:
    root.mainloop()
    
    # Get the selected EDF directory after the GUI window is closed:
    dir_path = path_var.get()

    return dir_path

#--------------------------------#
# Select directory:              #
#--------------------------------#
# Function to select a directory
def select_directory_qtpy():
    """
    Displays a GUI window to select a directory and returns the selected directory path.
    
    Returns:
        str: The selected directory path.
    """
    
    # Initialize the QtPy application:
    app = QApplication([])

    # Prompt for directory if not defined:
    directory = QFileDialog.getExistingDirectory(None, "Select directory")

    # Exit if no directory is selected:
    if not directory:
        print("No directory selected.")
        sys.exit()

    # Return the selected directory:
    return directory

#-------------------------------------------------------------------------------
# Read edf file and get the patter value
#-------------------------------------------------------------------------------
# Create a list of edf files:
main_text = 'Select the directory containing the edf files'
edf_dir_path = open_tkinter(main_text)             # Call the function to select and process the EDF directory
edf_list = glob.glob(edf_dir_path + "/*.edf")       # Create a list of paths for every .edf file

# Create a dataframe with filename and pattern values:
edf_filename_list = []                                # Empty list to append
edf_name_list = []                                    # Empty list to append
pattern_value_list = []                               # Empty list to append
for edf_path in edf_list:
    edf_filename = os.path.basename(edf_path)         # Get filename with path (with .edf extension)
    edf_name = edf_filename.split(".")[0]             # Get filename without path
    header = fabio.open(edf_path).header              # Get header, this is a list
    header_k = fabio.open(edf_path).header_keys       # Get header keys, this is a list
    pattern_value = float(header[pattern])            # choose a pattern, this is define at the beggining of the script
    
    # Append data to create list and then a data frame:
    edf_filename_list.append(edf_filename)            # Append
    edf_name_list.append(edf_name)                    # Append
    pattern_value_list.append(pattern_value)          # Append

df_edf = pd.DataFrame({"edf_filename": edf_filename_list,
pattern: pattern_value_list
})
print("These are the edf files:")
print("\n")
print(df_edf)
print("\n")

#-------------------------------------------------------------------------------
# Read circle files .dat and select applied the function selected 
#-------------------------------------------------------------------------------
# Create a dataframe with circles files:
main_text = 'Select the directory containing the circle files'
circle_dir_path = open_tkinter(main_text)
circle_list = glob.glob(circle_dir_path + "/" + "*{0}_circles_*[!_N-pattern].dat", recursive=True)  # create a list of path for every .dat file

circle_filename_list = []                             # Empty list to append
circle_name_list = []                                 # Empty list to append
for circle_path in circle_list:
    circle_filename = os.path.basename(circle_path)   # Get filename with path (with .edf extension)
    circle_name = circle_filename.split(".")[0]       # Get filename without path
    
    # Append data to create list and then a data frame
    circle_filename_list.append(circle_filename)    # Append
    circle_name_list.append(circle_name)            # Append

df_circles = pd.DataFrame({"circle_filename": circle_filename_list}) # Create a data frame with path to avery circles file

print("\n")
print("These are ther circles.dat files:")
print(df_circles)

#-------------------------------------------------------------------------------
# Apply the operations on a column:
new_filename_list = []            # Empty list to append
pattern_value_list = []           # Empty list to append
    
list_of_circle_files = df_circles["circle_filename"]                                       # List of path to every circles files
for circle_filename in list_of_circle_files:
    df = pd.read_csv(circle_dir_path +  "/" + circle_filename, comment="#", sep="\s+")     # Get data as dataframe
    # sep: separate by \t.
    # comment: skip rows with # symbol.
    
    column_options = list(df.columns)                                                      # Column option for the circler file
    column = column_options[number_column]                                                 # Choose a column, the second columnn, this is defined at the begining of the script
    name = circle_filename.split("{0}")[0]                                                            # e.g. 20230413_0_00026.edf
    pattern_value = df_edf.loc[df_edf["edf_filename"] == name, pattern].iloc[0]                       # Get pattern value evaluating the circle filaneme into the first dataframe
    df[column] = df[column].apply(choose_operation, operation=operation, pattern_value=pattern_value) # operate on column
    df.rename(columns={column: column + "_" + operation + "_" + pattern}, inplace=True)             # Rename a column

    # Export the new data:
    new_filename = circle_dir_path + "/" + circle_filename + "_" + operation + "_" + pattern + ".dat" # Create a new file
    new_filename_for_table = circle_filename + "_" + operation + "_" + pattern + ".dat"                # Create a new file

    new_file = df.to_csv(new_filename, sep="\t", index=False, float_format="%.5f", na_rep="nan")       # Create a new file and save
    # sep: separate by \t.
    # index: do not include index.
    # float_format: the numbers are formatted with five decimal places after the decimal point.
    # na_rep: missing values are represented as (NaN, Not a Number).
    # The original file contain nan values.

    # Append data:
    new_filename_list.append(new_filename_for_table)
    pattern_value_list.append(pattern_value)

df_edf_circle = pd.DataFrame({"new_filename": new_filename_list,
pattern: pattern_value_list
})

print('\n')
print("These are the circles.dat files:")
#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
print(df_edf_circle)

#exit()
'''
#-------------------------------------------------------------------------------
# Merge all .dat files into a excel one
#-------------------------------------------------------------------------------
# Create a list with all .dat file to merge:
main_text = 'Select the directory containing the edf files'
excel_dir_path  = open_tkinter(main_text)
excel_list=glob.glob(excel_dir_path + "/" + "*[_N-pattern].dat", recursive=True)
#print(excel_list)
#exit()
# Merge files:

# DataFrame para almacenar los datos de todos los archivos
final_df = pd.DataFrame()

# Iterar a través de la lista de archivos
for file_name in excel_list:
    # Leer el archivo CSV generado anteriormente
    df = pd.read_csv(file_name, sep="\t", header=0)
    #print(df)
    # Agregar los datos al DataFrame final
    final_df = final_df.append(df)

# Escribir el DataFrame final en un archivo Excel
excel_file_name = "resultados.xlsx"
final_df.to_excel(excel_file_name, index=False, engine="openpyxl")

#print(f"Los datos se han guardado en {excel_file_name}")
#-------------------------------------------------------------------------------
'''
exit()
