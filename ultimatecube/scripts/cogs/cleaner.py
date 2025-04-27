import os
import json

# Load the JSON file (located in the scripts folder)
config_file = "config.json"
config_path = os.path.join(os.path.dirname(__file__), "..", config_file)

DEFAULTS = {
    "cleanup_txt": True,
    "cleanup_png": True,
}

if not os.path.exists(config_path):
    print(f"Error: Configuration file '{config_path}' not found.\n")
    exit(1)

with open(config_path, "r") as config_file:
    _config = json.load(config_file)

cleanup_txt = _config.get("cleanup_txt", DEFAULTS["cleanup_txt"])
cleanup_png = _config.get("cleanup_png", DEFAULTS["cleanup_png"])

def clear(folder_name: str = None):
    # Define the path to the target folder (relative to the ultimatecube base folder)
    base_dir = os.path.join(os.path.dirname(__file__), "..", "..")  # Go two levels up to the ultimatecube folder
    target_folder = os.path.join(base_dir, folder_name)
    
    # Check if the folder exists
    if not os.path.exists(target_folder):
        print(f"The folder '{target_folder}' does not exist.\n")
        return
    
    # Iterate through files in the folder
    for file_name in os.listdir(target_folder):
        file_path = os.path.join(target_folder, file_name)
        try:
            # Delete the file
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")

if cleanup_txt:
    print("Cleaning up .txt files...\n")
    clear("converted_frames")  # Clean up the converted_frames folder
else:
    print("Cleanup_txt is disabled. No files were deleted.\n")

if cleanup_png:
    print("Cleaning up .png files...\n")
    clear("images")  # Clean up the images folder
else:
    print("Cleanup_png is disabled. No files were deleted.\n")