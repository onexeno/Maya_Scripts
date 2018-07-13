#主要思路是：
#1.根据包裹盒：分别比较包裹盒的Length、Width、Height三个参数判定
#2.根据包裹盒体积判定
#3.根据命名选择
#4.根据选择物体的范围半径
#5.根据节点类型
#6.根据轴向选择
#7.根据所选属性相同与否

import math
from maya import cmds
#获取包裹盒
#-------------------- Bounding Box Calculate Start -----------------------#

def calculateBoundingBoxVolume(object):
    tempBBOX = cmds.xform(object,q=True,ws=True,bb=True)
    return (tempBBOX[3]-tempBBOX[0])*(tempBBOX[4]-tempBBOX[1])*(tempBBOX[5]-tempBBOX[2])

def calculateBoundingBoxAxisX(object):
    tempBBOX = cmds.xform(object,q=True,ws=True,bb=True)
    return (tempBBOX[3]-tempBBOX[0])

def calculateBoundingBoxAxisY(object):
    tempBBOX = cmds.xform(object,q=True,ws=True,bb=True)
    return (tempBBOX[4]-tempBBOX[1])

def calculateBoundingBoxAxisZ(object):
    tempBBOX = cmds.xform(object,q=True,ws=True,bb=True)
    return (tempBBOX[5]-tempBBOX[2])

#-------------------- Bounding Box Calculate End -----------------------#


def mag(vector):
    return (math.sqrt(vector[0]*vector[0]+vector[1]*vector[1]+vector[2]*vector[2]))

def vLen(pointSta,pointEnd):
    return (math.sqrt(math.pow(pointEnd[0]-pointSta[0],2)+math.pow(pointEnd[1]-pointSta[1],2)+math.pow(pointEnd[2]-pointSta[2],2)))

def vDot(point,normal):
    