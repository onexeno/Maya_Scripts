import maya.cmds as cmds
import re

class myChecker():
    def __init__(self):
        pass
    #check the combine multi polymesh
    def combineObjects(self):
        for mesh in cmds.ls(dag=True,ni=True,type='mesh'):
            if cmds.polyEvaluate(mesh,shell=True)>1:
                yield mesh
        
    #check the face selection shading
    def multiShadings(self):
        for mesh in cmds.ls(dag=True,ni=True,type='mesh'):
            if len(set(cmds.listConnections(mesh,type='shadingEngine')))>1:
                yield mesh

    #check the object with -1 scale,means it is a mirror copy           
    def negativeScale(self):
        for transform in cmds.ls(dag=True,type='transform'):
            if cmds.getAttr(transform+'.scaleX') < 0 or cmds.getAttr(transform+'.scaleY') <0 or cmds.getAttr(transform+'.scaleZ') < 0:
                yield transform

    def verboseCameras(self):
        for camera in cmds.ls(dag=True,type='camera'):
            if re.search('[0-9]{1,}',camera) is not None:
                if cmds.camera(camera,q=True,sc=True):
                    yield cmds.listRelatives(camera,p=True)[0]

    def noShadings(self):
        for mesh in cmds.ls(dag=True,ni=True,type='mesh'):
            if len(set(cmds.listConnections(mesh,type='shadingEngine'))) == 0:
                yield mesh
    
    


check = myChecker()

cmds.select([i for i in check.combineObjects()],r=True)
cmds.select([i for i in check.multiShadings()],r=True)
