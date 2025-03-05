import hou
import json
import os


def go():
        # Get user input for the JSON file name
        json_file_name = hou.ui.readInput("Enter the name for the JSON file:", buttons=("OK",))[1]

        # Ensure the filename is not empty
        if json_file_name == "":
                print("No file name provided!")
        else:
                # Add .json extension if it's not already there
                if not json_file_name.endswith(".json"):
                        json_file_name += ".json"

                # Get the selected nodes
                selected_nodes = hou.selectedNodes()

                if len(selected_nodes) == 0:
                        print("No nodes selected!")
                else:
                        # Assuming you are working with the first selected node
                        node = selected_nodes[0]

                        # Get all the parameters of the selected node
                        parameters = node.parms()

                        # Create a dictionary to store parameter names and values
                        parm_dict = {}

                        for parm in parameters:
                                parm_name = parm.name()
                                parm_value = parm.eval()
                                parm_dict[parm_name] = parm_value

                        # Define the JSON file path (save in the Houdini working directory)
                        temppath = os.path.join(hou.homeHoudiniDirectory(), "copyTemp")
                        if not os.path.exists(temppath):
                                os.mkdir (temppath)
                        json_file_path = os.path.join(hou.homeHoudiniDirectory(), "copyTemp", json_file_name)

                        # Write the dictionary to a JSON file
                        with open(json_file_path, 'w') as json_file:
                                json.dump(parm_dict, json_file, indent=4)

                        print(f"Parameters have been saved to {json_file_path}")