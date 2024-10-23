
import os
import re
import pandas as pd
import platform 
    

def data_saver(load_library=False,load_function=False,saved_data=None):
    # check if load_library is true
    if load_library == True:
        # check if libraries.csv exists
        if os.path.exists('libraries.csv') == True:
            libraries = pd.read_csv('libraries.csv',index_col=0)
            return libraries
        else:
            libraries = pd.DataFrame(columns=['name','syntax','desc'])
            libraries.to_csv('libraries.csv')
            return libraries

    # check if load_function is true
    elif load_function == True:
        if os.path.exists('functions.json') == True:
            functions = pd.read_json('functions.json')
            return functions
        else:
            functions = pd.DataFrame(columns=['name','desc','tags','dependencies','syntax'])
            functions.to_json('functions.json')
            return functions

    # check if saved_data is not None
    elif type(saved_data) == type(pd.DataFrame()):
        if len(saved_data.columns) == 3:
            saved_data.to_csv('libraries.csv')
        elif len(saved_data.columns) == 5:
            saved_data.to_json('functions.json')
        else:
            print('Saved data length matches none')

    else:
        print('No options provided. Exiting.')

    return None
    

def format_text(text):
    # Step 1: Add a newline character after sequences of four or more spaces
    text = re.sub(r'(\S)(\s{4,})', r'\1\n\2', text)

    # Step 2: Replace every four consecutive spaces with a tab character
    # Function to replace spaces with tabs
    def replace_with_tabs(match):
        space_length = len(match.group())
        num_tabs = space_length // 4
        return '\t' * num_tabs

    # Use regular expression to find and replace space sequences
    formatted_text = re.sub(r' {3,}', replace_with_tabs, text)

    return formatted_text
    

def view_list(df):
    df = df.copy()
    print("Current list of entries:")
    for i in df.index:
        print(f'{df.iloc[i]["name"]}: {df.iloc[i].desc}')

    print()
    return None
    

def view_specific(df):
    df = df.copy()

    view_list(df)

    item_to_view = input('Which would you like to see? ')

    # pull the library index
    item_index = df[df["name"] == item_to_view].index

    if item_to_view in df['name'].values:
        for col in df.columns:
            print(f'{col}: {df[df["name"] == item_to_view][col][item_index[0]]}')
    else:
        print(f"No module named {item_to_view} found.")

    return None
    
def check_operating_system():
    os_name = platform.system()
    if os_name == "Windows":
        return "Windows"
    elif os_name == "Darwin":
        return "macOS"
    elif os_name == "Linux":
        return "Linux"
    else:
        return "Unknown Operating System"