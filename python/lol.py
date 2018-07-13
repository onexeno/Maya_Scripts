import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx  as OpenMayaMPx


kGaussianNodeName = "gaussian"
kGaussianNodeId = OpenMaya.MTypeId(0x00920123)
kGaussianNodeClassify = "utility/general"


class gaussianToolkit(OpenMayaMPx.MPxNode):
    #__init__ the class
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        gGaussianFloatA = OpenMaya.MObject()
        gGaussianFloatB = OpenMaya.MObject()
    
    #define the compute algorithm
    def compute(self,plug,block):
        resultFloat = OpenMaya.MFloatVector()
        gaussianFloat = block.inputValue(gaussianToolkit.gGaussianFloatB).asFloatVector()
        
        resultFloat = gaussianFloat

        outValueHandle = block.outputValue(gaussianToolkit.gGaussianFloatA).asFloatVector()
        outValueHandle.setMFloatVector(resultFloat)
        outValueHandle.setClean()
        #pass

#define node creator module
def nodeCreator():
    return OpenMayaMPx.asMPxPtr(gaussianToolkit())
#define node Initializer module
def nodeInitializer():
    nAttr = OpenMaya.MFnNumericAttribute()
    

    gaussianToolkit.gGaussianFloatB = nAttr.createPoint("inputValue","iv")
    nAttr.setWritable(1)
    nAttr.setReadable(1)
    nAttr.setStorable(1)
    nAttr.setKeyable(1)
    gaussianToolkit.gGaussianFloatA = nAttr.createPoint("outValue","ov")
    nAttr.setStorable(0)
    nAttr.setReadable(1)
    nAttr.setWritable(0)
    nAttr.setKeyable(0)
    
    gaussianToolkit.addAttribute(gaussianToolkit.gGaussianFloatA)
    gaussianToolkit.addAttribute(gaussianToolkit.gGaussianFloatB)
    
    gaussianToolkit.attributeAffects(gaussianToolkit.gGaussianFloatB,gaussianToolkit.gGaussianFloatA)
    
    
    #pass

def initializePlugin(mObject):
    mPlugin = OpenMayaMPx.MFnPlugin(mObject)
    mPlugin.registerNode(kGaussianNodeName,kGaussianNodeId,nodeCreator,nodeInitializer,OpenMayaMPx.MPxNode.kDependNode,kGaussianNodeClassify)
    
def uninitializePlugin(mObject):
    mPlugin = OpenMayaMPx.MFnPlugin(mObject)
    mPlugin.deregisterNode(kGaussianNodeId)
    
    
    
    
    
    