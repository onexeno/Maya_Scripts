import maya.cmds as cd
import re

objList = cd.ls(sl=True)

if cd.nodeType(objList[0])==cd.nodeType(objList[1]):
    try:
        oldConnections = cd.listConnections(objList[1],p=True,c=True)
                
        #newConnections = cd.listConnections(objList[0],p=True,c=True)
        for i in range(0,len(oldConnections),2):
            #oldNodeName = oldConnections[i].split('.')
            print oldConnections[i]
            reMatch = re.match("^.+?\.",oldConnections[i])
            newAttrName = objList[0] + "." + oldConnections[i][reMatch.end():len(oldConnections[i])]
            if cd.attributeQuery(oldConnections[i][reMatch.end():len(oldConnections[i])],n=objList[0],ex=True):        
                cd.disconnectAttr(oldConnections[i],oldConnections[i+1])
                cd.connectAttr(newAttrName,oldConnections[i+1],f=True)
            else:
                continue
    except:
        pass

else:
    cd.warning("Choose Same Node Type!!!")


