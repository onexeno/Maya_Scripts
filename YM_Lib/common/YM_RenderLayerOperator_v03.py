#-*- coding:utf-8 -*-

import maya.cmds as cmds
import re
import sys
import mtoa.aovs

from YM_ReferenceOperations import *
from YM_AOVOperator import *

def referenceCreatorWindow():
    if cmds.window('ReferenceCreatorWindow',ex=True):
        cmds.deleteUI('ReferenceCreatorWindow')
    
    cmds.window('ReferenceCreatorWindow',t='YM_ReferenceOperatorWindow',w=400,h=400)
    cmds.columnLayout()
    
    cmds.rowLayout(nc=6)
    cmds.checkBox('Sets_ReferenceCheckBox',l='Sets',v=0)
    cmds.checkBox('Props_ReferenceCheckBox',l='Props',v=1)
    cmds.checkBox('Chars_ReferenceCheckBox',l='Chars',v=1)
    cmds.button('YM_CreateRenderLayer_Separate',bgc=[0.1,0.2,0.3],l='Separate',w=70)
    cmds.button('YM_CreateRenderLayer_Combine',bgc=[0.15,0.25,0.35],l='Combine',w=70)
    cmds.button('YM_AOVOperation',bgc=[0.35,0.25,0.15],l='AOV Operation',w=100)
    
    cmds.setParent(u=True)
    
    cmds.separator(w=400,h=2,style='none',bgc=[0.0,0.2,0.35])
    cmds.rowLayout(nc=6)
    cmds.checkBox('Mesh_ReferenceCheckBox',l='Mesh',v=1)
    cmds.checkBox('Curve_ReferenceCheckBox',l='nurbsCurve',v=1)
    cmds.checkBox('Particle_ReferenceCheckBox',l='Particle',v=1)
    cmds.checkBox('Fluid_ReferenceCheckBox',l='Fluid',v=1)
    #cmds.checkBox('Light_ReferenceCheckBox',l='Light',v=1)
    cmds.setParent(u=True)
    cmds.textScrollList('YM_ReferenceWindow_List',w=400,h=500,ams=True)
  
    cmds.setParent(u=True)
    cmds.showWindow('ReferenceCreatorWindow')

    cmds.checkBox('Sets_ReferenceCheckBox',e=True,cc=lambda *args:refreshReferenceList())
    cmds.checkBox('Props_ReferenceCheckBox',e=True,cc=lambda *args:refreshReferenceList())
    cmds.checkBox('Chars_ReferenceCheckBox',e=True,cc=lambda *args:refreshReferenceList())
    cmds.button('YM_CreateRenderLayer_Separate',e=True,c=lambda *args:createRenderLayer(True))
    cmds.button('YM_CreateRenderLayer_Combine',e=True,c=lambda *args:createRenderLayer(False))
    cmds.button('YM_AOVOperation',e=True,c=lambda *args:AOVOperator_Window())
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

def findRenderableObjects(referenceNode):
    renderableObjectTypes = list()
    if cmds.checkBox('Mesh_ReferenceCheckBox',q=True,v=True):
        renderableObjectTypes.append('mesh')
    if cmds.checkBox('Curve_ReferenceCheckBox',q=True,v=True):
        renderableObjectTypes.append('nurbsCurve')
    if cmds.checkBox('Particle_ReferenceCheckBox',q=True,v=True):
        renderableObjectTypes.append('particle')
    if cmds.checkBox('Fluid_ReferenceCheckBox',q=True,v=True):
        renderableObjectTypes.append('fluid')
    #if cmds.checkBox('Light_ReferenceCheckBox',q=True,v=True):
    #   renderableObjectTypes.append('light')
    
    renderableObjects = list()
    referenceNodes = cmds.referenceQuery(referenceNode,nodes=True,dp=True)
    if len(referenceNodes) == 0:
        return ['']
    for objectType in renderableObjectTypes:
        for shape in referenceNodeTypeFilter(referenceNodes,objectType):
            if cmds.objExists(shape) is False:
                continue
            if cmds.getAttr(shape+'.intermediateObject') == 1:
                continue
            if cmds.getAttr(shape+'.visibility') == 0:
                continue
            if cmds.getAttr(shape+'.template') == 1:
                continue
            renderableObjects.append(shape)
    return renderableObjects

def createRenderLayer(trigger):
    if cmds.textScrollList('YM_ReferenceWindow_List',q=True,si=True) is None:
        cmds.warning('Select Some Reference Name!!!')
        return

    sceneAOVs = cmds.ls(type='aiAOV')
    
    if trigger is True:
        for reference in cmds.textScrollList('YM_ReferenceWindow_List',q=True,si=True):
            #Get reference's RenderLayer Node and give a hint with already layered reference
            count = 0
            for renderLayer in referenceNodeTypeFilter(cmds.referenceQuery(reference,nodes=True,dp=True),'renderLayer'):
                if re.search('(defaultRenderLayer){1,}',renderLayer) is None:
                    if cmds.confirmDialog( title='Continue?', message=reference + ' has some renderLayers already, Continue?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' ) == 'No':
                        count = 1
                        continue
            if count > 0:
                continue

            renderableShapes = cmds.listRelatives(findRenderableObjects(reference),p=True,f=True)

            if len(renderableShapes) == 0:
                continue
            #Get the reference filename    
            filenameList = getFormatFilename(cmds.referenceQuery(reference,filename=True,wcn=True))

            #Get reference's aiAOV Node
            referenceAOVs = referenceNodeTypeFilter(cmds.referenceQuery(reference,nodes=True),'aiAOV')
            
            referenceLayer = cmds.createRenderLayer(e=True,n=filenameList[1],noRecurse=True)
            cmds.editRenderLayerMembers(referenceLayer,renderableShapes,nr=True)

            #Switch to defaultRenderLayer and set the reference AOVs to disabled
            cmds.editRenderLayerGlobals(crl='defaultRenderLayer')
            
            for aov in referenceAOVs:
                cmds.setAttr(aov+'.enabled',0)

            #Switch to new Layer and set the relative AOVs to enabled , the unrelative AOVs to disabled
            cmds.editRenderLayerGlobals(crl=referenceLayer)
            for aov in sceneAOVs:
                cmds.editRenderLayerAdjustment(aov+'.enabled',layer=referenceLayer)
                if aov not in referenceAOVs:
                    cmds.setAttr(aov+'.enabled',0)
                else:
                    cmds.setAttr(aov+'.enabled',1)
                        
    else:
        renderableObjects = list()
        referenceAOVs = list()
        for reference in cmds.textScrollList('YM_ReferenceWindow_List',q=True,si=True):
            for parent in cmds.listRelatives(findRenderableObjects(reference),p=True,f=True):
                renderableObjects.append(parent)

            for aov in referenceNodeTypeFilter(cmds.referenceQuery(reference,nodes=True),'aiAOV'):
                referenceAOVs.append(aov)

        if len(renderableObjects) == 0:
            return
        
        referenceLayer = cmds.createRenderLayer(e=True,n='ChangeMyName',noRecurse=True)
        cmds.editRenderLayerMembers(referenceLayer,renderableObjects,nr=True)
        
        cmds.editRenderLayerGlobals(crl='defaultRenderLayer')
        for aov in referenceAOVs:
            cmds.setAttr(aov+'.enabled',0)
        
        cmds.editRenderLayerGlobals(crl=referenceLayer)
        for aov in sceneAOVs:
            cmds.editRenderLayerAdjustment(aov+'.enabled',layer=referenceLayer)
            if aov not in referenceAOVs:
                cmds.setAttr(aov+'.enabled',0)
            else:
                cmds.setAttr(aov+'.enabled',1)

    #print renderableObjects




