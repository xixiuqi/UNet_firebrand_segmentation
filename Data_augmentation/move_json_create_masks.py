import os
import shutil
import subprocess

def move_json_files_to_folder(source_dir, destination_dir):
    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Get a list of all files in the source directory
    files = os.listdir(source_dir)

    # Filter out only the .json files
    json_files = [file for file in files if file.endswith('.json')]

    # Move each .json file to the destination directory
    for file in json_files:
        src = os.path.join(source_dir, file)
        dst = os.path.join(destination_dir, file)
        shutil.move(src, dst)
        print(f"Moved '{file}' to '{destination_dir}'")

# Specify the source directory (current directory) and the destination directory
source_directory = '.'  # Current directory
destination_directory = 'new_folder_name'  # Change this to the desired destination folder name

# Call the function to move the .json files
move_json_files_to_folder(source_directory, destination_directory)

def process_json_files(folder_path):
    # List all .json files in the folder
    json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]

    # Iterate through each .json file
    for json_file in json_files:
        # Construct the full path to the JSON file
        json_file_path = os.path.join(folder_path, json_file)

        # Run labelme_export_json command for the current JSON file
        subprocess.run(['labelme_export_json', json_file_path])

# Replace 'folder_path' with the path to your folder containing the .json files
folder_path = r'C:\Users\xxi1\Desktop\images\new_folder_name'

# Call the function to process the .json files
process_json_files(folder_path)