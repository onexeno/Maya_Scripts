import maya.api.OpenMaya as OpenMaya

mSelList = OpenMaya.MGlobal.getActiveSelectionList()
mItSelList = OpenMaya.MItSelectionList(mSelList)

while (mItSelList.isDone()!=True): #注意这里isDone()，不能省略括号
    tempDag = mItSelList.getDagPath()
    print tempDag.getPath()
    mItSelList.next()


"Let's have a test"