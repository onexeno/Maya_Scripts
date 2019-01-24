#-*- coding: utf-8 -*-
import os
import sys
import re
import shutil
import time
import maya.standalone

from PySide import QtGui,QtCore

def replaceString():
    nullFilepath = list()
    filepathDict = dict() 

    for file in cmds.ls(type='file'):
        filepath = cmds.getAttr(file+'.fileTextureName')
        if len(filepath)==0:
            nullFilepath.append(file)
        else:
            filepathDict[file] = filepath

    
    filepath = os.path.dirname(cmds.file(q=True,loc=True))
    infoFile = open(filepath+'/_info_.txt','w+')

    pattern = '(//s2/projects/jxb_season2){1}'
    newpath = 'J:'
    
    for validFile in filepathDict.keys():
        #print filepathDict.get(validFile)
        infoFile.write(validFile + ' : ')

        lookup = re.search(pattern,filepathDict.get(validFile),re.I)
        if lookup is None:
            infoFile.write(' Null : Null ' + '\n')
            continue
        newString = newpath + lookup.string[lookup.end():len(lookup.string)]
        
        #print newString
        settedColorSpace = cmds.getAttr(validFile+'.colorSpace')
        cmds.setAttr(validFile+".fileTextureName",newString,type='string')
        cmds.setAttr(validFile+'.colorSpace',settedColorSpace,type='string')
        infoFile.write(lookup.string + ' : ' + newString + '\n')
    infoFile.close()
    
def external_Ops_ReplaceString(filepath):
    timeVar = str(time.localtime().tm_year) + '_' + str(time.localtime().tm_mon) + '_' +str(time.localtime().tm_mday)
    newpath = os.path.dirname(filepath)+'/history'
    if os.path.exists(newpath) is False:
        os.mkdir(newpath)
    filename = os.path.basename(filepath)
    shutil.copy(filepath,newpath+'/'+filename + '_'+timeVar)
    #os.rename(newpath+'/'+filename,newpath+'/'+filename+'_'+timeVar)

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
        cmds.file(filepath,open=True,prompt=True,f=True)
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
        replaceString()
    except:
        pass
    
    #maya.standalone.uninitialize()
    cmds.file(s=True)
    cmds.quit()
    #os._exit(0)
    #sys.exit()


class exteranlABC_Exporter(QtGui.QWidget):
    def __init__(self):
        super(exteranlABC_Exporter,self).__init__()

    def initializeUI(self):
        mainLayout = QtGui.QVBoxLayout()

        #oldStringEdit = QtGui.QLineEdit()
        #newStringEdit = QtGui.QLineEdit()

        #mainLayout.addWidget(oldStringEdit)
        #mainLayout.addWidget(newStringEdit)

        childLayout1 = QtGui.QHBoxLayout()
        self.textEdit = QtGui.QLineEdit()
        button1 = QtGui.QPushButton('Select Directory')
        #button2 = QtGui.QPushButton('Export All')
        button3 = QtGui.QPushButton('Replace Selection')

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
    
        for i,j,k in os.walk(fileUrl):
            #print j
            if (re.search("approve",i)) is None:
                continue
            for file in k:
                if (re.search('rig_ok\.m[b|a]$',file,re.I)) is None:
                    continue
                #print i + '\\' + files
                self.textScrollList.addItem(i.replace('\\','/')+'/'+file)
            

    
        #self.textScrollList.addItem('Test')
        #print fileList
        return fileUrl

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
            external_Ops_ReplaceString(tempItem.text())
            self.progressBar.setValue(count)
            count+=1
            #print tempItem.text()




app = QtGui.QApplication(sys.argv)
test = exteranlABC_Exporter()
test.initializeUI()
test.show()
app.exec_()