
#-*- coding: utf-8 -*-

import maya.cmds as cmds
import re
import os

def replaceString():
    nullFilepath = list()
    filepathDict = dict() 

    for file in cmds.ls(type='file'):
        filepath = cmds.getAttr(file+'.fileTextureName')
        if len(filepath)==0:
            nullFilepath.append(file)
        else:
            filepathDict[file] = filepath
            
    pattern = cmds.textFieldGrp('oldPathString',q=True,tx=True).replace('\\','/')
    newpath = cmds.textFieldGrp('newPathString',q=True,tx=True).replace('\\','/')
    for validFile in filepathDict.keys():
        #print filepathDict.get(validFile)
        lookup = re.search(pattern,filepathDict.get(validFile))
        if lookup is None:
            continue
        
        newString = newpath + lookup.string[lookup.end():len(lookup.string)]
        #print newString
        settedColorSpace = cmds.getAttr(validFile+'.colorSpace')
        cmds.setAttr(validFile+".fileTextureName",newString,type='string')
        cmds.setAttr(validFile+'.colorSpace',settedColorSpace,type='string')
    
def selectNullFile():
    nullList = list()
    for file in cmds.ls(type='file'):
        if len(cmds.getAttr(file+'.fileTextureName'))==0:
            nullList.append(file)
    cmds.select(nullList,r=True)

def selectNoExistFile():
    notExists = list()
    for file in cmds.ls(type='file'):
        filepath = cmds.getAttr(file+'.fileTextureName')
        if len(filepath)==0:
            continue
        if os.path.exists(filepath) is False:
            notExists.append(file)
    cmds.select(notExists,r=True)
        

if cmds.window('FilepathReplacer',ex=True):
    cmds.deleteUI('FilepathReplacer')

cmds.window('FilepathReplacer',w=600,h=200)
cmds.columnLayout()
cmds.textFieldGrp('oldPathString',l='oldPathString',w=500)
cmds.textFieldGrp('newPathString',l='newPathString',w=500)
cmds.rowLayout(nc=3)
cmds.button(l='Replace',c=lambda *args:replaceString(),w=60)
cmds.button(l='Null',c=lambda *args:selectNullFile(),w=60)
cmds.button(l='No Exist',c=lambda *args:selectNoExistFile(),w=60)
cmds.setParent(u=True)

cmds.showWindow('FilepathReplacer')

