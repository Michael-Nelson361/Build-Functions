import base
import pandas
import time
import autopep8
from IPython.display import clear_output

def get_filename():
    filename = input("Enter the filename: ")

    # Check if the filename ends with .py
    if not filename.endswith('.py'):
        filename += '.py'

    return filename

def select_functions():
    # Retrieve the functions
    df = base.data_saver(load_function=True)
    
    while True:
        # Clear screen
        time.sleep(0.05)
        clear_output()
        
        # Display available functions
        base.view_list(df)
        
        # Get user input
        input_string = input("Enter function names separated by commas: ")
        input_list = [name.strip() for name in input_string.split(',') if name.strip()]

        # Filter against DataFrame
        valid_functions = df[df['name'].isin(input_list)]['name'].tolist()

        if not valid_functions:
            print("None of the entered functions are available. Please try again.")
            time.sleep(1.5)
            continue

        print("Selected functions:", ', '.join(valid_functions))
        choice = input("Press Enter to confirm or 'restart' to start over: ").lower()

        if choice == 'restart':
            continue
        else:
            # Return the list of valid functions if user confirms
            return valid_functions
        
def find_dependencies(func_names, all_dependencies=set()):
    df = base.data_saver(load_function=True)
    
    new_dependencies = set()

    for func in func_names:
        # Get dependencies for the current function
        current_dependencies = df[df['name'] == func]['dependencies'].iloc[0]
        
        # Extract function dependencies if they exist
        func_dependencies = current_dependencies.get('function', []) if isinstance(current_dependencies, dict) else []

        # Add new dependencies to the set
        for dependency in func_dependencies:
            if dependency not in all_dependencies:
                new_dependencies.add(dependency)

    # Update the overall dependencies set
    all_dependencies.update(new_dependencies)

    # Recursively find dependencies for the new dependencies
    if new_dependencies:
        find_dependencies(new_dependencies, all_dependencies)

    return list(all_dependencies) if all_dependencies else None

def find_library_dependencies(func_names):
    df = base.data_saver(load_function=True)
    required_libraries = set()

    for func in func_names:
        # Retrieve the dependency record for the function
        dependency_record = df[df['name'] == func]['dependencies'].iloc[0]

        # Check if the record is a dictionary and contains the 'library' key
        if isinstance(dependency_record, dict) and 'library' in dependency_record:
            libraries = dependency_record['library']
            required_libraries.update(libraries)

    return list(required_libraries)

def syntax_grabber(item_list, df):
    syntax_list = []

    for item in item_list:
        # Find the row in the DataFrame where 'name' matches 'item'
        matching_row = df[df['name'] == item]
        
        syntax_list.append(matching_row['syntax'].iloc[0])

    return syntax_list

def assembler():
    # Get the filename from the user
    filename = get_filename()
    
    # Select for the functions to be included
    main_functions = select_functions()
    
    # Get the secondary functions that may be required to run
    primary_functions = find_dependencies(main_functions)
    
    # Establish the list of libraries
    libraries = set()
    
    # Add the libraries to the set
    libraries.update(set(find_library_dependencies(main_functions)))
    
    if primary_functions:
        libraries.update(set(find_library_dependencies(primary_functions)))
    
    # Retrieve the library syntaxes
    libraries_syntax = syntax_grabber(libraries,
                                      base.data_saver(load_library=True))
    
    if primary_functions:
        # Retrieve the function syntaxes
        function_syntax = syntax_grabber(primary_functions + main_functions,
                                        base.data_saver(load_function=True))
    else:
        function_syntax = syntax_grabber(main_functions,
                                        base.data_saver(load_function=True))
    
    # Build the file
    print(f'Creating {filename}...')
    with open(filename,'w') as file:
        for item in libraries_syntax:
            file.write(item + '\n')
            
        file.write('\n')
        
        for item in function_syntax:
            file.write(item + '\n\n')
    
    # Apply formatting fixes to the file
    corrections = autopep8.fix_file(filename)
    
    with open(filename,'w') as file:
        file.write(corrections)