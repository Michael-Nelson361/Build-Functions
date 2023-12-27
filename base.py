import os
import re
import pandas as pd

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

def add_newline_for_spaces(text):
    # Replace two or more spaces with a newline followed by the spaces
    modified_text = re.sub(r'(\S)(\s{3,})', r'\1\n\2', text)
    return modified_text

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