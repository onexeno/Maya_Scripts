import re
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
import sys
import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI
import shiboken2

mainWindow = shiboken2.wrapInstance(long(OpenMayaUI.MQtUtil.mainWindow()),QtWidgets.QWidget)

class myWindow(QtWidgets.QWidget):
    def __init__(self):
        super(myWindow,self).__init__()
    
    def initialze(self):
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.textBlankString = QtWidgets.QTextEdit()
        self.textBlankExpr = QtWidgets.QTextEdit()
        self.textBlankResult = QtWidgets.QTextEdit()
        self.mainLayout.addWidget(self.textBlankString)
        self.mainLayout.addWidget(self.textBlankExpr)   
        self.mainLayout.addWidget(self.textBlankResult)

        self.textBlankExpr.setText()
        self.setLayout(self.mainLayout)
    
    def regexPattern(self):
        self.textBlankExpr
    def regexResult(self):
        
    

widgetInstance = myWindow()
widgetInstance.initialze()
widgetInstance.show()




pattern = '(?!C:/).+'
string = 'C:/Windows/x110/wdani_da.dada'

matchResult = re.search(pattern,string)



if matchResult is None:
    print 1
else:   
    print matchResult.string[matchResult.start():matchResult.end()]

