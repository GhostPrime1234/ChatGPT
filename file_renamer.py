import os
import glob
from natsort import natsorted
from re import sub


def remove_existing_numbers(filename):
    """Remove any leading numbers and spaces from the filename."""
    return sub(r'^\d+\s*.', '', filename)


# Define the directory containing the files
user_input = input("Enter a file path: ")
directory = user_input

# Get a list of all files in the directory
files = natsorted(glob.glob(os.path.join(directory, '*')))

# Loop through the files and rename them
for i, file_path in enumerate(files):
    # Check if file is directory
    if os.path.isdir(file_path) or os.path.basename(file_path).startswith('__'):
        continue

    # Extract the file name and file extension
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))

    file_name = remove_existing_numbers(file_name)
    # Create the new file name with zero-padded numbering and the original name
    new_file_name = f'{i:02}.{file_name}{file_extension}'

    # Create the new file path
    new_file_path = os.path.join(directory, new_file_name)

    print(new_file_path)
    # Rename the file
    os.rename(file_path, new_file_path)

print("Files have been renamed.")
