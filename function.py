import time
import pandas as pd
from IPython.display import clear_output
import base

def handle_dependencies(input_string):
    dependencies = {}
    
    if input_string == '':
        print('Null')
        return None
    else:
        # Split input_string into pairs and strip spaces
        pairs = [pair.strip() for pair in input_string.split(',')]

        for pair in pairs:
            key, value = map(str.strip, pair.split(':'))
            if key in dependencies:
                dependencies[key].append(value)
            else:
                dependencies[key] = [value]
        return dependencies
    
def add_function(df):
    df = df.copy()
    
    name = input("Enter the name of the module: ")
    syntax = base.add_newline_for_spaces(input("Enter the syntax: "))
    desc = input("Enter the description: ")
    dependencies = input("Enter dependency type followed by name of dependency (e.g. 'library:pandas')\n \
If multiple dependencies, separate each item with a comma.")
    # tags = input("Enter modules that this function may be associated with: ")

    dependencies = handle_dependencies(dependencies)

    if name: 
        new_data = {'name': name,
                    'desc': desc,
                    # 'tags': tags,
                    'dependencies': dependencies,
                    'syntax': syntax
                   }
        df.loc[-1] = new_data
    
    return df

def edit_function(df):
    df = df.copy()
    
    base.view_list(df)
    
    name_to_edit = input("Enter the name of the module to edit: ")

    if name_to_edit in df['name'].values:
        new_name = input("Enter the new name (or press enter to keep it the same): ")
        new_syntax = base.add_newline_for_spaces(input("Enter the new syntax (or press enter to keep it the same): "))
        new_desc = input("Enter the new description (or press enter to keep it the same): ")
        # new_tags = input("Enter the new tags (or press enter to keep them the same): ")
        new_dependencies = handle_dependencies(input("Enter the new dependencies (or press enter to keep them the same): "))

        if new_name: df.loc[df['name'] == name_to_edit, 'name'] = new_name
        if new_syntax: df.loc[df['name'] == name_to_edit, 'syntax'] = new_syntax
        if new_desc: df.loc[df['name'] == name_to_edit, 'desc'] = new_desc
        # if new_tags: df.loc[df['name'] == name_to_edit, 'tags'] = new_tags
        if new_dependencies: df.loc[df['name'] == name_to_edit, 'dependencies'] = new_dependencies
    else:
        print(f"No module named {name_to_edit} found.")
        time.sleep(1.10)
        
    return df

def remove_function(df):
    df = df.copy()
    
    base.view_list(df)
    
    name_to_drop = input("Enter the name of the module to remove: ")
    
    if name_to_drop in df['name'].values:
        item_index = df[df["name"] == name_to_drop].index
        print(item_index[0])
        df = df.drop(item_index[0])
    else:
        print(f"No module named {name_to_drop} found.")
        time.sleep(1.10)
    
    return df

def manage_functions():
    df = base.data_saver(load_function=True)
    
    while True:
        time.sleep(0.05)
        clear_output()
        # Ask the user what they want to do
        print('What would you like to do?')
        action = input("""
        1) Add a new entry
        2) Edit an existing one
        3) Remove a specific function
        4) View a list of current functions
        5) View a specific function
        6) Exit
        """)
        
        if action == '1':
            # Add a new entry
            df = add_function(df)
        
        elif action == '2':
            # Edit an existing one
            df = edit_function(df)
        
        elif action == '3':
            # Remove a specific function
            df = remove_function(df)
        
        elif action == '4':
            # View a list of current functions
            base.view_list(df)
            input('Press enter to continue')
        
        elif action == '5':
            # View a specific function
            base.view_specific(df)
            input('Press enter to continue')
        
        elif action == '6':
            # Exit
            break
        
        else:
            print("Invalid action. Please choose a valid option.")
            time.sleep(1.25)
    
        df = df.drop_duplicates(subset='name', keep='first').reset_index(drop=True)
        
    base.data_saver(saved_data=df)
    
    return None