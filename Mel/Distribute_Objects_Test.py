#-*- coding:utf-8 -*-
import maya.cmds as cmds
import random

def distributeObject():
    if cmds.window('Distribution',ex=True):
        cmds.deleteUI('Distribution')
    cmds.window('Distribution',w=300,h=400)
    cmds.rowLayout(nc=2)
    cmds.columnLayout()
    cmds.rowLayout(nc=2)
    cmds.textFieldGrp('Distribution_StartPointReference',l='StartPoint',w=400)
    cmds.button('Distribution_Start_Button',l='<<<',w=100)
    cmds.setParent(u=True)
    cmds.rowLayout(nc=2)
    cmds.textFieldGrp('Distribution_EndPointReference',l='EndPoint',w=400)
    cmds.button('Distribution_End_Button',l='<<<',w=100)
    cmds.setParent(u=True)

    txField = cmds.floatFieldGrp(l='TranslateX',nf=2,v1=0,v2=0)
    tyField = cmds.floatFieldGrp(l='TranslateY',nf=2,v1=0,v2=0)
    tzField = cmds.floatFieldGrp(l='TranslateZ',nf=2,v1=0,v2=0)
    rxField = cmds.floatFieldGrp(l='RotateX',nf=2,v1=0,v2=0)
    ryField = cmds.floatFieldGrp(l='RotateY',nf=2,v1=0,v2=0)
    rzField = cmds.floatFieldGrp(l='RotateZ',nf=2,v1=0,v2=0)
    sxField = cmds.floatFieldGrp(l='ScaleX',nf=2,v1=1,v2=1)
    syField = cmds.floatFieldGrp(l='ScaleY',nf=2,v1=1,v2=1)
    szField = cmds.floatFieldGrp(l='ScaleZ',nf=2,v1=1,v2=1)
    seedField = cmds.intSliderGrp(l='Seed',field=True,min=0,max=65535)
    cmds.setParent(u=True)
    
    cmds.columnLayout()
    cmds.radioCollection()
    cmds.radioButton('Distribution_Linear_Switch',l='Linear',sl=True)
    cmds.radioButton('Distribution_Random_Switch',l='Random')
    cmds.separator(h=60,style='none')
    cmds.radioCollection()
    cmds.radioButton('Distribution_Uniform_Scale',l='Uniform',sl=True)
    cmds.radioButton('Distribution_Solo_Scale',l='Solo')
    cmds.setParent(u=True)
    cmds.showWindow('Distribution')
    
    fieldList = [txField,tyField,tzField,rxField,ryField,rzField,sxField,syField,szField,seedField]
    cmds.floatFieldGrp(txField,e=True,cc=lambda *args:transformObjects(fieldList))
    cmds.floatFieldGrp(tyField,e=True,cc=lambda *args:transformObjects(fieldList))
    cmds.floatFieldGrp(tzField,e=True,cc=lambda *args:transformObjects(fieldList))
    cmds.floatFieldGrp(rxField,e=True,cc=lambda *args:transformObjects(fieldList))
    cmds.floatFieldGrp(ryField,e=True,cc=lambda *args:transformObjects(fieldList))
    cmds.floatFieldGrp(rzField,e=True,cc=lambda *args:transformObjects(fieldList))
    cmds.floatFieldGrp(sxField,e=True,cc=lambda *args:transformObjects(fieldList))
    cmds.floatFieldGrp(syField,e=True,cc=lambda *args:transformObjects(fieldList))
    cmds.floatFieldGrp(szField,e=True,cc=lambda *args:transformObjects(fieldList))
    cmds.intSliderGrp(seedField,e=True,cc=lambda *args:transformObjects(fieldList))
    cmds.radioButton('Distribution_Uniform_Scale',e=True,cc=lambda *args:transformObjects(fieldList))
    cmds.radioButton('Distribution_Solo_Scale',e=True,cc=lambda *args:transformObjects(fieldList))
    cmds.radioButton('Distribution_Linear_Switch',e=True,cc=lambda *args:transformObjects(fieldList))
    cmds.radioButton('Distribution_Random_Switch',e=True,cc=lambda *args:transformObjects(fieldList))
    cmds.button('Distribution_Start_Button',e=True,c=lambda *args:startPointReferenceButtonAction(fieldList))
    cmds.button('Distribution_End_Button',e=True,c=lambda *args:endPointReferenceButtonAction(fieldList))

def startPointReferenceButtonAction(fieldsList):
    cmds.textFieldGrp('Distribution_StartPointReference',e=True,tx=cmds.ls(sl=True,dag=True,tr=True)[0])
    cmds.floatFieldGrp(fieldsList[0],e=True,v1=cmds.xform(cmds.textFieldGrp('Distribution_StartPointReference',q=True,tx=True),q=True,ws=True,piv=True)[0])
    cmds.floatFieldGrp(fieldsList[1],e=True,v1=cmds.xform(cmds.textFieldGrp('Distribution_StartPointReference',q=True,tx=True),q=True,ws=True,piv=True)[0])
    cmds.floatFieldGrp(fieldsList[2],e=True,v1=cmds.xform(cmds.textFieldGrp('Distribution_StartPointReference',q=True,tx=True),q=True,ws=True,piv=True)[0])
def endPointReferenceButtonAction(fieldsList):
    cmds.textFieldGrp('Distribution_EndPointReference',e=True,tx=cmds.ls(sl=True,dag=True,tr=True)[0])
    cmds.floatFieldGrp(fieldsList[0],e=True,v2=cmds.xform(cmds.textFieldGrp('Distribution_EndPointReference',q=True,tx=True),q=True,ws=True,piv=True)[0])
    cmds.floatFieldGrp(fieldsList[1],e=True,v2=cmds.xform(cmds.textFieldGrp('Distribution_EndPointReference',q=True,tx=True),q=True,ws=True,piv=True)[0])
    cmds.floatFieldGrp(fieldsList[2],e=True,v2=cmds.xform(cmds.textFieldGrp('Distribution_EndPointReference',q=True,tx=True),q=True,ws=True,piv=True)[0])

def transformObjects(fieldsList):
            
    objectTempList = cmds.ls(sl=True,dag=True,tr=True)    
    minTx = cmds.floatFieldGrp(fieldsList[0],q=True,v1=True)
    maxTx = cmds.floatFieldGrp(fieldsList[0],q=True,v2=True)
    minTy = cmds.floatFieldGrp(fieldsList[1],q=True,v1=True)
    maxTy = cmds.floatFieldGrp(fieldsList[1],q=True,v2=True)
    minTz = cmds.floatFieldGrp(fieldsList[2],q=True,v1=True)
    maxTz = cmds.floatFieldGrp(fieldsList[2],q=True,v2=True)
    minRx = cmds.floatFieldGrp(fieldsList[3],q=True,v1=True)
    maxRx = cmds.floatFieldGrp(fieldsList[3],q=True,v2=True)
    minRy = cmds.floatFieldGrp(fieldsList[4],q=True,v1=True)
    maxRy = cmds.floatFieldGrp(fieldsList[4],q=True,v2=True)
    minRz = cmds.floatFieldGrp(fieldsList[5],q=True,v1=True)
    maxRz = cmds.floatFieldGrp(fieldsList[5],q=True,v2=True)
    minSx = cmds.floatFieldGrp(fieldsList[6],q=True,v1=True)
    maxSx = cmds.floatFieldGrp(fieldsList[6],q=True,v2=True)
    minSy = cmds.floatFieldGrp(fieldsList[7],q=True,v1=True)
    maxSy = cmds.floatFieldGrp(fieldsList[7],q=True,v2=True)
    minSz = cmds.floatFieldGrp(fieldsList[8],q=True,v1=True)
    maxSz = cmds.floatFieldGrp(fieldsList[8],q=True,v2=True)
    seed = cmds.intSliderGrp(fieldsList[9],q=True,v=True)
    
   

    if cmds.radioButton('Distribution_Linear_Switch',q=True,sl=True):
        dtx = (maxTx - minTx) / len(objectTempList)
        dty = (maxTy - minTy) / len(objectTempList)
        dtz = (maxTz - minTz) / len(objectTempList)    
        drx = (maxRx - minRx) / len(objectTempList)
        dry = (maxRy - minRy) / len(objectTempList)
        drz = (maxRz - minRz) / len(objectTempList)
        dsx = (maxSx - minSx) / len(objectTempList)
        dsy = (maxSy - minSy) / len(objectTempList)
        dsz = (maxSz - minSz) / len(objectTempList)
    
        for i in range(len(objectTempList)):
            cmds.move((dtx * i + minTx),(dty * i + minTy),(dtz * i + minTz),objectTempList[i])
            cmds.rotate((drx * i + minRx),(dry * i + minRy),(drz * i + minRz),objectTempList[i])
            if cmds.radioButton('Distribution_Uniform_Scale',q=True,sl=True):
                cmds.scale((dsx * i + minSx),(dsx * i + minSx),(dsx * i + minSx),objectTempList[i])
            else:
                cmds.scale((dsx * i + minSx),(dsy * i + minSy),(dsz * i + minSz),objectTempList[i])
    
    elif cmds.radioButton('Distribution_Random_Switch',q=True,sl=True):
        random.seed(cmds.intSliderGrp(fieldsList[9],q=True,v=True))
        for i in range(len(objectTempList)):
            ptx = random.uniform(minTx,maxTx)
            pty = random.uniform(minTy,maxTy)
            ptz = random.uniform(minTz,maxTz)
            prx = random.uniform(minRx,maxRx)
            pry = random.uniform(minRy,maxRy)
            prz = random.uniform(minRz,maxRz)
            psx = random.uniform(minSx,maxSx)
            psy = random.uniform(minSy,maxSy)
            psz = random.uniform(minSz,maxSz)
            cmds.move(ptx,pty,ptz,objectTempList[i])
            cmds.rotate(prx,pry,prz,objectTempList[i])
            if cmds.radioButton('Distribution_Uniform_Scale',q=True,sl=True):
                cmds.scale(psx,psx,psx,objectTempList[i])
            else:
                cmds.scale(psx,psy,psz,objectTempList[i])


distributeObject()
        
        