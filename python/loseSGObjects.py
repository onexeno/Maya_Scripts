import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya


selectionList = OpenMaya.MGlobal.getActiveSelectionList()

selectionIter = OpenMaya.MItSelectionList(selectionList)



while selectionIter.isDone()==False:
    dagNode = selectionIter.getDagPath()    
    dagNodeShape = dagNode.extendToShape()  #still a MDagPath Object

    dgNode = OpenMaya.MFnDependencyNode(selectionIter.getDependNode())  #MFnDependencyNode(MObject)
    dgPlug = OpenMaya.MPlug(selectionIter.getDependNode(),dgNode.attribtue('opacity'))

    


    selectionIter.next()


