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

    #ask name
    #popup ask multi input
    values = hou.ui.readInput(
    "Give me a name please",
    buttons=("OK", "Cancel"),
    severity=hou.severityType.Message,
    title="Setup Name",
    default_choice=0, 
    close_choice=-1,
    initial_contents=None,
    )
    SetupName = str(values[1])


    #set node env
    obj = hou.node("/obj")
    lops = hou.node("/stage")
    selectedNode = hou.selectedNodes()[0]


    #create nodes
    newGeoNode = obj.createNode("geo")
    newBlastNode = newGeoNode.createNode("blast")
    newAttribWrangleA = newGeoNode.createNode("attribwrangle")
    newAttribWrangleB = newGeoNode.createNode("attribwrangle")
    newLopImport = newGeoNode.createNode("object_merge")
    newTransform = newGeoNode.createNode("xform")
    newObjectMerge = newGeoNode.createNode("object_merge")
    newAttCopy = newGeoNode.createNode("attribcopy")
    newOut = newGeoNode.createNode("output")
    #newLopNet = newGeoNode.createNode("lopnet")
    newPointVel = newGeoNode.createNode("pointvelocity")


    #connect nodes
    newOut.setInput(0, newPointVel)
    newPointVel.setInput(0, newAttCopy)
    newAttCopy.setInput(0, newAttribWrangleA)
    newAttCopy.setInput(1, newAttribWrangleB)
    newAttribWrangleA.setInput(0, newBlastNode)
    newBlastNode.setInput(0, newTransform)
    newTransform.setInput(0, newLopImport)
    newAttribWrangleB.setInput(0, newObjectMerge)
    








    #layout nodes
    newGeoNode.layoutChildren()


    #set DisplayFlag
    newOut.setDisplayFlag(True)
    newOut.setRenderFlag(True)


    #popup ask multi input 
    choices = [n.path()
            for n in hou.node('/obj/AYON_CONTAINERS').allSubChildren()]
    selected = hou.ui.selectFromTree(choices)
    nodes = [hou.node(p) for p in selected]  
    print("picked:")
    print(nodes)  


    #set Parms Lop Import Node
    nodesPicked = "/obj/AYON_CONTAINERS/" + str(nodes[0])
    getLopPath = newLopImport.parm("objpath1")
    getLopPath.set(nodesPicked)


    #set Parms obj merge
    nodesSelected = "/obj/AYON_CONTAINERS/" + str(selectedNode) + "/geo1/OUT"
    getObjPath = newObjectMerge.parm("objpath1")
    getObjPath.set(nodesSelected)


    #set Parms AttCopy
    getAttName = newAttCopy.parm("attribname")
    getAttName.set("shop_materialpath")
    getAttName = newAttCopy.parm("srcgrouptype")
    getAttName.set(2)
    getAttName = newAttCopy.parm("destgrouptype")
    getAttName.set(2)
    getAttName = newAttCopy.parm("matchbyattribute")
    getAttName.set(1)
    getAttName = newAttCopy.parm("attributetomatch")
    getAttName.set("name")
    getAttName = newBlastNode.parm("group")
    getAttName.set("@path=*CTRL*")

    getAttName = newAttribWrangleA.parm("snippet")
    vex_code = """\
        string parts[] = split(s@path, "/");
        s@name = parts[len(parts) - 1];
        """
    getAttName.set(vex_code)

    getAttName = newAttribWrangleB.parm("snippet")
    getAttName.set(vex_code)
    getAttName = newAttribWrangleB.parm("class")
    getAttName.set(1)
    getAttName = newAttribWrangleA.parm("class")
    getAttName.set(1)


    #set names
    newOut.setName("OUT")
    newGeoNode.setName("SETUP_" + SetupName)


    #set colors
    newGeoNode.setColor(hou.Color((0.537,0.819,0.309)))


    #Create_Render_Node
    newRenderGeoNode = obj.createNode("geo")
    newRenderGeoNode.setName("RNDR_" + SetupName)
    newRenderGeoNode.setColor(hou.Color((0.937,0.219,0.309)))
    newRenderObjMerge = newRenderGeoNode.createNode("object_merge")
    #set Parms obj merge
    getRenderObjPath = newRenderObjMerge.parm("objpath1")
    getRenderObjPath.set("../../SETUP_" + SetupName + "/OUT")
    newGeoNode.setDisplayFlag(False)

    









