#-*- coding: utf-8 -*-
sys.path.append('F:/Works/Codes/Git/Maya_Scripts/Mel/Python')
import maya.cmds as cmds
import maya.mel as mel
import os
import sys
import shutil
import time
import re
from YM_ReferenceOperations import *


def abcExportUI():
    if cmds.window('YM_ABC_Export_Window',ex=True):
        cmds.deleteUI('YM_ABC_Export_Window')
    
    cmds.window('YM_ABC_Export_Window',
                title='YM_ABC_Export_Window',
                width=450,
                height=600,
                bgc=[0.27,0.27,0.27],
                sizeable=False)
    #----------------------------------------------------------------------------------------------------------
    cmds.scrollLayout('YM_ABC_Export_BaseLayout',w=450,h=600)
    #----------------------------------------------------------------------------------------------------------
    #Filter Layout
    cmds.frameLayout('YM_ABC_Export_Filter_Layout',label='Group Name',w=450,cl=True,cll=True,parent='YM_ABC_Export_BaseLayout',bgc=[0.05,0.127,0.127])
    cmds.rowLayout(nc=3)
    cmds.textField('YM_ABC_Export_Filter_Input_Field',tx='MOD Model Geo Geometry',w=350)
    cmds.button('YM_ABC_Export_Filter_Add_Button',l='Add',w=40,c=lambda arg:groupFilterAddButtonCmd())
    cmds.button('YM_ABC_Export_Filter_Save_Button',l='Save',w=40,c=lambda arg:groupFilterSaveButtonCmd(),en=False)
    cmds.setParent(u=True)
    cmds.textScrollList('YM_ABC_Export_Filter_List',w=450,h=300)
    cmds.setParent(u=True)
    #Filter Layout
    #----------------------------------------------------------------------------------------------------------
    #Attribute Layout
    cmds.frameLayout('YM_ABC_Export_Attribute_Layout',l='Attributes',w=450,cl=True,cll=True,parent='YM_ABC_Export_BaseLayout',bgc=[0.125,0.27,0.27])
    cmds.rowLayout(nc=3)
    cmds.textField('YM_ABC_Export_Attribute_Input_Field',w=350)
    cmds.button('YM_ABC_Export_Attribute_Add_Button',l='Add',w=40,c=lambda arg:attributeAddButtonCmd())
    cmds.button('YM_ABC_Export_Attribute_Save_Button',l='Save',w=40,en=False)
    cmds.setParent(u=True)
    cmds.textScrollList('YM_ABC_Export_Attribute_List',w=300,h=300)
    cmds.setParent(u=True)
    #Attribute Layout
    #----------------------------------------------------------------------------------------------------------
    #Flags Layout
    cmds.frameLayout('YM_ABC_Export_Flags_Layout',l='Options',w=450,cl=True,cll=True,parent='YM_ABC_Export_BaseLayout',bgc=[0.25,0.5,0.5])
    cmds.columnLayout(co=['both',150])
    cmds.radioCollection()
    cmds.radioButton('YM_ABC_Export_Options_CurrentFrame',l='CurrentFrame',cc=lambda arg:setFrameRange(),sl=False)
    cmds.radioButton('YM_ABC_Export_Options_FrameRange',l='Time Slider',cc=lambda arg:setFrameRange(),sl=True)
    cmds.radioButton('YM_ABC_Export_Options_Manual',l='Manual',sl=False)
    cmds.rowLayout(nc=2)
    cmds.floatField('YM_ABC_Export_Options_StartFrame',value=cmds.playbackOptions(q=True,min=True))
    cmds.floatField('YM_ABC_Export_Options_EndFrame',value=cmds.playbackOptions(q=True,max=True))
    cmds.setParent(u=True)
    cmds.checkBox('YM_ABC_Export_Options_Normal',l='No Normals',value=0)
    cmds.checkBox('YM_ABC_Export_Options_Renderable',l='Renderable Only',value=0)
    cmds.checkBox('YM_ABC_Export_Options_Namespace',l='Strip Namespaces',value=0)
    cmds.checkBox('YM_ABC_Export_Options_WholeGeo',l='Whole Frame Geo',value=0)
    cmds.checkBox('YM_ABC_Export_Options_WorldSpace',l='World Space',value=1)
    cmds.checkBox('YM_ABC_Export_Options_Visibility',l='Visibility',value=1)
    cmds.checkBox('YM_ABC_Export_Options_Crease',l='Creases',value=0)
    cmds.checkBox('YM_ABC_Export_Options_UV',l='UV',value=1)
    cmds.checkBox('YM_ABC_Export_Options_FaceSets',l='Face Sets',value=0)
    cmds.checkBox('YM_ABC_Export_Options_ColorSets',l='Color Sets',value=0)
    cmds.checkBox('YM_ABC_Export_Options_EulerFilter',l='Euler Filter',value=0)
    cmds.checkBox('YM_ABC_Export_Options_Verbose',l='Verbose',value=0)
    cmds.setParent(u=True)
    #Flags Layout
    #----------------------------------------------------------------------------------------------------------
    #Reference Layout
    cmds.frameLayout('YM_ABC_Export_MainLayout',l='Reference',w=450,cl=False,cll=False,parent='YM_ABC_Export_BaseLayout',bgc=[0.5,0.75,0.75])
    #cmds.rowLayout(nc=2)
    cmds.columnLayout()
    cmds.rowLayout(nc=3)
    cmds.checkBox('YM_ABC_Export_Option_Char',l='Char',value=1)
    cmds.checkBox('YM_ABC_Export_Option_Prop',l='Prop',value=0)
    cmds.checkBox('YM_ABC_Export_Option_Sets',l='Sets',value=0)
    cmds.setParent(u=True)
    #cmds.columnLayout()
    cmds.textScrollList('YM_ABC_Export_ReferenceList',w=450,h=450)
    cmds.setParent(u=True)
    cmds.setParent(u=True)
    cmds.columnLayout()
    cmds.rowLayout(nc=4,p='YM_ABC_Export_MainLayout')
    cmds.textField('YM_ABC_Export_Path_Field',tx=os.path.splitext(cmds.file(q=True,loc=True))[0]+'.abc',w=300)
    cmds.button('YM_ABC_Export_Path_Selector_Button',l='File',w=20)
    cmds.radioCollection()
    cmds.radioButton('YM_ABC_Export_Options_SingleFile',l='Single',sl=False)
    cmds.radioButton('YM_ABC_Export_Options_MultipleFile',l='Multiple',sl=True)
    cmds.setParent(u=True)
    cmds.button('YM_ABC_Export_Confirm',l='Click Me',bgc=[0.27,0.54,1])
    cmds.setParent(u=True)
    
    #Reference Layout
    #----------------------------------------------------------------------------------------------------------
    cmds.showWindow('YM_ABC_Export_Window')
    #----------------------------------------------------------------------------------------------------------
    #edit the checkbox command
    cmds.checkBox('YM_ABC_Export_Option_Char',e=True,cc=lambda arg:setReferenceList())
    cmds.checkBox('YM_ABC_Export_Option_Prop',e=True,cc=lambda arg:setReferenceList())
    cmds.checkBox('YM_ABC_Export_Option_Sets',e=True,cc=lambda arg:setReferenceList())
    cmds.radioButton('YM_ABC_Export_Options_SingleFile',e=True,cc=lambda arg:fileNumSwitch())
    cmds.radioButton('YM_ABC_Export_Options_MultipleFile',e=True,cc=lambda arg:fileNumSwitch())
    cmds.textScrollList('YM_ABC_Export_Filter_List',e=True,dcc=lambda :deleteListItem('YM_ABC_Export_Filter_List'))
    cmds.textScrollList('YM_ABC_Export_Attribute_List',e=True,dcc=lambda :deleteListItem('YM_ABC_Export_Attribute_List'))
    cmds.textScrollList('YM_ABC_Export_ReferenceList',e=True,dcc=lambda :deleteListItem('YM_ABC_Export_ReferenceList'))
    cmds.button('YM_ABC_Export_Confirm',e=True,c=lambda arg:exportAbc(),w=50)
    groupFilterAddButtonCmd()

def deleteListItem(list):
    listItem = cmds.textScrollList(list,q=True,si=True)
    if listItem is None:
        return
    cmds.textScrollList(list,e=True,ri=listItem)


def groupFilterAddButtonCmd():
    string = cmds.textField('YM_ABC_Export_Filter_Input_Field',q=True,tx=True)
   
    if string is not None:
        for item in string.split(' '):
            if len(item)==0:
                continue
            existList = cmds.textScrollList('YM_ABC_Export_Filter_List',q=True,ai=True)
            #print existList
            if existList is not None:
                if existList.count(item) == 0:
                    cmds.textScrollList('YM_ABC_Export_Filter_List',e=True,a=item)
                    #print item
            else:
                cmds.textScrollList('YM_ABC_Export_Filter_List',e=True,a=item)
    else:
        return

def groupFilterSaveButtonCmd():
    listItem = cmds.textScrollList('YM_ABC_Export_Filter_List',q=True,ai=True)
    string = ''
    if listItem is None:
        return
    for item in listItem:
        string += item
        string += ' '
    removeSpaceString = string[0:len(string)-1]
    cmds.optionVar(sv=['YM_ABC_OptionVar_FilterString',removeSpaceString])
    return removeSpaceString

def attributeAddButtonCmd():
    string = cmds.textField('YM_ABC_Export_Attribute_Input_Field',q=True,tx=True)
    if len(string.split(' '))>1:
        cmds.error('No Space Allowed')
        return
    existItem = cmds.textScrollList('YM_ABC_Export_Attribute_List',q=True,ai=True)
    if existItem is not None:
        if existItem.count(string)==0:
            cmds.textScrollList('YM_ABC_Export_Attribute_List',e=True,a=string)
        else:
            cmds.error(string + ' is already in the list')
            return
    else:
        cmds.textScrollList('YM_ABC_Export_Attribute_List',e=True,a=string)
    

def getExportFlags():
    flags = ' '
    
    if cmds.checkBox('YM_ABC_Export_Options_Normal',q=True,value=True):
        flags += '-noNormals '
    if cmds.checkBox('YM_ABC_Export_Options_Renderable',q=True,value=True):
        flags += '-renderableOnly '
    if cmds.checkBox('YM_ABC_Export_Options_Namespace',q=True,value=True):
        flags += '-stripNamespaces '
    if cmds.checkBox('YM_ABC_Export_Options_WholeGeo',q=True,value=True):
        flags += '-wholeFrameGeo '
    if cmds.checkBox('YM_ABC_Export_Options_WorldSpace',q=True,value=True):
        flags += '-worldSpace '
    if cmds.checkBox('YM_ABC_Export_Options_Visibility',q=True,value=True):
        flags += '-writeVisibility '
    if cmds.checkBox('YM_ABC_Export_Options_Crease',q=True,value=True):
        flags += '-writeCreases '
    if cmds.checkBox('YM_ABC_Export_Options_UV',q=True,value=True):
        flags += '-uvWrite '   
    if cmds.checkBox('YM_ABC_Export_Options_FaceSets',q=True,value=True):
        flags += '-writeFaceSets ' 
    if cmds.checkBox('YM_ABC_Export_Options_ColorSets',q=True,value=True):
        flags += '-writeColorSets ' 
    if cmds.checkBox('YM_ABC_Export_Options_EulerFilter',q=True,value=True):
        flags += '-eulerFilter '
    if cmds.checkBox('YM_ABC_Export_Options_Verbose',q=True,value=True):
        flags += '-verbose '     

    return flags

def setReferenceList():
    
    referenceNodeList = getLoadedReferenceList()
    checkOptions = []
    if cmds.checkBox('YM_ABC_Export_Option_Char',q=True,value=True):
        checkOptions.append('char')
    if cmds.checkBox('YM_ABC_Export_Option_Prop',q=True,value=True):
        checkOptions.append('prop')
    if cmds.checkBox('YM_ABC_Export_Option_Sets',q=True,value=True):
        checkOptions.append('sets')

    if len(checkOptions) == 0:
        checkOptions.append('.+')
    
    if referenceNodeList is not None:
        referenceFilterList = []
        for referenceNode in referenceNodeList:
            referencePath = cmds.referenceQuery(referenceNode,f=True)
            for checkOption in checkOptions:
                if re.search(checkOption,referencePath) is not None:
                    referenceFilterList.append(referenceNode)
                else:
                    continue
        if referenceFilterList is not None:
            cmds.textScrollList('YM_ABC_Export_ReferenceList',e=True,ra=True)
        for referenceFilterNode in referenceFilterList:    
            cmds.textScrollList('YM_ABC_Export_ReferenceList',e=True,a=referenceFilterNode)
    
def setFrameRange():
    if cmds.radioButton('YM_ABC_Export_Options_CurrentFrame',q=True,sl=True):
        cmds.floatField('YM_ABC_Export_Options_StartFrame',e=True,value=cmds.currentTime(q=True))
        cmds.floatField('YM_ABC_Export_Options_EndFrame',e=True,value=cmds.currentTime(q=True))
    if cmds.radioButton('YM_ABC_Export_Options_FrameRange',q=True,sl=True):
        cmds.floatField('YM_ABC_Export_Options_StartFrame',e=True,value=cmds.playbackOptions(q=True,min=True))
        cmds.floatField('YM_ABC_Export_Options_EndFrame',e=True,value=cmds.playbackOptions(q=True,max=True))

def fileNumSwitch():
    if cmds.radioButton('YM_ABC_Export_Options_SingleFile',q=True,sl=True):
        cmds.textField('YM_ABC_Export_Path_Field',e=True,en=True)
        cmds.button('YM_ABC_Export_Path_Selector_Button',e=True,en=True)
    if cmds.radioButton('YM_ABC_Export_Options_MultipleFile',q=True,sl=True):
        cmds.textField('YM_ABC_Export_Path_Field',e=True,en=False)
        cmds.button('YM_ABC_Export_Path_Selector_Button',e=True,en=False)

def singleFileExportPath():
    filepath = cmds.textField('YM_ABC_Export_Path_Field',q=True,tx=True)
    if filepath == 'unknown.abc':
        cmds.error('Please save the scene before export!')
        return ''

    return filepath

#get the world group
def getWorldGroup(referenceNode):
    relativeNodes = cmds.referenceQuery(referenceNode,nodes=True)
    transformNodes = [node for node in relativeNodes if cmds.nodeType(node)=='transform']
    worldGroup = []
    for transformNode in transformNodes:
        #print transformNode
        if cmds.listRelatives(transformNode,parent=True) is None and cmds.listRelatives(transformNode) is not None:
            worldGroup.append(transformNode)
        else:
            continue
    return worldGroup

def getExportAttributes():
    attributes = cmds.textScrollList('YM_ABC_Export_Attribute_List',q=True,ai=True)

    if attributes is None:
        return ''
    else:
        temp = ''
        for attribute in attributes:
            temp += ' -userAttr ' + attribute
        return temp

def exportArgumentsCreator():
    referenceList = cmds.textScrollList('YM_ABC_Export_ReferenceList',q=True,ai=True)
    #获取列表中的参考节点
    
    if referenceList is None:
            return
    
    argmentsList = []
    argmentsString = ''
    for referenceNode in referenceList:
        argString = ''
        #获取节点下的最高父级transform节点
        worldGroupList = getWorldGroup(referenceNode)
        if len(worldGroupList)==1:
            filterList = cmds.textScrollList('YM_ABC_Export_Filter_List',q=True,ai=True)
            if filterList is None:
                cmds.error('No filter group founded, Please enter one least filter to the group field')
                return
            else:
                #验证transform节点结尾{"MOD","Model","Geometry"}等
                for filterItem in filterList:
                    filterMatch = re.search(filterItem,worldGroupList[0])
                    if filterMatch is None:
                        continue
                    else:
                        #对每个参考节点生成一个root *_MOD字符串
                        argString = '-root |' + worldGroupList[0]
                        argmentsString += '-root |' + worldGroupList[0] + ' '
        else:
            cmds.warning(referenceNode+' has no root group')
        if len(argString)==0:
            continue
        else:
            argString += getExportFlags()
            argString += '-frameRange ' + str(cmds.floatField('YM_ABC_Export_Options_StartFrame',q=True,value=True)) + ' ' + \
                          str(cmds.floatField('YM_ABC_Export_Options_EndFrame',q=True,value=True))
            argString += getExportAttributes()
            #对每个参考节点生成路径，路径为当前目录下新建的ABC目录                             
            currentPath = cmds.file(q=True,loc=True)
            currentDir = os.path.dirname(currentPath)
            
            argString += ' -file ' + currentDir + '/ABC/' + os.path.splitext(os.path.basename(currentPath))[0]+'_' + referenceNode + '.abc'

        argmentsList.append(argString)

    #print argmentsList
        #return argmentsList
        #找到一个即跳出，找到多个即警报，跳出函数
    if cmds.radioButton('YM_ABC_Export_Options_MultipleFile',q=True,sl=True):
        return argmentsList
    elif cmds.radioButton('YM_ABC_Export_Options_SingleFile',q=True,sl=True) and len(argmentsString)>0:
        argmentsString += getExportFlags()
        argmentsString += '-frameRange ' + str(cmds.floatField('YM_ABC_Export_Options_StartFrame',q=True,value=True)) + ' ' + \
                          str(cmds.floatField('YM_ABC_Export_Options_EndFrame',q=True,value=True))
        argmentsString += getExportAttributes()                          
        currentPath = cmds.file(q=True,loc=True)
        currentDir = os.path.dirname(currentPath)
        currentFile = os.path.basename(currentPath)
        
        argmentsString += ' -file ' + currentDir + '/ABC/' + currentFile + '.abc'
        #print argmentsString
        return argmentsString
        #同上
        #将多个root *MOD字符串合并为一个
        #路径使用Path_Field中的字符串

def exportAbc():
    argments = exportArgumentsCreator()

    if type(argments) is list:
        for argment in argments:
            try:
                cmds.AbcExport(j=argment)
            except:
                cmds.warning(argment+' is error,check the scene!')
                continue
    elif type(argments) is str:
        try:
            cmds.AbcExport(j=argment)
        except:
            cmds.warning('Export Error Occurs, Check the scene')

    #flags = getExportFlags()
    #cmds.AbcExport(j='')

def move_History_File(filepath):
    localTime = time.localtime()
    
    formatTime = '_' + str(localTime.tm_year) + '_' \
                     + str(localTime.tm_mon) + '_' \
                     + str(localTime.tm_mday) + '_' \
                     + str(localTime.tm_hour) + '_' \
                     + str(localTime.tm_min)

    filename = os.path.basename(filepath.split('.')[0])
    
    nameList = filepath.split('.')
    fileExt = ''
    if len(nameList)>1:
        for i in range(1,len(nameList)):
            fileExt += '.'
            fileExt += nameList[i]
    
    dirpath = os.path.dirname(filepath)

    filenewname = filename + formatTime + fileExt
    
    if os.path.exists(dirpath+'/history_version') is False:
        os.mkdir(dirpath+'/history_version')

    if os.path.exists(filepath):
        os.rename(filepath,dirpath+'/'+filenewname)
        shutil.move(dirpath+'/'+filenewname,dirpath+'/history_version/'+filenewname)
    

abcExportUI()