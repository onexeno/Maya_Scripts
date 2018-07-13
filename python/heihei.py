import sys
import maya.OpenMaya as OM
import maya.OpenMayaMPx as OMMPx

kHappyFooId = OM.MTypeId(0x80689305)
kHappyFooName = "happyGo"
kHappyFooClassify = "utility/color"

class happyGoShader(OMMPx.MPxNode):
    
    def __init__(self):
        OMMPx.MPxNode.__init__(self)
        aHappyColor = OM.MObject()
        aHappyOffset = OM.MObject()
        aHappyScale = OM.MObject()
        aHappyPoint = OM.MObject()
    
    def compute(self,plug,dataBlock):
        resultColor = OM.MFloatVector(0.0,0.0,0.0)
        #happyColor = dataBlock.inputValue(happyGoShader.aHappyColor).asFloatVector()
        happyOffset = dataBlock.inputValue(happyGoShader.aHappyOffset).asFloatVector()
        happyScale = dataBlock.inputValue(happyGoShader.aHappyScale).asFloatVector()
        happyPoint = dataBlock.inputValue(happyGoShader.aHappyPoint).asFloatVector()
        
        resultColor.x = happyPoint.x * happyScale.x + happyOffset.x
        resultColor.y = happyPoint.y * happyScale.y + happyOffset.y
        resultColor.z = happyPoint.z * happyScale.z + happyOffset.z
        
        outColorHandle = dataBlock.outputValue(happyGoShader.aHappyColor)
        outColorHandle.setMFloatVector(resultColor)
        outColorHandle.setClean
        
def nodeCreator():
    return OMMPx.asMPxPtr(happyGoShader())

def nodeInitializer():
    nAttr = OM.MFnNumericAttribute()
    
    try:
        happyGoShader.aHappyPoint = nAttr.createPoint("point","p")
        nAttr.setStorable(0)
        nAttr.setHidden(0)
        nAttr.setWritable(1)
        nAttr.setReadable(1)
        nAttr.setKeyable(1)
        
        happyGoShader.aHappyOffset = nAttr.createPoint("offset","o")
        nAttr.setStorable(1)
        nAttr.setKeyable(1)
        nAttr.setWritable(1)
        nAttr.setReadable(1)
        
        happyGoShader.aHappyScale = nAttr.createPoint("scale","s")
        nAttr.setStorable(1)
        nAttr.setKeyable(1)
        nAttr.setWritable(1)
        nAttr.setReadable(1)
        
        happyGoShader.aHappyColor = nAttr.createPoint("outcolor","oc")
        nAttr.setStorable(0)
        nAttr.setWritable(0)
        nAttr.setReadable(1)
        nAttr.setKeyable(0)
        
    except:
        
        sys.stderr.write("Failed\n")
        raise
        
    try:
        happyGoShader.addAttribute(happyGoShader.aHappyPoint)
        happyGoShader.addAttribute(happyGoShader.aHappyScale)
        happyGoShader.addAttribute(happyGoShader.aHappyOffset)
        happyGoShader.addAttribute(happyGoShader.aHappyColor)

    except:
        sys.stderr.write("Failed\n")
        raise
    
    try:
        happyGoShader.attributeAffects(happyGoShader.aHappyScale,happyGoShader.aHappyColor)
        happyGoShader.attributeAffects(happyGoShader.aHappyOffset,happyGoShader.aHappyColor)
        happyGoShader.attributeAffects(happyGoShader.aHappyPoint,happyGoShader.aHappyColor)

    except:
        sys.stderr.write("Failed\n")
        raise
        
def initializePlugin(mObject):
    mPlugin = OMMPx.MFnPlugin(mObject)
    try:
        mPlugin.registerNode(kHappyFooName,kHappyFooId,nodeCreator,nodeInitializer,OMMPx.MPxNode.kDependNode,kHappyFooClassify)
    
    except:
        
        sys.stderr.write("Failed\n")
        raise
    
    
def uninitializePlugin(mObject):
    mPlugin = OMMPx.MFnPlugin(mObject)
    try:
        mPlugin.deregisterNode(kHappyFooId)
    except:
        sys.stderr.write("Failed\n")
        raise
        
            



            