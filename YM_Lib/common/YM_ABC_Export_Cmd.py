#-*- coding: utf-8 -*-
import maya.cmds as cmds
import os
import re

from YM_ReferenceMeshGroup import *
from YM_Camera_Ops import *
defaultPath = '//S2/Projects/JXB_Season2/TD_Tools/reference_Nodes_List.txt'

def exportCamera():
    
    filepath = cmds.file(q=True,loc=True)
    path = os.path.dirname(filepath) + '/ABC_Caches/'
    
    if os.path.exists(path) is False:
            os.mkdir(path)

    camList = cmds.ls(type='camera')
    #print camList
    
    renderableCamDict = getUnStartupCameras()
    renderableCamList = renderableCamDict.keys()

    '''for cam in camList:
        if cmds.getAttr(cam+'.renderable') == True:
            renderableCamList.append(cam)
    '''


    camTransforms = []
    for renderableCam in renderableCamList:
        for transform in groupAnalyzer(renderableCam,'transform','up'):
            if cmds.listRelatives(transform,parent=True) is None and cmds.listRelatives(transform) is not None:
                camTransforms.append(transform)
    #print camTransforms
    string = ''
    for transform in camTransforms:
        string += ' -root ' + transform

    string += ' -worldSpace -writeVisibility '
    string += exportFrameRange(1)
    string += ' -file '
    string += path
    string += os.path.splitext(os.path.basename(cmds.file(q=True,loc=True)))[0] + '_Camera'
    string += '.abc'
    
    cmds.AbcExport(j=string)
    #return string




def defaultFlags():
    flags = ' '
    #flags += '-noNormals '
    #flags += '-renderableOnly '
    flags += '-stripNamespaces '
    #flags += '-wholeFrameGeo '
    flags += '-worldSpace '
    flags += '-writeVisibility '
    #flags += '-writeCreases '
    flags += '-uvWrite '   
    #flags += '-writeFaceSets ' 
    #flags += '-writeColorSets ' 
    #flags += '-eulerFilter '
    #flags += '-verbose '  
    return flags


def exportFrameRange(switch):
    if switch is False:
        return ''
    else:
        minTime = str(cmds.playbackOptions(q=True,min=True))
        maxTime = str(cmds.playbackOptions(q=True,max=True))
        return ' -frameRange ' + minTime + ' ' + maxTime + ' '




def exportAbcCmd():
    filepath = cmds.file(q=True,loc=True)
    path = os.path.dirname(filepath) + '/ABC_Caches/'

    if os.path.exists(path) is False:
            os.mkdir(path)

    exportNodesDict = getReferenceMeshGroup(defaultPath)
    writeResults(defaultPath,exportNodesDict)

    for key in exportNodesDict.keys():
        referencePath = cmds.referenceQuery(key,f=True)
        if re.search('([s|S]ets){1}',referencePath) is not None:
            continue
        argmentsString = ' -root |'
        argmentsString += exportNodesDict.get(key)
        argmentsString += defaultFlags()
        
        argmentsString += exportFrameRange(1)
        argmentsString += ' -file '
        argmentsString += path

        removeString = re.search('(_okRN){1,}',key)
        if removeString is None:
            removeString = key
        else:
            removeString = removeString.string[0:removeString.start()] + removeString.string[removeString.end():len(removeString.string)]
        removeString = removeString.replace(':','_')
        argmentsString += removeString
        argmentsString += '.abc'
        try:
            print argmentsString
            cmds.AbcExport(j=argmentsString)
        except:
            print (key + 'cannot export, check your scene!')
            continue
'''
try:
    exportCamera()
except:
    pass
try:
    exportAbcCmd()
except:
    cmds.warning('Check your scene!!!')
'''