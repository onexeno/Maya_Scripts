import maya.cmds as cmds

#cmds.ls(typ='reference') #Get reference node
#cmds.file(q=True,r=True) #Get reference file

def getLoadedReferenceList():
    loadReferenceList = []
    for ref in cmds.ls(type='reference'):
        if cmds.referenceQuery(ref,il=True):
            loadReferenceList.append(ref)
    return loadReferenceList

def referenceCreateDisplayLayer(referenceList): 
    #根据参考创建对应的显示层
    for reference in referenceList:
        referenceRelativesNodes = cmds.referenceQuery(reference,nodes=True)
        referenceNamespace = cmds.referenceQuery(reference,namespace=True,showNamespace=True)
        transformNodes = referenceNodeTypeFilter(referenceRelativesNodes,'transform')
        referenceDisplayLayer = cmds.createDisplayLayer(e=True,n=referenceNamespace+'_View')
        cmds.editDisplayLayerMembers(referenceDisplayLayer,transformNodes)

def referenceCreateRenderLayer(referenceList):
    #根据参考创建对应的渲染层
    for reference in referenceList:
        referenceRelativeNodes = cmds.referenceQuery(reference,nodes=True)
        referenceNamespace = cmds.referenceQuery(reference,namespace=True,showNamespace=True)
        transformNodes = referenceNodeTypeFilter(referenceRelativeNodes,'transform')
        renderableObjects = referenceNodeRenderableCheck(transformNodes)
        referenceRenderLayer = cmds.createRenderLayer(e=True,n=referenceNamespace+'_Render')
        cmds.editRenderLayerMembers(referenceRenderLayer,transformNodes)

def referenceNodeRenderableCheck(referenceNodeList):
    #Exclude the Template,Ghost object
    #检查如果对应物体是否是template（模板）或者intermediate（中介）对象
    renderableObjects = []
    for referenceNode in referenceNodeList:
        if cmds.getAttr(referenceNode+'.template') is False and cmds.getAttr(referenceNode+'.intermediateObject') is False:
            renderableObjects.append(referenceNode)
    return renderableObjects


def referenceNodeTypeFilter(referenceNodesList,type):
    #根据输入的节点类型筛选参考节点
    nodesList = []
    for referenceNode in referenceNodesList:
        if(cmds.nodeType(referenceNode) == type):
            nodesList.append(referenceNode)
    return nodesList
