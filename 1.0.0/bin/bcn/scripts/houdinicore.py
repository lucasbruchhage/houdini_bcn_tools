import PID_popup as pop
import hou
import getpass
import os
pop.show()

username = getpass.getuser()
# Setting context to skip this line when starting houdini in a render worker to avoid incorrect user name

UID_path = "/mnt/production/user/{}/".format(username.split('@')[0])
if 'CONTEXT' in os.environ and os.environ['CONTEXT'] == 'workstation':
    hou.hscript("set -g UID = {}".format(username.split('@')[0]))

hou.hscript("set -g ULC = /mnt/production/user")

hou.hscript("set -g PRJ = /mnt/production/project")

hou.hscript("set -g LIB = /mnt/production/resources/houdini")

hou.hscript("set -g SCR = /mnt/production/scratch")


start_frame = float(1001)
end_frame = float(1601)
setGobalFrangeExpr = "tset `({0}-1)/$FPS` `{1}/$FPS`".format(start_frame,end_frame)
hou.hscript(setGobalFrangeExpr)
hou.playbar.setFrameRange(start_frame, end_frame)
