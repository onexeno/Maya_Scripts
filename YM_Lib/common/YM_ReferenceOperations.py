#-*- coding: utf-8 -*-
import maya.cmds as cmds
import re
#cmds.ls(typ='reference') #Get reference node
#cmds.file(q=True,r=True) #Get reference file

def getLoadedReferenceList():
    #获取已经加载的参考节点
    loadReferenceList = []
    for ref in cmds.ls(type='reference'):
        try:
            if cmds.referenceQuery(ref,il=True):
                loadReferenceList.append(ref)
        except:
            continue        
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
    if referenceNodesList is None:
        return ['']
    for referenceNode in referenceNodesList:
        if(cmds.nodeType(referenceNode) == type):
            nodesList.append(referenceNode)
    return nodesList

def referenceRootGroup(referenceNode):
    if referenceNode is None:
        return ''
    
    relativeNodes = cmds.referenceQuery(referenceNode,nodes=True)
    fullPathName = []
    for node in relativeNodes:
        apName = cmds.ls(node,ap=True)
        if cmds.nodeType(apName) == 'transform':
            fullPathName.append(cmds.ls(node,ap=True)[0])

    #transformNodes = [node for node in relativeNodes if cmds.nodeType(node)=='transform']
    transformNodes = fullPathName
    worldGroup = []
    for transformNode in transformNodes:
        #print transformNode
        if cmds.listRelatives(transformNode,parent=True) is None and cmds.listRelatives(transformNode) is not None:
            worldGroup.append(transformNode)
        else:
            continue
    return worldGroup

def checkReferenceTypeByPath(referenceNode,referenceType):
    filename = cmds.referenceQuery(referenceNode,filename=True)
    if filename is None:
        return 0
    if re.search(referenceType,referenceNode) is None:
        return 0
    else:
        return 1

