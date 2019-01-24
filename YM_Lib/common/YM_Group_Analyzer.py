import maya.cmds as cmds

def groupAnalyzer(node,type,direction):
    allRelativeNodes = []
    def findAllInGroup(node,type):
        if node is not None:
            apName = cmds.ls(node,ap=True)
            if direction == 'down':
				list = cmds.listRelatives(apName,f=True,c=True)
            elif direction == 'up':
				list = cmds.listRelatives(apName,f=True,p=True)
        if list is not None:
            for item in list:
                if len(type)==0:
                    #print item
                    allRelativeNodes.append(item)
                    findAllInGroup(item,type)
                else:
                    if cmds.nodeType(item)==type:
                        #print item
                        allRelativeNodes.append(item)
                    findAllInGroup(item,type)
    findAllInGroup(node,type)
    return allRelativeNodes



