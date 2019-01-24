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
            
    pattern = cmds.textField('FromPATH',q=True,tx=True).replace('\\','/')
    newpath = cmds.textField('TOPATH',q=True,tx=True).replace('\\','/')
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
        

def YM_Repath_Window():
    if cmds.window('YM_FILEPATH_REPLACER',ex=True):
        cmds.deleteUI('YM_FILEPATH_REPLACER')
    
    cmds.window('YM_FILEPATH_REPLACER',w=600,h=200)
    cmds.rowLayout(nc=3)
    cmds.columnLayout(adj=True)
    cmds.text(l='From:',al='right',h=20)
    cmds.separator(h=2,style='none')
    cmds.text(l='To:',al='right',h=20)
    cmds.setParent(u=True)
    cmds.columnLayout()
    cmds.textField('FromPATH',w=300)
    cmds.separator()
    cmds.textField('TOPATH',w=300)
    cmds.setParent(u=True)
    cmds.rowLayout(nc=2)
    cmds.columnLayout()
    cmds.button(l='Replace',c=lambda *args:replaceString(),w=60,h=20,bgc=[0.45,0.15,0.05])
    cmds.separator()
    cmds.button(l='FTM',c=lambda *args:maya.mel.eval('source "//S3/软件库/P_插件目录/YunMan_Toolsets/Common/YM_FileTextureManager.mel"'),w=60,h=20,bgc=[0.35,0.2,0.05])
    cmds.setParent(u=True)
    cmds.columnLayout()
    cmds.button(l='Not Exists',c=lambda *args:selectNoExistFile(),w=60,h=20,bgc=[0.05,0.35,0.2])
    cmds.separator()
    cmds.button(l='Null',c=lambda *args:selectNullFile(),w=60,h=20,bgc=[0.05,0.45,0.15])
    
    cmds.setParent(u=True)
    cmds.setParent(u=True)
    
    cmds.showWindow('YM_FILEPATH_REPLACER')

