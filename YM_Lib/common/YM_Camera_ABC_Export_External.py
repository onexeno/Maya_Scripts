#-*- coding: utf-8 -*-
from PySide import QtGui,QtCore
import sys
import os
import re
import time
import maya.standalone
libPath = '//S3/软件库/P_插件目录/YunMan_Toolsets/Common/Python'.decode('utf-8')
if sys.path.count(libPath):
    sys.path.append(libPath)

from YM_ABC_Export_Cmd import *
from YM_Camera_Ops import *

def external_Ops_exportABC(filepath):
    
    try:
        maya.standalone.initialize('python')
    except:
        print 'Cannot initialize the python standalone'
        return 
    
    import pymel.core
    import maya.cmds as cmds

    print 1
    libPath = '//S3/软件库/P_插件目录/YunMan_Toolsets/Common/Python'.decode('utf-8')
    arnoldPath = 'C:/solidangle/mtoadeploy/2016/scripts'
    print 2
    if sys.path.count(libPath) == 0:
        sys.path.append(libPath)
    if sys.path.count(arnoldPath) == 0:
        sys.path.append(arnoldPath)
    print 3   
    try:
        cmds.file(filepath,open=True,f=True)
        print 4
    except:
        print 'Cannot Open the file: ' + filepath
        #maya.standalone.uninitialize()
        return
    
    if cmds.pluginInfo('AbcExport',q=True,loaded=True) is False:
        cmds.loadPlugin('AbcExport')
    if cmds.pluginInfo('mtoa',q=True,loaded=True) is False:
        cmds.loadPlugin('mtoa')
        
    try:
        exportCamera()
        setRenderableCameras()
    except:
        pass
    
    
    #maya.standalone.uninitialize()
    cmds.quit()
    #os._exit(0)
    #sys.exit()
    



class exteranlABC_Exporter(QtGui.QWidget):
    def __init__(self):
        super(exteranlABC_Exporter,self).__init__()

    def initializeUI(self):
        mainLayout = QtGui.QVBoxLayout()

        childLayout1 = QtGui.QHBoxLayout()
        self.textEdit = QtGui.QLineEdit()
        button1 = QtGui.QPushButton('Set Directory')
        #button2 = QtGui.QPushButton('Export All')
        button3 = QtGui.QPushButton('Export Selection')
        childLayout1.addWidget(self.textEdit)
        childLayout1.addWidget(button1)
        #childLayout1.addWidget(button2)
        childLayout1.addWidget(button3)
        mainLayout.addLayout(childLayout1)

        self.textScrollList = QtGui.QListWidget()
        mainLayout.addWidget(self.textScrollList)
        childLayout2 = QtGui.QVBoxLayout()
        self.progressBar = QtGui.QProgressBar()
        self.textLabel = QtGui.QLabel()
        childLayout2.addWidget(self.progressBar)
        childLayout2.addWidget(self.textLabel)
        mainLayout.addLayout(childLayout2)

        button1.clicked.connect(self.fileDialog)
        #button2.clicked.connect(self.export)
        button3.clicked.connect(self.exportSelections)

        self.textScrollList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.setLayout(mainLayout)
    
    def export(self):
        if self.textScrollList.count() == 0:
            return
        itemTempList = []
        for i in range(0,self.textScrollList.count()):
            itemTempList.append(self.textScrollList.item(i))

        self.progressBar.setRange(0,len(itemTempList)-1)
        count = 0

        for item in itemTempList:
            self.textLabel.setText(item.text())
            self.progressBar.setValue(count)
            #self.textScrollList.removeItemWidget(item)
            #print self.textScrollList.count()
            time.sleep(0.5)
            external_Ops_exportABC(item.text())
            count += 1
            
    def exportSelections(self):
        if self.textScrollList.count() == 0:
            return
        tempItems = []
        
        for item in self.textScrollList.selectedItems():
            tempItems.append(item)
        if len(tempItems) == 0:
            return
        
        self.progressBar.setRange(0,len(tempItems)-1)
        count = 0
        
        for tempItem in tempItems:
            print tempItem.text()
            self.textLabel.setText(tempItem.text())
            external_Ops_exportABC(tempItem.text())
            self.progressBar.setValue(count)
            count+=1
            #print tempItem.text()

    def writeLogs(self):
        filepath = ''

    def fileDialog(self):
        qFileDialog = QtGui.QFileDialog()
        #print qFileDialog.FileMode()
        qFileDialog.setFileMode(QtGui.QFileDialog.Directory)
        # qFileDialog.setFileMode(QtGui.QFileDialog.FileMode.Directory)
        #qFileDialog.setOption(QtGui.QFileDialog.ShowDirsOnly,True)
        qFileDialog.setOption(QtGui.QFileDialog.ShowDirsOnly,True)
        #print qFileDialog.FileMode()
        fileUrl = qFileDialog.getExistingDirectory()
        qFileDialog.close()
        fileUrl = fileUrl.replace('\\','/')
        self.textEdit.setText(fileUrl)
        fileList = []
        path = fileUrl.decode('utf-8')
        
        #print path
        
        for i in os.listdir(path):
            if os.path.isdir(path+'/'+i+'/approve') is True:
                filePath = os.listdir(path+'/'+i+'/approve')
                for file in filePath:
                    if re.search('(\.m[a|b]$){1}',file) is not None:
                        fileList.append(path+'/'+i+'/approve/'+file)
                        #print file
                        self.textScrollList.addItem(path+'/'+i+'/approve/'+file)
        #self.textScrollList.addItem('Test')
        #print fileList
        return fileUrl

    def progressBarOps(self):
        pass

app = QtGui.QApplication(sys.argv)
test = exteranlABC_Exporter()
test.initializeUI()
test.show()
app.exec_()

