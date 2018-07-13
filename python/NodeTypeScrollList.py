import maya.cmds as cmds


allNodes = cmds.ls()
nodeType = []
for node in allNodes:
    nodeType.append(cmds.nodeType(node))
    
nodeType = list(set(nodeType)) #remove duplicates element in list





    
def textScrSelection(textControl):
    cmds.select(cl=True)
    for type in cmds.textScrollList(textControl,q=True,si=True):
        nodes = cmds.ls(typ=type)
        cmds.select(nodes,add=True)




if (cmds.window("Television",ex=True)):
    cmds.deleteUI("Television")
   
cmds.window("Television",t="Hoy",w=500,h=600)
mainLayout = cmds.frameLayout(l="MayBe")
cmds.textField(p=mainLayout,w=500)
childLayout = cmds.columnLayout(p=mainLayout)
textScr1 = cmds.textScrollList(p=childLayout,w=500,h=500,ams=True,dcc=lambda :textScrSelection(textScr1))
cmds.showWindow("Television")



for type in nodeType:
    cmds.textScrollList(textScr1,a=type,e=True)    



