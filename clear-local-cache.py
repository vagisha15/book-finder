import os

def delete_pyc_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pyc"):
                pyc_file = os.path.join(root, file)
                os.remove(pyc_file)
                print(f"Deleted: {pyc_file}")

# Specify the directory where you want to delete .pyc files
directory = "/path/to/your/directory"

# Call the function to delete .pyc files
delete_pyc_files(directory)
