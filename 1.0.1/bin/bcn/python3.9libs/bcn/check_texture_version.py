import hou
import toolutils
import os
import shutil
import random
import datetime
import webbrowser
import time




def go():
    # Get params
    #hip = hou.expandString('$HIP')
    #normalized_path_hip = os.path.normpath(hip)
    #path_components_hip = normalized_path_hip.split(os.sep)
    #print(normalized_path_hip)
   
    #set node env
    obj = hou.node("/obj")
    lops = hou.node("/stage")
    selectedNode = hou.selectedNodes()[0]

    print(selectedNode)

    #find all nodes that contain a texture and eval their path
    child_nodes = selectedNode.children()
    for child in child_nodes:
        getParm = child.parm("tex0")
        if getParm != None:
            evalParm = getParm.eval()
            #print(evalParm)
            path = evalParm
            dirs_in_path = path.split('/')
            # Combine them back to form a path to the 'lookdev' directory
            lookdev_path = '/'.join(dirs_in_path[:-2])
            
            # Extract all directories in 'lookdev' that start with 'v' and have only digits after it
            version_dirs = [d for d in os.listdir(lookdev_path) if d.startswith('v') and d[1:].isdigit()]

            # If no such directory exists, then no versions exist
            if not version_dirs:
                print("No versions exist.")
                
            # Extract version numbers, choose the maximum
            max_version = max(int(d[1:]) for d in version_dirs)

            # Combine with lookdev_path and file name to get the latest path
            latest_version_file_path = f"/{lookdev_path}/v{max_version:03}/{dirs_in_path[-1]}"

            print(max_version)
            print(latest_version_file_path)
            getParm.set(latest_version_file_path)


            
                    



        


   

   







