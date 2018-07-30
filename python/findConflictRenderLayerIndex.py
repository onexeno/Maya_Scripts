import maya.cmds as cmds

def findConflictRenderLayerIndex():
    renderLayerManager = cmds.ls(type='renderLayerManager')
    if(len(renderLayerManager)!=1):
        cmds.error('There are more than one renderLayerManager in this scene')
    renderLayerIndices = cmds.getAttr(renderLayerManager+'.renderLayerId')

    countElement = []
    for renderLayerIndex in renderLayerIndices:
        countElement.append(renderLayerIndex)
        count = 0
        for index in renderLayerIndices:
            if index==renderLayerIndex:
                count+=1
        
        countElement.append = count
    
    for i in range(0,len(countElement),2):
        print('Index is :' + countElement[i] + ' And Count Number is : ' + countElement[i+1]+'\n')

