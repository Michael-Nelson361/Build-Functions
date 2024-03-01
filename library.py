
import base
import pandas as pd
import time
from IPython.display import clear_output
    

def add_library(df):
    df = df.copy()
    # Add a new entry
    name = input("Enter the name of the module: ")
    syntax = input("Enter the syntax: ")
    desc = input("Enter the description: ")

    if name:
        new_data = {'name': name, 'syntax': syntax, 'desc': desc}

        df.loc[-1] = new_data

    return df
    

def edit_library(df):
    df = df.copy()

    base.view_list(df)

    name_to_edit = input("Enter the name of the module to edit: ")

    if name_to_edit in df['name'].values:
        new_name = input("Enter the new name (or press enter to keep it the same): ")
        new_syntax = input("Enter the new syntax (or press enter to keep it the same): ")
        new_desc = input("Enter the new description (or press enter to keep it the same): ")

        if new_name: df.loc[df['name'] == name_to_edit, 'name'] = new_name
        if new_syntax: df.loc[df['name'] == name_to_edit, 'syntax'] = new_syntax
        if new_desc: df.loc[df['name'] == name_to_edit, 'desc'] = new_desc
    else:
        print(f"No module named {name_to_edit} found.")
        time.sleep(1.10)

    return df
    

def manage_library():
    df = base.data_saver(load_library=True)

    while True:
        time.sleep(0.05)
        clear_output()
        # Ask the user what they want to do
        print('What would you like to do?')
        action = input('''
        1) Add a new entry
        2) Edit an existing one
        3) View a list of current libraries
        4) View a specific library
        5) Exit
        ''')

        if action == '1':
            # Add a new entry
            df = add_library(df)

        elif action == '2':
            # Edit an existing entry
            df = edit_library(df)

        elif action == '3':
            # view current libraries
            base.view_list(df)
            input('Press enter to continue')

        elif action == '4':
            # view specific library
            base.view_specific(df)
            input('Press enter to continue')

        elif action == '5':
            # exit the program/loop
            break

        else:
            print("Invalid action. Please choose a valid option.")
            time.sleep(1.75)

        df = df.drop_duplicates(subset='name', keep='first').reset_index(drop=True)

    base.data_saver(saved_data=df)

    return None
    
