import hou
import toolutils
import os
import shutil
import random
import datetime
import webbrowser
import time


def go():
    

    obj = hou.node("/obj")
    lops = hou.node("/stage")
    rops = hou.node("/out")
    selectedNode = hou.selectedNodes()[0]
    

    #set Parms obj merge
    getRsEasyMode = selectedNode.parm("RS_easyMode")
    getRsEasyMode.set(2)

    getParam = selectedNode.parm("MotionBlurEnabled")
    getParam.set(True)

    getParam = selectedNode.parm("MotionBlurDeformationEnabled")
    getParam.set(True)

    getParam = selectedNode.parm("EnableAutomaticSampling")
    getParam.set(False)

    getParam = selectedNode.parm("UnifiedRandomizePattern")
    getParam.set(False)

    getParam = selectedNode.parm("RS_denoisingEnabled")
    getParam.set(True)

    getParam = selectedNode.parm("SecondaryGIEngine2")
    getParam.set(1)

    getParam = selectedNode.parm("NumGIBounces2")
    getParam.set(2)

    getParam = selectedNode.parm("AbortOnLicenseFail")
    getParam.set(True)

    getParam = selectedNode.parm("AbortOnMissingResource")
    getParam.set(True)

    getParam = selectedNode.parm("AbortOnHoudiniCookingError")
    getParam.set(True)









