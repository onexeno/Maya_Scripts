import sys
import maya.cmds as cmds

def findRelativeConnections(direction,object,count,filter):
    allUpstreamNodes = []
    tempConnectArray = []
    if direction == 0:
        tempConnectArray = cmds.listConnections(object,sh=True,d=False,c=False,scn=True) 
    elif direction == 1:
        tempConnectArray = cmds.listConnections(object,sh=True,s=False,c=False,scn=True)
    else:
        tempConnectArray = cmds.listConnections(object,sh=True,c=False,scn=True)
    #print (tempConnectArray)
    #print type(tempConnectArray)
    try:
        if len(tempConnectArray)>0 and count!=0:
            count-=1
            if(abs(count)>10):
                return allUpstreamNodes
            for temp in tempConnectArray:
                if allUpstreamNodes.count(temp)<=0 and filter.count(cmds.nodeType(temp))>0:
                    allUpstreamNodes.append(temp)
                    findRelativeConnections(direction,temp,count,filter)
                else:
                    continue
    except:
        return allUpstreamNodes
    return allUpstreamNodes


#findRelativeConnections(1,'pSphereShape1',1,['shadingEngine'])