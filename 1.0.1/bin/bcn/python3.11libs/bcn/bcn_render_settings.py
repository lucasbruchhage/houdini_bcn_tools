import hou
import toolutils
import os
import shutil
import random
import datetime
import webbrowser
import time
import json


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

    getParam = selectedNode.parm("RS_outputMultilayerMode")
    getParam.revertToDefaults()

    getParam = selectedNode.parm("RS_aovMultipart")
    getParam.set(True)


    #getParam = selectedNode.parm("RS_aovGetFromNode")
    #getParam.set("../BCN_AOV")

    
    # getParam = selectedNode.parm("RS_aov")
    # getParam.insertMultiParmInstance(0)
    # getParam = selectedNode.parm("RS_aovID_1")
    # getParam.set(5)
    # getParam = selectedNode.parm("RS_aovMaterialDenoise_1")
    # getParam.set(True)

    # getParam = selectedNode.parm("RS_aov")
    # getParam.insertMultiParmInstance(1)
    # getParam = selectedNode.parm("RS_aovID_2")
    # getParam.set(7)
    # getParam = selectedNode.parm("RS_aovMaterialDenoise_2")
    # getParam.set(True)


    multiParm = selectedNode.parm("RS_aov")
    multiParm.set(0)
    file_dir = "/mnt/studio/pipeline/packages/houdini_bcn_tools/1.0.1/bin/bcn/python3.9libs/bcn/aov_base.json"
    data = {}
    with open(file_dir) as outfile:
        data = json.load(outfile)

    blocks = data["aovs"]
    for i in range(len(blocks)):
        multiParm.insertMultiParmInstance(i)

        for name, value in blocks[i].items():
            selectedNode.parm(name).set(value)

    #add_custom_aov()


def add_custom_aov():

    # Define the gallery preset name
    preset_name = 'BCN_custom_AOV'

    # Access the user gallery path
    gallery_path = "/mnt/studio/pipeline/packages/houdini_bcn_tools/1.0.1/bin/bcn/gallery"

    # Define Context
    out_context = hou.node("/out")

    # Create a new node, for example, a 'geometry' node
    new_node = out_context.createNode('geometry', 'BCN_custom_AOV')





    














        











