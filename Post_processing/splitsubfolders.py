import os
import shutil

# Define the path to the folder containing files
folder_path = "frames./subfolder_5"

# List all files in the folder
files = os.listdir(folder_path)

# Sort the files by name
files.sort()

# Calculate the number of files per subfolder
files_per_subfolder = len(files) // 5

# Create subfolders if they don't exist
for i in range(5):
    subfolder_path = os.path.join(folder_path, f"subfolder_{i+1}")
    os.makedirs(subfolder_path, exist_ok=True)

# Move files into subfolders
for i in range(5):
    start_index = i * files_per_subfolder
    end_index = (i + 1) * files_per_subfolder if i < 4 else None
    subfolder_files = files[start_index:end_index]
    subfolder_path = os.path.join(folder_path, f"subfolder_{i+1}")
    for file in subfolder_files:
        file_path = os.path.join(folder_path, file)
        dest_path = os.path.join(subfolder_path, file)
        shutil.move(file_path, dest_path)
