#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

import hou
import os




class LayoutTool(QtWidgets.QWidget):

    def getHoudiniMainWindow():
        """Get the Houdini main window.

        Returns:
            PySide2.QtWidgets.QWidget: 'QWidget' Houdini main window.
        """
        return hou.qt.mainWindow()

    def __init__(self):
        super(LayoutTool, self).__init__(hou.qt.mainWindow())

        print("TESTING")

        self.setWindowTitle("Select Current Project")
        self.setWindowFlags(QtCore.Qt.Dialog)

        stylesheet = hou.qt.styleSheet()
        self.setStyleSheet(stylesheet)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.list_wdg = QtWidgets.QListWidget()
        # self.list_wdg.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.populate()

        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.close_btn = QtWidgets.QPushButton("Close")

    def populate(self):

        """
        Create all the widgets
        """
        self.list_wdg.clear()
        projects_names = os.listdir('/mnt/production/project')
        self.list_wdg.addItems(projects_names)




    def create_layout(self):
        """
        Create all the layouts from the window
        """
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.list_wdg)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)



    def create_connections(self):
        """
        Create all the connections from the buttons
        """
        self.apply_btn.clicked.connect(self.apply_project_variable)
        self.refresh_btn.clicked.connect(self.populate)
        self.close_btn.clicked.connect(self.close)

    def apply_project_variable(self):
        
        item = self.list_wdg.selectedItems()[0].text()
        hou.hscript("set -g PID = {}".format(item))
        hou.ui.displayMessage("Selected Project: {0}".format(item))
        print("Selected Project: {0}".format(item))

        self.close()




_ui = None
def show():
	try: 
		global _ui
		if _ui is None:
			_ui = LayoutTool()
		_ui.show()
	except: 
		pass



