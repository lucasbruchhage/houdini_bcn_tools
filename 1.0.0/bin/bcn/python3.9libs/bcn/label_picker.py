import hou
import os
from PySide2 import QtCore, QtUiTools, QtWidgets
import re


# Get params
lbtpath = hou.expandString('$BCN')
lbtpath = os.path.normpath(lbtpath)
#print(lbtpath)
uipath = lbtpath + "/config/ui/test.ui"
uipath = os.path.normpath(uipath)
#print(uipath)
selected = hou.selectedNodes()
#define colors
#https://www.tydac.ch/color/
red = hou.Color((0.91,0.11,0.12))
green = hou.Color((0.63,0.91,0.11))
yellow = hou.Color((0.91,0.78,0.11))
black = hou.Color((0.06,0.06,0.08))
purple = hou.Color((0.65,0.43,0.7))


# make a pattern
pattern = ["SETUP", "RENDER"]

class pywindow(QtWidgets.QWidget):
    def __init__(self):
        super(pywindow,self).__init__()
        ui_file = uipath
        self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)


    # Setup "Create Geometry" button
        self.ui.setup.clicked.connect(self.buttonClicked_setup)
        self.ui.renderb.clicked.connect(self.buttonClicked_render)
        self.ui.matte.clicked.connect(self.buttonClicked_matte)
        self.ui.lights.clicked.connect(self.buttonClicked_lights)
        self.ui.sim.clicked.connect(self.buttonClicked_sim)

    def buttonClicked_setup(self):
        for node in hou.selectedNodes():
            nodename = (node.name())
            if re.search('RNDR|SETUP|MATTE|LGT|SIM', nodename):
                nodename = nodename.split("_")
                nodename = nodename[1:]
                nodename = '_'.join(nodename)
                print(nodename)
                node.setName("SETUP_" + nodename)
                node.setColor(green)
            else:    
                node.setName("SETUP_" + nodename)
                node.setColor(green)


    def buttonClicked_render(self):
        for node in hou.selectedNodes():
            nodename = (node.name())
            if re.search('RNDR|SETUP|MATTE|LGT|SIM', nodename):
                nodename = nodename.split("_")
                nodename = nodename[1:]
                nodename = '_'.join(nodename)
                print(nodename)
                node.setName("RNDR_" + nodename)
                node.setColor(red)
            else:    
                node.setName("RNDR_" + nodename)
                node.setColor(red)


    def buttonClicked_matte(self):
        for node in hou.selectedNodes():
            nodename = (node.name())
            if re.search('RNDR|SETUP|MATTE|LGT|SIM', nodename):
                nodename = nodename.split("_")
                nodename = nodename[1:]
                nodename = '_'.join(nodename)
                print(nodename)
                node.setName("MATTE_" + nodename)
                node.setColor(black)
            else:    
                node.setName("MATTE_" + nodename)
                node.setColor(black)


    def buttonClicked_lights(self):
        for node in hou.selectedNodes():
            nodename = (node.name())
            if re.search('RNDR|SETUP|MATTE|LGT|SIM', nodename):
                nodename = nodename.split("_")
                nodename = nodename[1:]
                nodename = '_'.join(nodename)
                print(nodename)
                node.setName("LGT_" + nodename)
                node.setColor(yellow)
            else:    
                node.setName("LGT_" + nodename)
                node.setColor(yellow)


    def buttonClicked_sim(self):
        for node in hou.selectedNodes():
            nodename = (node.name())
            if re.search('RNDR|SETUP|MATTE|LGT|SIM', nodename):
                nodename = nodename.split("_")
                nodename = nodename[1:]
                nodename = '_'.join(nodename)
                print(nodename)
                node.setName("SIM_" + nodename)
                node.setColor(purple)
            else:    
                node.setName("SIM_" + nodename)
                node.setColor(purple)

win = pywindow()
win.show()