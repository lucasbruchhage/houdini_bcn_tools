import time
import hou
import os
import os.path
from os import path
import glob
import re
import functools



def go():
    # get params
    ulc = hou.expandString('$ULC')
    uid = hou.expandString('$UID')
    pid = hou.expandString('$PID')

    #popup ask number
    #res = hou.ui.readInput("Enter number:", buttons=("OK", "Cancel"))


    #select from list
    task_list = ["modeling","lookdev","animation","fx","lighting",""]
    res = hou.ui.selectFromList(task_list, message="Please Select a Taks", title="BCN Visuals Save Version", exclusive=True, column_header="Task choice", num_visible_rows=10, clear_on_cancel=False, width=500, height=250)
    res = int(''.join(map(str, res)))
    task_choice = str(task_list[res])
    print (task_choice)
    # print (ulc)
    # print (uid)
    # print (pid)

    # define file path
    path_merge = os.path.join(ulc, uid, pid, task_choice,)
    path_merge_norm = os.path.normpath(path_merge)
    path_base = os.path.join(ulc, uid)
    path_base_norm = os.path.normpath(path_base)
    path_new_dir = os.path.join(pid, task_choice)
    path_new_dir_norm = os.path.normpath(path_new_dir)
    print (path_merge_norm)

    # check if folder exists
    if path.exists(path_merge_norm):
        print ("path exists, will save new version")
        os.chdir(path_merge_norm)
        path_for_list = str(path_merge_norm)
        latest_file = glob.glob(path_for_list + '/*.hip')  # * means all if need specific format then *.csv
        latest_file = [file for file in latest_file if str(hou.hipFile.name().split('/')[-1].rsplit('_', 1)[0]) in file]
        latest_file = max(latest_file, key=os.path.getctime)
        latest_file = os.path.basename(latest_file)
        version = re.findall(r'\d+', latest_file)
        version = int("".join(version))
        print (version)

        new_version = int(version) + 1
        new_version = str(new_version)
        new_name = latest_file.rsplit('_', 1)[0]
        hip_name = str(new_name + "_" + new_version)
        filename = os.path.join(path_merge_norm, hip_name) + ".hip"
        hou.hipFile.save(file_name=filename, save_to_recent_files=False)
        hou.hipFile.setName(filename)
        return filename


    else:
        print("path does not exist, will create it for you")
        os.chdir(path_base_norm)
        os.makedirs(path_new_dir)
        # define file_name
        version = str(1)
        hip_name = str(pid + "_" + task_choice + "_" + uid + "_" + version)
        filename = os.path.join(path_merge_norm, hip_name) + ".hip"
        print (filename)
        hou.hipFile.save(file_name=filename, save_to_recent_files=False)
        hou.hipFile.setName(filename)
        return filename
