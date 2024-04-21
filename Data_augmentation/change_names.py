import os
 
image_folder = r'C:\Users\xxi1\Desktop\traning_set_2\masks'
 
file_list = os.listdir(image_folder)
 
start_number = 1
 
for filename in file_list:
    new_filename = str(start_number) + os.path.splitext(filename)[-1]
 
    old_filepath = os.path.join(image_folder, filename)
    new_filepath = os.path.join(image_folder, new_filename)
 
    os.rename(old_filepath, new_filepath)
 
    start_number += 1