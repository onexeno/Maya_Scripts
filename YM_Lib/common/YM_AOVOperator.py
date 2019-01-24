#-*- coding: utf-8 -*-

from mtoa import aovs
import maya.cmds as cmds
from YM_ReferenceOperations import *

global YM_TempAOVList

def AOVOperator_Window():
    aovObject = aovs.AOVInterface()

    if cmds.window('YM_AOV_OPERATOR',ex=True):
        cmds.deleteUI('YM_AOV_OPERATOR')
    if cmds.windowPref('YM_AOV_OPERATOR',ex=True):
        cmds.windowPref('YM_AOV_OPERATOR',r=True)
    cmds.window('YM_AOV_OPERATOR',t='YM_AOV_Operator_Window',w=305,h=70)
    cmds.columnLayout('YM_AOV_OPERATOR_LAYOUT')
    cmds.checkBox('YM_AOV_OVERRIDE_CHECKBOX',l='Use Render Layer Override',v=1)
    cmds.separator(h=2,w=308,bgc=[0.0,0.375,0.9],style='none')
    cmds.rowLayout(nc=2)
    cmds.columnLayout()
    cmds.button(l='Enable ALL AOV',c=lambda *args:enableAllAOV(1),w=150,bgc=[0.35,0.15,0.05])
    cmds.button(l='Disable ALL AOV',c=lambda *args:enableAllAOV(0),w=150,bgc=[0.375,0.175,0.05])
    cmds.setParent(u=True)
    cmds.columnLayout()
    cmds.button(l='Del Multiple AOV',c=lambda *args:removeDuplicateAOVs(),w=150,bgc=[0.175,0.375,0.05])
    cmds.button(l='List References',c=lambda *args:listReferences(),w=150,bgc=[0.15,0.375,0.05])
    cmds.setParent(u=True)
    cmds.showWindow('YM_AOV_OPERATOR')

def enableAllAOV(switch):
    if cmds.checkBox('YM_AOV_OVERRIDE_CHECKBOX',q=True,v=True):
        if cmds.getAttr(cmds.editRenderLayerGlobals(crl=True,q=True)+'.global') is False:
            for aov in cmds.ls(type='aiAOV'):
                cmds.editRenderLayerAdjustment(aov+'.enabled',layer=cmds.editRenderLayerGlobals(crl=True,q=True))
                cmds.setAttr(aov+'.enabled',swtich)
        else:
            warning('defaultRenderLayer cannot use the override option !')
    else:
        for aov in cmds.ls(type='aiAOV'):
            cmds.setAttr(aov+'.enabled',switch)

def listReferences():
    if cmds.control('YM_AOV_OPERATOR_LISTLAYOUT',ex=True) == False:
        cmds.rowLayout('YM_AOV_OPERATOR_LISTLAYOUT',nc=2,p='YM_AOV_OPERATOR_LAYOUT')
        cmds.textScrollList('YM_AOV_OPERATOR_REFERENCELIST',sc=lambda *args:refreshRelativeAOVList(),w=152)
        cmds.textScrollList('YM_AOV_OPERATOR_RELATIVEAOVLIST',ams=True,w=152)
        cmds.popupMenu()
        cmds.menuItem(l='Enable Selected AOV',c=lambda *args:AOVListSelectItemToAOVNode(1))
        cmds.menuItem(l='Disable Selected AOV',c=lambda *args:AOVListSelectItemToAOVNode(0))
        cmds.setParent(u=True)

    cmds.textScrollList('YM_AOV_OPERATOR_REFERENCELIST',e=True,ra=True)
    
    for reference in getLoadedReferenceList():
        cmds.textScrollList('YM_AOV_OPERATOR_REFERENCELIST',e=True,a=reference)

def refreshRelativeAOVList():
    global YM_TempAOVList
    YM_TempAOVList = {}
    cmds.textScrollList('YM_AOV_OPERATOR_RELATIVEAOVLIST',e=True,ra=True)
    for item in cmds.textScrollList('YM_AOV_OPERATOR_REFERENCELIST',q=True,si=True):
        tempDict = dict()
        for aiAOV in referenceNodeTypeFilter(cmds.referenceQuery(item,nodes=True),'aiAOV'):
            YM_TempAOVList[aiAOV] = cmds.getAttr(aiAOV+'.name')
            cmds.textScrollList('YM_AOV_OPERATOR_RELATIVEAOVLIST',e=True,a=cmds.getAttr(aiAOV+'.name'))

def AOVListSelectItemToAOVNode(trigger):
    global YM_TempAOVList

    tempItemList = list()
    
    for item in cmds.textScrollList('YM_AOV_OPERATOR_RELATIVEAOVLIST',q=True,si=True):
        for key,value in YM_TempAOVList.items():
            if item == value:
                tempItemList.append(key)
    
    for aov in tempItemList:
        if cmds.checkBox('YM_AOV_OVERRIDE_CHECKBOX',q=True,v=True):
            if cmds.getAttr(cmds.editRenderLayerGlobals(crl=True,q=True)+'.global') is False:
                cmds.editRenderLayerAdjustment(aov+'.enabled')
                cmds.setAttr(aov+'.enabled',trigger)

    return tempItemList

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
        