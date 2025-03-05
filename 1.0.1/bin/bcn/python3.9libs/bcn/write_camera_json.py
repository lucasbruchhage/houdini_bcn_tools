import json
import os
import hou

homedir = hou.getenv("HOME") + "/Desktop"


def save_node_parameters_as_json(output_directory= homedir, file_name='camera_parameters.json'):
    # Get the currently selected node
    selected_nodes = hou.selectedNodes()

    if not selected_nodes:
        raise RuntimeError("No node selected. Please select a node.")

    node = selected_nodes[0]

    # Specify the parameters you want to extract
    parameter_names = ["winx", "winy", "winsizex", "winsizey"]

    # Create a dictionary to hold parameter values
    parameter_dict = {}

    # Loop over parameter names and get their values from the node
    for name in parameter_names:
        parm = node.parm(name)
        if parm:
            parameter_dict[name] = parm.eval()
        else:
            parameter_dict[name] = None  # Handle missing parameters

    # Convert the dictionary to a JSON string
    json_str = json.dumps(parameter_dict, indent=4)

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Define the full path for the JSON file
    file_path = os.path.join(output_directory, file_name)

    # Write the JSON string to the file
    with open(file_path, 'w') as json_file:
        json_file.write(json_str)

    return file_path

# Use the function in Houdini
json_file_path = save_node_parameters_as_json()
print(f"Parameters saved to: {json_file_path}")