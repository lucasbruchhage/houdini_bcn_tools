import hou
import toolutils
import os
import hou
import shutil
import random
import datetime
import webbrowser



def go():
    # Get params
    #hip = hou.expandString('$HIP')
    #normalized_path_hip = os.path.normpath(hip)
    #path_components_hip = normalized_path_hip.split(os.sep)
    #print(normalized_path_hip)


    #get nodes
    obj = hou.node("/obj")
    lops = hou.node("/stage")
    selectedNode = hou.selectedNodes()[0]


    #create nodes
    newGeoNode = selectedNode.createNode("geo")
    newObjMerge = newGeoNode.createNode("object_merge")
    newTransform = newGeoNode.createNode("xform")
    newMaterial = newGeoNode.createNode("material")
    newMatnet = newGeoNode.createNode("matnet")
    newOut = newGeoNode.createNode("output")


    #connect nodes
    newTransform.setInput(0, newObjMerge)
    newOut.setInput(0, newMaterial)
    newMaterial.setInput(0, newTransform)


    #layout nodes
    newGeoNode.layoutChildren()


    #set DisplayFlag
    newOut.setDisplayFlag(True)
    newOut.setRenderFlag(True)


    #set Parms Material Node
    getMatPath = newMaterial.parm("shop_materialpath1")
    getMatPath.set("../matnet1")


    #popup ask multi input 
    choices = [n.path()
            for n in hou.node('/obj/AYON_CONTAINERS').allSubChildren()]
    selected = hou.ui.selectFromTree(choices)
    nodes = [hou.node(p) for p in selected]  
    print("picked:")
    print(nodes)  


    #set Object Merge Path
    nodesPicked = "/obj/AYON_CONTAINERS/" + str(nodes[0])
    getObjPath = newObjMerge.parm("objpath1")
    getObjPath.set(nodesPicked)
    

    #set names
    newOut.setName("OUT")


