import maya.OpenMaya as OM
import maya.OpenMayaMPx as OMMPx
import sys

kHelloNodeName = "hello"
kHelloNodeId = OM.MTypeId(0x291021)
kHelloNodeClassify = "utility/general"

class shello(OMMPx.MPxNode):
    
    def __init__(self):
        OMMPx.MPxNode.__init__(self)
        pass

def nodeCreator():
    return OMMPx.asMPxPtr(shello())
    #pass
    
def nodeInitializer():
    pass
    
def initializePlugin(mobject):
    mplugin = OMMPx.MFnPlugin(mobject)
    
    try:
        mplugin.registerNode(kHelloNodeName,kHelloNodeId,nodeCreator,nodeInitializer,OMMPx.MPxNode.kDependNode,kHelloNodeClassify)
    except:
        raise
        
def uninitializePlugin(mobject):
    mplugin = OMMPx.MFnPlugin(mobject)
    
    try:
        mplugin.deregisterNode(kHelloNodeId)
    except:
        raise
        
        

import maya.cmds
import maya.cmds as cmds

