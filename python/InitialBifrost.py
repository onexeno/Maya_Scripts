

import maya.cmds as cmds

if(len(cmds.ls(sl=True,tr=True) == 1)):
    bboxInfo = calculateBoundingBox()
else:
    bboxInfo = [[100,20,100],[0,0,0]]

def calculateBoundingBox():
    bbox = cmds.xform(q=True,ws=True,bb=True)
    size = [bbox[3]-bbox[0],bbox[4]-bbox[1],bbox[5]-bbox[2]]
    position = [bbox[3]+bbox[0],bbox[4]+bbox[1],bbox[5]+bbox[2]]
    return [size,position]


#Generate two boxes as container & collider
def generateBoxs(bboxInfo):
    container = cmds.polyCube(n='BifrostConatinerBox')
    collider = cmds.polyCube(n='BifrostColliderBox')

    cmds.setAttr(container[0]+".scaleX",bboxInfo[0][0])
    cmds.setAttr(container[0]+".scaleY",bboxInfo[0][1])
    cmds.setAttr(container[0]+".scaleZ",bboxInfo[0][2])
    cmds.setAttr(collider[0]+".scaleX",bboxInfo[0][0])
    cmds.setAttr(collider[0]+".scaleY",bboxInfo[0][1])
    cmds.setAttr(collider[0]+".scaleZ",bboxInfo[0][2])
    cmds.delete(collider[0]+".f[1]")
    cmds.setAttr(container[0]+".tx",bboxInfo[1][0])
    cmds.setAttr(container[0]+".ty",bboxInfo[1][1])
    cmds.setAttr(container[0]+".tz",bboxInfo[1][2])
    cmds.setAttr(collider[0]+".tx",bboxInfo[1][0])
    cmds.setAttr(collider[0]+".ty",bboxInfo[1][1])
    cmds.setAttr(collider[0]+".tz",bboxInfo[1][2])
    return [container[0],collider[0]]


def createBifrostContainer(*ContainerObject,*ColliderObject,*GuideObject):
    cmds.select(cl=True)

    try:
        cmds.select(ContainerObject)
        cmds.CreateBifrostLiquid()
        cmds.select(cl=True)
        try:
            cmds.select(ColliderObject,'bifrostContainerLiquid1')
            cmds.AddBifrostCollider()
            cmds.select(cl=True)   
        except:
            pass
        try:
            cmds.select(GuideObject,'bifrostContainerLiquid1')
            cmds.AddBifrostGuide()
        except:
            pass
    except:
        cmds.CreateBifrostLiquid()



    
    


