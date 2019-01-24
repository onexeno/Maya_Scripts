#-*- coding: utf-8 -*-
import maya.standalone as standalone
import maya.cmds as cmds
import sys


defaultPath = '//S3/软件库/P_插件目录/YunMan_Toolsets/Common/Python'

if sys.path.count(defaultPath) == 0:
    sys.path.append(defaultPath)

from PySide2 import QtWidgets,QtCore,QtGui
from YM_ReferenceOperations import *
from YM_Group_Analyzer import *
from YM_ABC_Export_Cmd import *

class myWindow(QtWidgets.QWidget):
    def __init__(self):
        super(myWindow,self).__init__()

    def initialize(self):    
        self.layout = QtWidgets.QHBoxLayout()
        self.button1 = QtWidgets.QPushButton('OpenFile')
        self.button2 = QtWidgets.QPushButton('Export_Abc')
        self.lineEdit1 = QtWidgets.QLineEdit('F:/test.mb')
        
        self.layout.addWidget(self.button1)

        self.layout.addWidget(self.lineEdit1)
        self.layout.addWidget(self.button2)
        self.setLayout(self.layout)
        self.button1.clicked.connect(self.buttonCmd)
        self.button1.clicked.connect(self.buttonCmd2)

    def buttonCmd(self):
        openPythonStandalone(self.lineEdit1.text())
    def buttonCmd2(self):
        Export_Abc()
        
def openPythonStandalone(filepath):
    try:
        standalone.initialize(name='python')
        cmds.file(filepath,open=True)
        cmds.loadPlugin('AbcExport')
        cmds.loadPlugin('mtoa')
    except:
        return
    
def Export_Abc():
    exportCamera()
    exportAbcCmd()
    maya.standalone.uninitialize()
    cmds.quit()
    exit()    
    
#print dir(standalone.uninitialize)

app = QtWidgets.QApplication(sys.argv)
window = myWindow()
window.initialize()
window.show()

app.exec_()
sys.exit(app)

#if __name__ == '__main__':
   

