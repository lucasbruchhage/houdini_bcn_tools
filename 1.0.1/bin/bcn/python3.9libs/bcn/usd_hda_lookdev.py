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

    #create nodes
    obj = hou.node("/obj")
    lops = hou.node("/stage")
    selectedNode = hou.selectedNodes()[0]
    newGeoNode = selectedNode.createNode("geo")
    newLopImport = newGeoNode.createNode("lopimport::2.0")
    newTransform = newGeoNode.createNode("xform")
    newMaterial = newGeoNode.createNode("material")
    newMatnet = newGeoNode.createNode("matnet")
    newOut = newGeoNode.createNode("output")
    newLopNet = newGeoNode.createNode("lopnet")


    #connect nodes
    newOut.setInput(0, newMaterial)
    newMaterial.setInput(0, newTransform)
    newTransform.setInput(0, newLopImport)

    #layout nodes
    newGeoNode.layoutChildren()

    #set DisplayFlag
    newOut.setDisplayFlag(True)
    newOut.setRenderFlag(True)

    #set Parms Material Node
    getMatPath = newMaterial.parm("shop_materialpath1")
    getMatPath.set("../matnet1")

    #set Parms Lop Import Node
    getPrimPattern = newLopImport.parm("primpattern")
    getPrimPattern.set("%type:Mesh")


    #popup ask multi input
   
    choices = [n.path()
            for n in hou.node('/stage').allSubChildren()]
    selected = hou.ui.selectFromTree(choices)
    nodes = [hou.node(p) for p in selected]  
    print("picked:")
    print(nodes)  

    #set Parms Lop Import Node
    nodesPicked = "../lopnet1/" + str(nodes[0])
    getLopPath = newLopImport.parm("loppath")
    getLopPath.set(nodesPicked)
    
    #move selected nodes to internal LopNet
    hou.moveNodesTo(nodes, newLopNet)

    #set names
    newOut.setName("OUT")


