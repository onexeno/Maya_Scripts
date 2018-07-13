from mtoa import aovs
from maya import cmds


def switchLayerAOV(trigger):
    existsAOVs = aovs.AOVInterface().getAOVNodes(names=True)
    
    for existsAOV in existsAOVs:
        #aovName = existsAOV[0]
        aovNode = existsAOV[1].getName()
        cmds.editRenderLayerAdjustment(aovNode+".enabled")
        cmds.setAttr(aovNode+".enabled",trigger)
        #print(aovName + "\t:\t" +aovNode)
    



if cmds.window("AOVNode",ex=True):
    cmds.deleteUI("AOVNode")
    
cmds.window("AOVNode",w=120,h=60,t='AOVWindow')
cmds.columnLayout()
cmds.text(l="          ¼òµ¥¿ª¹ØAOV")
cmds.rowLayout(nc=2)
cmds.button(l="ON",w=60,h=60,bgc=[0,0.5,0],c='switchLayerAOV(1)')
cmds.button(l="OFF",w=60,h=60,bgc=[0.5,0,0],c='switchLayerAOV(0)')
cmds.showWindow("AOVNode")