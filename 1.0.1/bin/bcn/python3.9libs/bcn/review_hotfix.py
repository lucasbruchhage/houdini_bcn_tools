import hou

def go():
    # Get the selected nodes
    selected_nodes = hou.selectedNodes()

    # Iterate through each selected node
    for node in selected_nodes:
        node.parm("picture").set("$HIP/pyblish/$OS/$OS.$F4.png")
        node.parm("variant").set("$OS")
        node.parm("AYON_productName").set("$OS")
        node.parm("folderPath").set("$AYON_FOLDER_PATH")
        node.parm("task").set("$AYON_TASK_NAME")

        # Add other parameters you want to set

    # Notify that parameters have been set
    hou.ui.displayMessage("Parameters have been set!")

# Call the function
go()