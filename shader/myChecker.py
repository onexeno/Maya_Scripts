import maya.cmds as cmds

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
                
    

check = myChecker()

cmds.select([i for i in check.combineObjects()],r=True)
cmds.select([i for i in check.multiShadings()],r=True)
