import os

def create_new_dir():
    # Get the directory where the script is being run
    root_dir = os.getcwd()  # Gets the current working directory
    dir_name = "11-Working-with-Databases"  # Name of the new folder

    # Define the new folder path    
    new_folder_path = os.path.join(root_dir, dir_name)

    # Create the new folder if it doesn't exist
    if not os.path.exists(new_folder_path):
        os.mkdir(new_folder_path)
        print(f"Folder '{dir_name}'' created successfully at {new_folder_path}")
    else:
        print(f"Folder '{dir_name}' already exists at {new_folder_path}")

create_new_dir()