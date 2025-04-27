import shutil
import os
import json

DEFAULTS = {"move_output": True}

# Load config settings from JSON
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(script_dir, "..", "..")  # Go two levels up to the ultimatecube folder
videos_dir = os.path.join(project_dir, "videos")  # Path to the videos folder

output_file = os.path.join(project_dir, "output.mp4")  # Path to the output.mp4 file
config_path = os.path.join(script_dir, "..", "config.json")  # Path to scripts/config.json

if not os.path.exists(config_path):
    print("Error: configuration file not found.\n")
    exit(1)

with open(config_path, "r") as config_file:
    _config = json.load(config_file)

move_output = _config.get("move_output", DEFAULTS["move_output"])

# Function to move a file to the videos directory
def move_file_to_videos_dir(file_path, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Move the file to the videos directory
    shutil.move(file_path, os.path.join(destination_dir, os.path.basename(file_path)))
    print(f"Moved {file_path} to {destination_dir}.\n")

if move_output:
    print("Moving output file...\n")

    # Check if the output file exists before moving
    if os.path.exists(output_file):
        move_file_to_videos_dir(output_file, videos_dir)
    else:
        print(f"Error: The file '{output_file}' does not exist.\n")
else:
    print("Move output is disabled. Skipping file move operation.\n")