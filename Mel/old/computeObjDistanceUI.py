import maya.cmds as mc
import maya.mel as mel
import math
#declare a global locator, use to delete locator
locator = []
newCurve = []
textElements = ""

def disBetweenTwoVtxNode():
    global locator
    target = mc.ls(sl=True,fl=True)

    if(len(target)!=2):
        mc.warning("Choose Two Point or Object")
    else:
        sourcePos = mc.xform(target[0],q=True,ws=True,t=True)
        targetPos = mc.xform(target[1],q=True,ws=True,t=True)
        sourceLocator = mc.spaceLocator()
        locator.append(sourceLocator[0])
        targetLocator = mc.spaceLocator()
        locator.append(targetLocator[0])
        mc.xform(sourceLocator[0],ws=True,t=sourcePos)
        mc.xform(targetLocator[0],ws=True,t=targetPos)
        mc.select(sourceLocator[0],targetLocator[0])

        distanceNode = mc.distanceDimension( sp = sourcePos , ep = targetPos )

        mc.select(clear=True)
        mc.select(target[0],sourceLocator[0])
        mel.eval('doCreatePointOnPolyConstraintArgList 2 {   "0" ,"0" ,"0" ,"1" ,"" ,"1" ,"0" ,"0" ,"0" ,"0" };')

        mc.select(clear=True)
        mc.select(target[1],targetLocator[0])
        mel.eval('doCreatePointOnPolyConstraintArgList 2 {   "0" ,"0" ,"0" ,"1" ,"" ,"1" ,"0" ,"0" ,"0" ,"0" };')

def disBetweenTwoObjNode():
    global locator
    target = mc.ls(sl=True,tr=True)

    if(len(target)!=2):
        mc.warning("Choose Two Point or Object")
    else:
        sourceBB = mc.xform(target[0],q=True,bb=True)
        srcBBCenter = [(sourceBB[0]+sourceBB[3])/2,(sourceBB[1]+sourceBB[4])/2,(sourceBB[2]+sourceBB[5])/2]
        targetBB = mc.xform(target[1],q=True,bb=True)
        tarBBCenter = [(targetBB[0]+targetBB[3])/2,(targetBB[1]+targetBB[4])/2,(targetBB[2]+targetBB[5])/2]

        sourceLocator = mc.spaceLocator()
        locator.append(sourceLocator[0])
        targetLocator = mc.spaceLocator()
        locator.append(targetLocator[0])
        mc.xform(sourceLocator[0],ws=True,t=srcBBCenter)
        mc.xform(targetLocator[0],ws=True,t=tarBBCenter)
        mc.select(sourceLocator[0],targetLocator[0])

        distanceNode = mc.distanceDimension( sp = srcBBCenter , ep = tarBBCenter)
        mc.select(target[0],sourceLocator[0])
        mel.eval('doCreatePointConstraintArgList 1 { "0","0","0","0","0","0","0","1","","1" };')
        mc.select(clear = True)
        mc.select(target[1],targetLocator[0])
        mel.eval('doCreatePointConstraintArgList 1 { "0","0","0","0","0","0","0","1","","1" };')
        mc.select(clear = True)

def deleteLocator():
    global locator
    global newCurve
    locatorCount = 0
    newCurveCount = 0
    for loc in locator:
        if(mc.objExists((loc))):
            mc.delete(loc)
            locatorCount+=1
    for cur in newCurve:
        if(mc.objExists(cur)):         
            mc.delete(cur)
            newCurveCount+=1
    if(len(locator)>0 and locatorCount==0):
        locator = []
    if(len(newCurve)>0 and newCurveCount==0):
        newCurve = []


def computePointDistance():
    target = mc.ls(sl=True,fl=True)
    if(len(target)!=2):
        mc.warning("Choose Two Point or Object")
        return "Error"
    else:
        sourcePos = mc.xform(target[0],q=True,ws=True,t=True)
        targetPos = mc.xform(target[1],q=True,ws=True,t=True)
        posVector = [ sourcePos[0] - targetPos[0] , sourcePos[1] - targetPos[1] , sourcePos[2] - targetPos[2] ]

        return math.sqrt(math.pow(posVector[0],2)+math.pow(posVector[1],2)+math.pow(posVector[2],2))

def computeObjDistance():
    target = mc.ls(sl=True,tr=True)
    if(len(target)!=2):
        mc.warning("Choose Two Point or Object")
        return "Error"
    else:
        sourceBB = mc.xform(target[0],q=True,bb=True)
        srcBBCenter = [(sourceBB[0]+sourceBB[3])/2,(sourceBB[1]+sourceBB[4])/2,(sourceBB[2]+sourceBB[5])/2]
        targetBB = mc.xform(target[1],q=True,bb=True)
        tarBBCenter = [(targetBB[0]+targetBB[3])/2,(targetBB[1]+targetBB[4])/2,(targetBB[2]+targetBB[5])/2]

        posVector = [srcBBCenter[0]-tarBBCenter[0],srcBBCenter[1]-tarBBCenter[1],srcBBCenter[2]-tarBBCenter[2]]

        return math.sqrt(math.pow(posVector[0],2)+math.pow(posVector[1],2)+math.pow(posVector[2],2))


def createCurveBetweenVertex():
    target = mc.ls(sl=True,fl=True)
    global newCurve
    if(len(target)!=2):
        mc.warning("Choose Two Point or Object")
    else:
        sourcePos = mc.xform(target[0],q=True,ws=True,t=True)
        targetPos = mc.xform(target[1],q=True,ws=True,t=True)

        pointCurve = mc.curve(p=(sourcePos,targetPos),ws=True,d=1)
        newCurve.append(pointCurve)
        cluster1 = mc.cluster(pointCurve+'.cv[0]')
        newCurve.append(cluster1[1])
        mc.setAttr(cluster1[1]+'.visibility',0)
        cluster2 = mc.cluster(pointCurve+'.cv[1]')
        newCurve.append(cluster2[1])
        mc.setAttr(cluster2[1]+'.visibility',0)
        
        
        mc.select(clear=True)
        mc.select(target[0],cluster1[1])
        mel.eval('doCreatePointOnPolyConstraintArgList 2 {   "0" ,"0" ,"0" ,"1" ,"" ,"1" ,"0" ,"0" ,"0" ,"0" };')

        mc.select(clear=True)
        mc.select(target[1],cluster2[1])
        mel.eval('doCreatePointOnPolyConstraintArgList 2 {   "0" ,"0" ,"0" ,"1" ,"" ,"1" ,"0" ,"0" ,"0" ,"0" };')



def computeObjDistanceUI():
    if(mc.window('computeDistanceUI',ex=True)):
        mc.deleteUI('computeDistanceUI')

    global textElements
    mc.window('computeDistanceUI',t='ComputeDistance',sizeable=False)
    mc.columnLayout()
    mc.separator(h=5)
    mc.rowLayout(nc=3)
    mc.separator(w=2,style='none')
    textElements = mc.text(w=110,h=35,l="Distance",bgc=[1,1,1],en=True)
    mc.separator(w=2,style='none')
    mc.setParent(u=True)
    mc.separator(h=5)
    mc.button(ann='选择两个顶点，测量距离',l='Point Distance',w=120,h=30,c='mc.text( textElements , e=True,l = computePointDistance() )',bgc=[0.1,0.2,0.3])
    mc.button(ann='选择两个物体，测量距离',l='Object Distance',w=120,h=30,c='mc.text( textElements , e=True,l = computeObjDistance() )',bgc=[0.125,0.225,0.325])
    mc.button(ann='选择两个顶点，生成测量节点',l='Point DisNode',w=120,h=30,c='disBetweenTwoVtxNode()',bgc=[0.15,0.25,0.35])
    mc.button(ann='选择两个物体,生成测量节点',l='Object DisNode',w=120,h=30,c='disBetweenTwoObjNode()',bgc=[0.175,0.275,0.375])
    mc.button(ann='选择两个顶点，创建线段',l='Create Curve',w=120,h=30,c='createCurveBetweenVertex()',bgc=[0.2,0.3,0.4])
    mc.button(ann='删除当前创建的locator节点',l='Del Locator',w=120,h=30,c='deleteLocator()',bgc=[0.225,0.325,0.425])
    if(mc.window('computeDistanceUI',ex=True)):
       mc.windowPref('computeDistanceUI',r=True)


    mc.showWindow('computeDistanceUI')


computeObjDistanceUI()


