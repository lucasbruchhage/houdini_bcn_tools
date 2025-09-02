import shutil
import os
import hou

KB = 1024
MB = 1024 * KB
GB = 1024 * MB
TB = 1024 * GB




def get_size(path):
    getsize = shutil.disk_usage(path).free / TB
    sizestring = str(round(getsize, 2))
    return sizestring


    

#------------------------- MAIN -----------------------------    
scratch_size = (get_size('/mnt/production/project'))
user_size = (get_size('/mnt/production/user'))

message = ("----FREE SPACE----" + "\n" + "PROJECT: " + scratch_size + " TB" + "\n" "USER: " + user_size + " TB")
hou.ui.displayMessage(message)
