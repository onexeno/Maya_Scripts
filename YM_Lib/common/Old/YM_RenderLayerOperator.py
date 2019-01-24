#-*- coding:utf-8 -*-

import maya.cmds as cmds
import re
import sys
import mtoa.aovs

sys.path.append('I:\\Works\\Codes\\Git\\Maya_Scripts\\Mel\\Python')

from YM_ReferenceOperations import *

def referenceCreatorWindow():
    if cmds.window('ReferenceCreatorWindow',ex=True):
        cmds.deleteUI('ReferenceCreatorWindow')
    
    cmds.window('ReferenceCreatorWindow',t='YM_ReferenceOperatorWindow',w=400,h=400)
    cmds.columnLayout()
    
    cmds.rowLayout(nc=6)
    cmds.checkBox('Sets_ReferenceCheckBox',l='Sets',v=1)
    cmds.checkBox('Props_ReferenceCheckBox',l='Props',v=1)
    cmds.checkBox('Chars_ReferenceCheckBox',l='Chars',v=1)
    cmds.button('YM_CreateRenderLayer_Separate',bgc=[0.1,0.2,0.3],l='Separate',w=70)
    cmds.button('YM_CreateRenderLayer_Combine',bgc=[0.15,0.25,0.35],l='Combine',w=70)
    cmds.button('YM_RemoveDuplicateAOVs',bgc=[0.35,0.25,0.15],l='Rebuild AOVs',w=100)
    
    cmds.setParent(u=True)
    
    cmds.separator(w=400,h=2,style='none',bgc=[0.0,0.2,0.35])
    
    cmds.textScrollList('YM_ReferenceWindow_List',w=400,h=500,ams=True)
  
    cmds.setParent(u=True)
    cmds.showWindow('ReferenceCreatorWindow')

    cmds.checkBox('Sets_ReferenceCheckBox',e=True,cc=lambda *args:refreshReferenceList())
    cmds.checkBox('Props_ReferenceCheckBox',e=True,cc=lambda *args:refreshReferenceList())
    cmds.checkBox('Chars_ReferenceCheckBox',e=True,cc=lambda *args:refreshReferenceList())
    cmds.button('YM_CreateRenderLayer_Separate',e=True,c=lambda *args:createRenderLayer(True))
    cmds.button('YM_CreateRenderLayer_Combine',e=True,c=lambda *args:createRenderLayer(False))
    cmds.button('YM_RemoveDuplicateAOVs',e=True,c=lambda *args:removeDuplicateAOVs())
    refreshReferenceList()

def refreshReferenceList():
    cmds.textScrollList('YM_ReferenceWindow_List',e=True,ra=True)
    for reference in getLoadedReferenceList():
        if cmds.checkBox('Sets_ReferenceCheckBox',q=True,v=True) and checkReferenceTypeByPath(cmds.referenceQuery(reference,filename=True),'([s|S]ets){1}'):
            cmds.textScrollList('YM_ReferenceWindow_List',e=True,a=reference)
        if cmds.checkBox('Props_ReferenceCheckBox',q=True,v=True) and checkReferenceTypeByPath(cmds.referenceQuery(reference,filename=True),'([p|P]rops){1}'):
            cmds.textScrollList('YM_ReferenceWindow_List',e=True,a=reference)
        if cmds.checkBox('Chars_ReferenceCheckBox',q=True,v=True) and checkReferenceTypeByPath(cmds.referenceQuery(reference,filename=True),'([c|C]hars){1}'):
            cmds.textScrollList('YM_ReferenceWindow_List',e=True,a=reference)

def getFormatFilename(filepath):
    filename = re.search('([^<>/\\\|:""\*\?]+)\.\w+$',filepath)
    extensionName = re.search('(\.\w+){0,}$',filename.string[filename.start():filename.end()])
    pureName = filename.string[filename.start():filename.end()-len(extensionName.string[extensionName.start():extensionName.end()])]
    filenameList = pureName.split('_')
    return filenameList

def createRenderLayer(trigger):
    if cmds.textScrollList('YM_ReferenceWindow_List',q=True,si=True) is None:
        cmds.warning('Select Some Reference Name!!!')
        return
    if trigger is True:
        for reference in cmds.textScrollList('YM_ReferenceWindow_List',q=True,si=True):
            referenceRelativeNodes = cmds.referenceQuery(reference,nodes=True,dp=True)
            if len(referenceRelativeNodes) == 0:
                continue      
            visibleTransforms = list()
            
            for transform in referenceNodeTypeFilter(referenceRelativeNodes,'transform'):
                if cmds.objExists(transform) is False:
                    continue
                if cmds.getAttr(transform+'.visibility'):
                    visibleTransforms.append(transform)
            
            if len(visibleTransforms) == 0:
                continue
            filenameList = getFormatFilename(cmds.referenceQuery(reference,filename=True,wcn=True))
            
            referenceLayer = cmds.createRenderLayer(e=True,n=filenameList[1])
            cmds.editRenderLayerMembers(referenceLayer,visibleTransforms)
    else:
        visibleTransforms = list()
        for reference in cmds.textScrollList('YM_ReferenceWindow_List',q=True,si=True):
            referenceRelativeNodes = cmds.referenceQuery(reference,nodes=True,dp=True)
            if len(referenceRelativeNodes) == 0:
                continue

            for transform in referenceNodeTypeFilter(referenceRelativeNodes,'transform'):
                if cmds.objExists(transform) is False:
                    continue
                if cmds.getAttr(transform+'.visibility'):
                    visibleTransforms.append(transform)
            
        if len(visibleTransforms) == 0:
            return
            
        referenceLayer = cmds.createRenderLayer(e=True,n='ChangeMyName')
        cmds.editRenderLayerMembers(referenceLayer,visibleTransforms)

def removeDuplicateAOVs():
    myAOV = mtoa.aovs.AOVInterface()

    duplicateAOVs = list()

    for aov in myAOV.getAOVs(group=True):
        if len(aov[1])>1:
            #for nodes in myAOV.getAOVNodes(aov[0]):
                #print nodes
            #print aov[0]
            duplicateAOVs.append(aov[0])

    if len(duplicateAOVs) == 0:
        duplicateAOVs = ['']

    else:
        myAOV.removeAOVs(duplicateAOVs)
        for newaov in duplicateAOVs:
            myAOV.addAOV(newaov)
        

referenceCreatorWindow()




