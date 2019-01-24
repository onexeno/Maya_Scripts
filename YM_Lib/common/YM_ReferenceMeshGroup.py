#-*- coding: utf-8 -*-

import maya.cmds as cmds
import re
from YM_ReferenceOperations import *
from YM_Group_Analyzer import *
        
def writeResults(filepath,resultDict):
    resultCache = readResults(filepath)
    resultfile = open(filepath,'w+')
    #tempDict = resultDict
    for key in resultDict.keys():
        if resultCache.has_key(key):
            if resultDict.get(key) != resultCache.get(key):
                #resultDict[key] = ''
                resultCache[key] = resultDict.get(key)
        else:
            resultCache[key] = resultDict.get(key)
                    
    for key,value in resultCache.items():
        if len(value) == 0 or value is None:
            continue
        resultfile.write(key)
        resultfile.write(' ')
        resultfile.write(value)
        resultfile.write('\n')

    resultfile.close()


def readResults(filepath):
    resultfile = open(filepath,'r')
    if resultfile.mode == 'r':
        resultDict = {}
        for line in resultfile.readlines():
            if len(line) > 1:
                content = line.split(' ')
                #print len(line)
                resultDict[content[0]] = content[1].strip('\n')
        resultfile.close()
        return resultDict
    else:
        resultfile.close()
        return {}

#同一个参考节点名，但是下面的节点数量和root节点名可能会有不同，因为分集参考的原因
#同一个参考，可能会被参考多次，所以如果用参考路径作为唯一参照量，不可行。   


def getReferenceMeshGroup(filepath):
    noRootReferences = []
    validRootReference = {}

    preloadDict = readResults(filepath)

    for reference in getLoadedReferenceList():
        referencePath = cmds.referenceQuery(reference,f=True)
        #如果参考路径是场景，跳过此循环
        if re.search('([s|S]ets){1}',referencePath) is not None:
            continue
        
        rootGroups = []
        mainMeshGroup = ''
        meshNumberTemp = 0
        skeletonNumberTemp = 0

        if preloadDict.has_key(reference):
            mainMeshGroup = preloadDict.get(reference)
            if cmds.objExists(mainMeshGroup):
                validRootReference[reference] = mainMeshGroup
                continue
    
        rootGroups = referenceRootGroup(reference)
        if rootGroups is None:
            noRootReferences.append(reference)
            continue
        
        for rootGroup in rootGroups:
            #如果参考路径是人物，则要检查组内是否存在骨骼
            if re.search('[p|P]rops{1}',referencePath) is None:
                if len(groupAnalyzer(rootGroup,'joint','down')) > 0:
                    continue
            meshNumber = len(groupAnalyzer(rootGroup,'mesh','down'))
            
            if meshNumber > meshNumberTemp:
                meshNumberTemp = meshNumber
                mainMeshGroup = rootGroup
        validRootReference[reference] = mainMeshGroup

    for validKey in validRootReference.keys():
        if validRootReference.get(validKey) is None or len(validRootReference.get(validKey)) == 0:
            validRootReference.pop(validKey)
    
    return validRootReference
    


