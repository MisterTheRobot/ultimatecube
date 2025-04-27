from PIL import Image, ImageDraw, ImageFont
import os
import shutil  # For moving files
import json  # For loading gradient configuration

# Constants
WIDTH = 40
HEIGHT = 40
FONT_SIZE = 12
DEFAULTS = {
    "start_color": [255, 255, 255],  # White
    "end_color": [0, 0, 0],  # Black
    "gradient_steps": HEIGHT,
}

# Load a monospaced font (adjust the path to your font file)
font = ImageFont.truetype("consola.ttf", FONT_SIZE)

# Load gradient settings from JSON
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "..", "config.json")  # Adjusted to point to scripts/config.json

# Debugging: Print the resolved path
print(f"Looking for config.json at: {config_path}")

if not os.path.exists(config_path):
    print("Error: configuration file not found.\n")
    exit(1)

with open(config_path, "r") as config_file:
    _config = json.load(config_file)

gradient_steps = _config.get("gradient_steps", DEFAULTS["gradient_steps"])  # Number of gradient steps
start_color = _config.get("start_color", DEFAULTS["start_color"])  # White
end_color = _config.get("end_color", DEFAULTS["end_color"])  # Black

def interpolate_color(start, end, factor):
    """Interpolate between two colors."""
    return [
        int(start[i] + (end[i] - start[i]) * factor)
        for i in range(3)
    ]

def text_to_image(frame_file, output_file):
    with open(frame_file, "r") as f:
        lines = f.readlines()

    # Ensure all lines are exactly WIDTH characters long
    padded_lines = [line.rstrip().ljust(WIDTH) for line in lines]

    # Calculate the image dimensions based on the text dimensions
    img_width = WIDTH * FONT_SIZE
    img_height = HEIGHT * FONT_SIZE

    # Create an image with a black background
    img = Image.new("RGB", (img_width, img_height), "black")
    draw = ImageDraw.Draw(img)

    # Draw the text onto the image with gradient colors
    for i, line in enumerate(padded_lines):
        factor = min(i / gradient_steps, 1)  # Normalize factor to [0, 1]
        color = interpolate_color(start_color, end_color, factor)
        
        text_width = draw.textlength(line, font=font)
        x_offset = (img_width - text_width) // 2  # Center horizontally
        y_offset = i * FONT_SIZE  # Line height
        draw.text((x_offset, y_offset), line, font=font, fill=tuple(color))

    img.save(output_file)

# Define paths relative to the script's directory
frames_dir = os.path.join(script_dir, "..", "..", "frames")  # Adjusted to go two levels up
images_dir = os.path.join(script_dir, "..", "..", "images")  # Adjusted to go two levels up
converted_frames_dir = os.path.join(script_dir, "..", "..", "converted_frames")  # Adjusted to go two levels up

# Ensure the frames folder exists
if not os.path.exists(frames_dir):
    print(f"Error: The folder '{frames_dir}' does not exist.\n")
    exit(1)
if not os.path.exists(images_dir):
    os.makedirs(images_dir)
if not os.path.exists(converted_frames_dir):
    os.makedirs(converted_frames_dir)

# Process all .txt files in the frames folder
for frame in sorted(os.listdir(frames_dir)):
    if frame.startswith("frame_") and frame.endswith(".txt"):
        frame_path = os.path.join(frames_dir, frame)
        output_file = os.path.join(images_dir, frame.replace(".txt", ".png"))
        print(f"Processing {frame_path} -> {output_file}\n")
        
        # Convert the .txt file to an image
        text_to_image(frame_path, output_file)
        
        # Move the .txt file to the converted_frames folder
        converted_frame_path = os.path.join(converted_frames_dir, frame)
        shutil.move(frame_path, converted_frame_path)
        print(f"Moved {frame_path} -> {converted_frame_path}\n")

print("All frames have been converted to images.\n")