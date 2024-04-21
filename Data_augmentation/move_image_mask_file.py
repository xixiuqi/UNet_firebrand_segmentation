import os
import shutil

def move_and_rename_files(root_folder):
# Create a new folder with the name of the sub-folder
    new_folder_path = os.path.join("masks")
    os.makedirs(new_folder_path, exist_ok=True)


    # Iterate over each sub-folder in the root folder
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        
        # Check if the current item is a directory
        if os.path.isdir(folder_path):
            # Search for files named 'img' in the sub-folder
            img_files = [file for file in os.listdir(folder_path) if file.startswith('label.png')]
            
            # If 'img' files found, move and rename them
            if img_files:
              
                # Move and rename 'img' files
                for img_file in img_files:
                    src = os.path.join(folder_path, img_file)
                    dst = os.path.join(new_folder_path, folder_name + os.path.splitext(img_file)[1])
                    shutil.move(src, dst)
                    print(f"Moved and renamed '{img_file}' to '{dst}'")

# Replace 'root_folder' with the path to the root directory
root_folder = r'C:\Users\xxi1\Desktop\images\new_folder_name'

# Call the function to move and rename the files
move_and_rename_files(root_folder)