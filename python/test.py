from PySide2 import QtCore,QtGui,QtWidgets

import sys

mainWidget = QtWidgets.QApplication(sys.argv)

class myWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.initUI()


    def initUI(self):
        self.mainLayout = QtWidgets.QGridLayout()
        self.testButton = QtWidgets.QPushButton("Click Me")
        
        self.groupBox = QtWidgets.QGroupBox()
        self.groupBox.setTitle("Group Box")
        self.groupBox.setFlat(True)
        self.groupLayout = QtWidgets.QGridLayout()
        
        #textDoc = QtGui.QTextDocument("Nothing to do")
        #textEdit = QtWidgets.QTextBrowser()
        self.textEdit = QtWidgets.QListWidget()
#        self.textEdit.connect(lambda:print("a"),SIGNAL("clicked()"))
        self.groupLayout.addWidget(self.textEdit)
        self.groupBox.setLayout(self.groupLayout)
        
        
        self.mainLayout.addWidget(self.testButton)
        self.mainLayout.addWidget(self.groupBox)
        
        self.testButton.clicked.connect(lambda :self.textListData('testt'))
        self.textEdit.itemDoubleClicked.connect(lambda :self.textListData('te'))
        self.setLayout(self.mainLayout)

    def textListData(self,item):
        self.textEdit.addItem(item)
        
    def updateList(self):
        pass        
        

#class extlistWidget(QtWidgets.QListWidget):

d = myWindow()

d.show()
mainWidget.exec_()
