import hou
import json
import os

# Define the location of the JSON file
json_file_path = os.path.join("/mnt/production/project/bcn_mstrs/work", "screen_data.json")

def import_screen():
    # Load existing data from the JSON file
    try:
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
                if isinstance(data, dict):
                    data = [data]  # Convert dictionary to list
                elif not isinstance(data, list):
                    data = []  # Reset to empty list if data isn't a list or dict
        else:
            hou.ui.displayMessage(f"No data found in {json_file_path}.")
            return
    except json.JSONDecodeError:
        hou.ui.displayMessage(f"Error reading {json_file_path}.")
        return

    # If no screens available
    if not data:
        hou.ui.displayMessage(f"No screens are available in {json_file_path}.")
        return

    # Display available screens to the user
    screen_names = [screen['screen_name'] for screen in data]
    selected_index = hou.ui.selectFromList(screen_names, message="Select a screen to import:")
    
    if not selected_index:
        return  # User canceled

    selected_screen = data[selected_index[0]]

    # Get the HIP file path of the selected screen and merge it into the current scene
    hip_file_path = selected_screen["hip_file_path"]

    if not os.path.exists(hip_file_path):
        hou.ui.displayMessage(f"File {hip_file_path} does not exist.")
        return

    try:
        hou.hipFile.merge(hip_file_path)
        hou.ui.displayMessage(f"Screen '{selected_screen['screen_name']}' has been imported successfully.")
    except Exception as e:
        hou.ui.displayMessage(f"Failed to import screen: {e}")

def create_screen():
    # Get user input for screen name
    result = hou.ui.readInput("Enter the screen name:", buttons=("OK", "Cancel"))
    if result[0] == 1:
        return  # User canceled
    screen_name = result[1]

    # Get user input for frame range
    result = hou.ui.readInput("Enter the frame range (start,end):", buttons=("OK", "Cancel"))
    if result[0] == 1:
        return  # User canceled
    frame_range = result[1]

    # Get user input for FPS
    result = hou.ui.readInput("Enter the FPS:", buttons=("OK", "Cancel"))
    if result[0] == 1:
        return  # User canceled
    fps = result[1]

    # Get the currently open HIP file path
    hip_file_path = hou.hipFile.path()

    # Create a dictionary to hold the screen data
    screen_data = {
        "screen_name": screen_name,
        "frame_range": frame_range,
        "fps": fps,
        "hip_file_path": hip_file_path
    }

    # Load existing data from the JSON file
    try:
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
                if isinstance(data, dict):
                    data = [data]  # Convert dictionary to list
                elif not isinstance(data, list):
                    data = []  # Reset to empty list if data isn't a list or dict
        else:
            data = []
    except json.JSONDecodeError:
        data = []  # Handle empty or corrupted JSON file

    # Append new screen data
    data.append(screen_data)

    # Save the updated data back to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    hou.ui.displayMessage(f"Screen data saved to {json_file_path}.")

def ask_user_action():
    result = hou.ui.displayMessage(
        "Do you want to import a screen or create a screen?",
        buttons=("Import", "Create")
    )
    if result == 0:
        import_screen()
    elif result == 1:
        create_screen()

# Run the function to ask the user
ask_user_action()