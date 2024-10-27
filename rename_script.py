import os

def rename_files(directory, prefix='file', max_length=50):
    """
    Recursively renames files in the given directory and its subdirectories to shorter names if they exceed max_length.

    Parameters:
    - directory: The root directory to start renaming files.
    - prefix: The prefix to use for the new filenames.
    - max_length: Maximum length of the filename to avoid Git path issues.
    """
    counter = 0
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Check if filename length exceeds max_length
            if len(filename) > max_length:
                extension = os.path.splitext(filename)[1]
                new_name = f"{prefix}_{counter}{extension}"
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, new_name)
                
                # Rename the file
                os.rename(old_path, new_path)
                print(f'Renamed: {old_path} -> {new_path}')
                counter += 1

# Specify the directory to start renaming files
directory = 'C:\\Users\\thoma\\Downloads\\Missile Interception System\\'

# Call the function
rename_files(directory)
