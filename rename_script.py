import os

def rename_files(directory, prefix='file'):
    """
    Recursively renames files in the given directory and its subdirectories to shorter names.

    Parameters:
    - directory: The root directory to start renaming files.
    - prefix: The prefix to use for the new filenames.
    """
    counter = 0
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.startswith('events.out.tfevents'):
                # Get file extension
                extension = os.path.splitext(filename)[1]
                # Create new filename
                new_name = f"{prefix}_{counter}{extension}"
                # Get full paths
                old_path = os.path.join(root, filename)
                new_path = os.path.join(root, new_name)
                # Rename the file
                os.rename(old_path, new_path)
                print(f'Renamed: {old_path} -> {new_path}')
                counter += 1

# Specify the directory where your TensorBoard logs are stored
directory = 'C:\\Users\\thoma\\Downloads\\Missile Interception System\\2d_versions\\2d_ml_versions_(v2)'

# Call the function
rename_files(directory)
