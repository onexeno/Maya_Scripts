#-*- coding:gbk -*-
from maya import cmds

#callback函数有固定的传入参数，在调用函数的时候会由对象自动传入，所以声明函数的时候要带上必须的参数
def gridCallback(dragControl,x,y,modifiers):
    layout = cmds.control(dragControl,q=True,p=True)
    
    
def gridDropCallback(dragControl,dropControl,messages,x,y,dragTypes):
    print dragControl + '\n'
    print dropControl + '\n'
    print str(x) + ',' + str(y) + '\n'
    gridOrder = cmds.gridLayout('testGridLayout',q=True,go=True,fpn=True)
    dragName = dragControl.split('|')
    dropName = dropControl.split('|')
    dragOrder = gridOrder.index(dragName[-1])
    dropOrder = gridOrder.index(dropName[-1])
    cmds.gridLayout('testGridLayout',e=True,pos=[dragName[-1],dropOrder+1])
    cmds.gridLayout('testGridLayout',e=True,pos=[dropName[-1],dragOrder+1])
    cmds.setFocus('testGridLayout')
    
    print messages
    print dragTypes
    


if cmds.window('testLayout',ex=True):
    cmds.deleteUI('testLayout')
    
cmds.window('testLayout',t='TestLayout',w=400,h=200)
cmds.gridLayout('testGridLayout',ag=True,cr=True,cw=100,ch=100)

cmds.button('ButtonA1',w=100,dgc=gridCallback,dpc=gridDropCallback)
cmds.button('ButtonA2',w=100,dgc=gridCallback,dpc=gridDropCallback)
cmds.button('ButtonA3',w=100,dgc=gridCallback,dpc=gridDropCallback)
cmds.button('ButtonA4',w=100,dgc=gridCallback,dpc=gridDropCallback)
cmds.button('ButtonA5',w=100,dgc=gridCallback,dpc=gridDropCallback)
cmds.button('ButtonA6',w=100,dgc=gridCallback,dpc=gridDropCallback)
cmds.showWindow('testLayout')
