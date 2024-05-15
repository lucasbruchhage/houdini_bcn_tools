import hou
import os
import json

def apply_parameters():
    try:
        # Define the path to the directory containing the JSON files
        temppath = os.path.join(hou.homeHoudiniDirectory(), "copyTemp")
        
        if not os.path.exists(temppath):
            hou.ui.displayMessage("The directory 'copyTemp' does not exist!")
            return
        
        # List all JSON files in the directory
        json_files = [f for f in os.listdir(temppath) if f.endswith('.json')]
        
        if not json_files:
            hou.ui.displayMessage("No JSON files found in 'copyTemp' directory!")
            return

        # Prompt the user to select a JSON file from the list
        chosen_files = hou.ui.selectFromList(json_files, message="Select a JSON file", exclusive=True)
        
        if not chosen_files:
            hou.ui.displayMessage("No file selected!")
            return

        chosen_file = json_files[chosen_files[0]]  # Select the first chosen file

        # Path to the selected JSON file
        json_file_path = os.path.join(temppath, chosen_file)

        # Read parameters from the JSON file
        with open(json_file_path, 'r') as json_file:
            parm_dict = json.load(json_file)

        # Get the selected nodes
        selected_nodes = hou.selectedNodes()

        if len(selected_nodes) == 0:
            hou.ui.displayMessage("No nodes selected!")
            return

        # Assuming you are working with the first selected node
        node = selected_nodes[0]

        # Parameters to ignore
        ignored_params = {"id", "productType", "active", "creator_identifier", "creator_identifier", "folderPath", "task", "creator_attributes", "publish_attributes", "AYON_productName", "RS_outputFileNamePrefix", "RS_archive_file"}

        # Apply parameters to the selected node
        for parm_name, parm_value in parm_dict.items():
            if parm_name in ignored_params:
                continue
            parameter = node.parm(parm_name)
            if parameter is not None:
                try:
                    parameter.set(parm_value)
                except hou.PermissionError:
                    print(f"Could not set parameter '{parm_name}' due to insufficient permissions.")
                except hou.OperationFailed:
                    print(f"Failed to set parameter '{parm_name}'.")
            else:
                print(f"Parameter '{parm_name}' does not exist on the selected node.")

        hou.ui.displayMessage(f"Parameters from {json_file_path} have been applied to the selected node.")
    
    except Exception as e:
        hou.ui.displayMessage(f"An error occurred: {e}")

# Call the function to execute the script
