#Importing the headers for processing the dataframes.
import numpy as np
import pandas as pd

#Importing the headers to create the folders.
import os

#_____________________________________________
#MEthod 1

#Feeds Data to the FolderSplitter functio based on maximum uniques.n.
def using_maxUniques(filepath, max_uniques, output_folderpath):
    '''Returns a Folder Structure of the tables
    in the csv.
    *filepath -> Your csv file.
    *max_uniques -> Max uniques allowed.
    *output_folderpath -> Folder within which sub folders
    will be formed.
    '''
  
    #It's uhmm, the parent_folder within which the sub folders will be formed.
    parent_folder = output_folderpath
    
    #Importing the csv as a df.
    data_csv = pd.read_csv(filepath)
    
    #IF condition to check the folder's existence.
    if not os.path.exists(parent_folder):
                
        #Create the folder.
        os.makedirs(parent_folder)
        
    
    #Total count of rows.
    rows_total = len(data_csv)
    
    #Total count of columns.
    cols_total = data_csv.shape[1]
    
    #Current column.
    col_current = 0
    
    #Passing the data into FolderSplitter.
    outputstring = FolderSplitter2(data_csv, max_uniques, col_current, cols_total, parent_folder)
    
    print(outputstring)

#_____________________________________________

#The recursive code to split folders.
def FolderSplitter2(data_csv, max_uniques, col_current, cols_total, parent_folder):
    
    #Is the current column within the total columns limit?
    if col_current < cols_total:

        #Unique values in the current column.
        current_uniqueValues = pd.unique(data_csv.iloc[:, col_current])
        
        #Count of unique values in current column.
        col_uniqueCount = len(current_uniqueValues)
        
        #current column name.
        current_colname = data_csv.columns[col_current]
            
        #Check if current column is within the limits of max_uniques.
        if col_uniqueCount < (max_uniques + 1):           
            
            #Directory_maker(folder_path) 
            #parent_folder = parent_folder + '\\' +  str(current_colname)
            
            #IF condition to check the folder's existence.
            if not os.path.exists(parent_folder):
                #Create the folder.
                os.makedirs(parent_folder)
                
            
            #Writing data to the csv.
            data_csv.to_csv(parent_folder + '\Output_' + str(current_colname) + '.csv', index = False)
            
            
            #For condition to cycle through the unique values.
            for value in current_uniqueValues:

                #Creating the folder path.
                #folder_path = os.path.join(parent_folder, data_csv.columns[col_current])
                #folder_path = os.path.join(parent_folder, str(value))
                folder_path = parent_folder + '\\' + str(value)                 

            
                #Temporary sub dataframe.
                data_temp = data_csv[data_csv[current_colname] == value]
                
                #Writing the csv to the created folder_path.
                ##data_temp.to_csv(folder_path + '\Output_' + str(value) + '.csv', index = False)
                
                
                if col_current == (cols_total - 1):
                
                    #IF condition to check the folder's existence.
                    if not os.path.exists(folder_path):
                        
                        #Create the folder.
                        os.makedirs(folder_path)
                        
                    data_temp.to_csv(folder_path + '\Output_' + str(value) + '.csv', index = False)         
                
                
                #Sweet Sweet Recursion baby!
                FolderSplitter2(data_temp, max_uniques, (col_current + 1), cols_total, folder_path)
            
            
        else:

            #When the uniques are out of hand/ beyond the maximum specified, this recursive code is called in.
            #So basically, more recursion baby!
            FolderSplitter2(data_csv, max_uniques, (col_current + 1), cols_total, parent_folder)
        
    #The main else condition.
    else:
        
        stringSample = 'dummy string'
        
        
    #The output string.
    outputstring = '\n_____________________________\n_____________END_____________\nThe folders and nested sub-folders have been created in the location: \n' + str(parent_folder) + '\n_____________END_____________\n_____________________________'
        
    #I dont even know if this is necessary, oh well, gotta return something :-P .
    return outputstring
    
    
#_____________________________________________
#METHOD 2

#Recursive code to split the columns based on the column names input.
def FolderSplitter_Columns(data_csv, columnList, current_col, total_col_count, parent_folder):
    
    #Is the current column within the list of total column inputs (total_col_count).
    if current_col < total_col_count:
        
        #Unique values in the current column.
        current_uniqueValues = pd.unique(data_csv.loc[:, columnList[current_col]])      
        
        #IF condition to check the folder's existence.
        if not os.path.exists(parent_folder):
            
            #Create the folder.
            os.makedirs(parent_folder)      
        
        
        #Writing data to the csv.
        data_csv.to_csv(parent_folder + '\Output_' + str(columnList[current_col]) + '.csv', index = False)
        
        for value in current_uniqueValues:

            #Creating the folder path.
            #folder_path = os.path.join(parent_folder, data_csv.columns[col_current])
            #folder_path = os.path.join(parent_folder, str(value))
            folder_path = parent_folder + '\\' + str(value)                 


            #Temporary sub dataframe.
            data_temp = data_csv[data_csv[str(columnList[current_col])] == value]
            
            if current_col == (total_col_count - 1):
                
                #IF condition to check the folder's existence.
                if not os.path.exists(folder_path):
                        
                    #Create the folder.
                    os.makedirs(folder_path)
                        
                    data_temp.to_csv(folder_path + '\Output_' + str(value) + '.csv', index = False)   
                 
                
            #Sweet Sweet Recursion baby!
            FolderSplitter_Columns(data_temp, columnList, (current_col + 1), total_col_count, folder_path)
        
    #The main else condition.
    else:
        
        #I dont even know if this is necessary, oh well, gotta return something :-P .
        stringSample = 'Dummy string'
        
        
    #The output string.
    outputstring = '\n_____________________________\n_____________END_____________\nThe folders and nested sub-folders have been created in the location: \n' + str(parent_folder) + '\n_____________END_____________\n_____________________________'
        
    #I dont even know if this is necessary, oh well, gotta return something :-P .
    return outputstring
      
      
#_____________________________________________

#Fetch input from the user and folder split.
def Split_with_columnNames(filepath, output_folderpath):

    '''Returns a Folder Structure based on the Selected
    Column names from the tables in the csv.
    *filepath -> Your csv file.
    *output_folderpath -> Folder within which sub folders
    will be formed.
    '''
    
    #It's uhmm, the parent_folder within which the sub folders will be formed.
    parent_folder = output_folderpath
    
    #Initiate empty lists to be used later.
    list_colName = []
    list_colUniques = []
    list_inputColnames = []
    current_col = 0
    
    #Importing the csv as a df.
    data_csv = pd.read_csv(filepath)

    #Displaying datatable with column name and its uniques count to the user.
    for column in data_csv.columns:

        list_colName.append(column)
        list_colUniques.append(len(pd.unique(data_csv.loc[:, column])))

        df_colstructure = pd.DataFrame({'Column name' : list_colName,
                                       'Unique Count' : list_colUniques},
                                      columns = ['Column name', 'Unique Count']).sort_values(by = ['Unique Count'], ascending = True)

    print(df_colstructure)
    
    #For aesthetics.
    print('\n____________________________\n') 
    
    #Input count?
    inputCount = input('Count of column names (Folder depth): ')
    
    #While condition to loop until the input is an int.
    while (inputCount.isdigit() == False) or ((int(inputCount) < (len(list_colName) + 1)) == False):
        
        print('[ERROR] - Please Enter an interger within : *' + str(len(list_colName)) + '* and try again.')
        print('____________________________')
        inputCount = input("Count of column names (Folder depth): ")
        print('____________________________')
        
        #The if condition to verify if the entered input is an integer.
        if (inputCount.isdigit() == False):
            print("Incorrect input, please enter an integer.")
        
        elif ((int(inputCount) < (len(list_colName) + 1)) == False):
            print("Incorrect input, please enter an integer within : " + str(len(list_colName)))
            
        else:
            #Break the loop.
            break
        
    #For aesthetics.
    print('____________________________')
    
    #Obtaining the column names from the user.
    for count in range(0, int(inputCount), 1):
    
        #Adding the user input to a list.
        colname = str(input('Input the folder number ' + str(count + 1) + ' -> '))
        
        #Checking if the entered column names actually exist.
        while (colname in list_colName) == False:
            
            print('[ERROR] - This column name does NOT exists in the table.')
            print('____________________________')
            colname = input("Please Enter a Column name that exists in the datatable: ")
            print('____________________________')
            
            #The if condition to verify if the column name exists in the list of column names.
            if (colname in list_colName) == False:
                
                print('Incorrect input, This column name does NOT exists in the table.')
                
            else:
                #Break the loop.
                break
        
        #Adding the inputs to the list.
        list_inputColnames.append(colname)
        
        
    #Calling the recursive code to get the job done.
    outputstring = FolderSplitter_Columns(data_csv, list_inputColnames, current_col, int(len(list_inputColnames)), parent_folder)
    
    #Notifying the user about the end of execution.
    print(outputstring)
    
    
    
#_____________________________________________
