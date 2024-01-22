# import os
# import time
# import shutil
# from tkinter import filedialog
# from datetime import datetime
#
#
# def create_subfolder(directory_path, folder_name):
#     subfolder_path = os.path.join(directory_path, folder_name)
#
#     if not os.path.exists(subfolder_path):
#         os.makedirs(subfolder_path)
#         print(f"The '{folder_name}' folder has been created at: {subfolder_path}")
#     else:
#         print(f"The '{folder_name}' folder already exists.")
#
#     return subfolder_path
#
#
# def get_file_modified_info(path_to_file):
#     file_modified_value = os.path.getmtime(path_to_file)
#     file_modified_converted = time.ctime(file_modified_value)
#     return file_modified_value, file_modified_converted
#
#
# def format_date(input_date):
#     parsed_date = datetime.strptime(input_date, '%a %b %d %H:%M:%S %Y')
#     formatted_date = parsed_date.strftime('%Y-%m')
#     return formatted_date
#
#
# # Select the folder we want as root
# root_dir = filedialog.askdirectory()
# print(f"Selected directory: {root_dir}")
#
# # Create new 'Sorted' sibling folder
# sorted_dir = create_subfolder(os.path.dirname(root_dir), 'Sorted')
# print(f"Sorted directory: {sorted_dir}")
#
# # Traverse through all files in the target folder
# for root, dirs, files in os.walk(root_dir):
#     for name in files:
#         file_curr_path = os.path.join(root, name)
#         file_sort_val, file_sort_val_converted = get_file_modified_info(file_curr_path)
#
#         # Add the files to the new folder, in sub-folders with format 'YYYY-MM'
#         target_dir_path = create_subfolder(sorted_dir, format_date(file_sort_val_converted))
#         shutil.copy(file_curr_path, target_dir_path)
#         print(f"File {file_curr_path} moved to {target_dir_path}")


import os
import time
import shutil
from tkinter import filedialog
from datetime import datetime
from PIL import Image

def create_subfolder(directory_path, folder_name):
    subfolder_path = os.path.join(directory_path, folder_name)

    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
        print(f"The '{folder_name}' folder has been created at: {subfolder_path}")
    else:
        print(f"The '{folder_name}' folder already exists.")

    return subfolder_path


def format_date(input_date):
    parsed_date = datetime.strptime(input_date, '%a %b %d %H:%M:%S %Y')
    formatted_date = parsed_date.strftime('%Y-%m')
    return formatted_date

def get_image_taken_time(image_path):
    try:
        with Image.open(image_path) as img:
            # Extract the metadata
            exif_data = img._getexif()

            # Check if the image has EXIF data
            if exif_data is not None:
                # Try to extract the datetime information from EXIF
                taken_time = exif_data.get(0x9003)  # 0x9003 corresponds to DateTimeOriginal tag
                if taken_time is not None:
                    taken_time = datetime.strptime(taken_time, "%Y:%m:%d %H:%M:%S")
                    return taken_time
                else:
                    print(f"Image {image_path} has no DateTimeOriginal tag in EXIF data.")
            else:
                print(f"Image {image_path} has no EXIF data.")
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")

    return None

# Select the folder we want as root
root_dir = filedialog.askdirectory()
print(f"Selected directory: {root_dir}")

# Create new 'Sorted' and 'Sorted with errors' sibling folders
sorted_dir = create_subfolder(os.path.dirname(root_dir), 'Sorted')
sorted_errors_dir = create_subfolder(os.path.dirname(root_dir), 'Sorted with errors')
print(f"Sorted directory: {sorted_dir}")
print(f"Sorted with errors directory: {sorted_errors_dir}")

# Traverse through all files in the target folder
for root, dirs, files in os.walk(root_dir):
    for name in files:
        file_curr_path = os.path.join(root, name)
        taken_time = get_image_taken_time(file_curr_path)

        if taken_time is not None:
            # Format the date in the desired format
            formatted_date = taken_time.strftime('%Y-%m')

            # Add the files to the 'Sorted' folder, in sub-folders with the image taken time format 'YYYY-MM'
            target_dir_path = create_subfolder(sorted_dir, formatted_date)
            shutil.copy(file_curr_path, target_dir_path)
            print(f"File {file_curr_path} moved to {target_dir_path}")
        else:
            # If there is an error, move the file to the 'Sorted with errors' folder and sort by date modified
            file_sort_val, file_sort_val_converted = os.path.getmtime(file_curr_path), time.ctime(os.path.getmtime(file_curr_path))
            formatted_date = format_date(file_sort_val_converted)
            target_dir_path = create_subfolder(sorted_errors_dir, formatted_date)
            shutil.copy(file_curr_path, target_dir_path)
            print(f"File {file_curr_path} moved to {target_dir_path} (Error)")

# Now you can handle the 'Sorted with errors' folder separately if needed
