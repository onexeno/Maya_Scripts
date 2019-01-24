#-*- coding:utf-8 -*-

import maya.cmds as cmds
import mtoa.core as core
import math
import sys
import pymel
if sys.path.count('\\\\S3\\软件库\\P_插件目录\\YunMan_Toolsets\\Common\\Python') == 0:
    sys.path.append('\\\\S3\\软件库\\P_插件目录\\YunMan_Toolsets\\Common\\Python')
from YM_Group_Analyzer import *


def createWindow():
    if cmds.window('MeshLightSetter',ex=True):
        cmds.deleteUI('MeshLightSetter')

    cmds.window('MeshLightSetter',t='MeshLight Setter',w=600,h=800)
    cmds.rowLayout(nc=2)
    cmds.frameLayout(l='aiTranslatorAttributes',w=380)
    cmds.formLayout('MeshLight_FormLayout')
    f1 = cmds.optionMenu('MeshLight_aiTranslator')
    cmds.menuItem(l='polymesh',p='MeshLight_aiTranslator')
    cmds.menuItem(l='mesh_light',p='MeshLight_aiTranslator')
    cmds.menuItem(l='procedural',p='MeshLight_aiTranslator')
    cmds.menuItem(l='quad',p='MeshLight_aiTranslator')
    cmds.menuItem(l='cylinder',p='MeshLight_aiTranslator')
    cmds.menuItem(l='disk',p='MeshLight_aiTranslator')
    f2 = cmds.colorSliderGrp('MeshLight_aiColor',l='Color')
    f3 = cmds.floatSliderGrp('MeshLight_aiIntensity',l='Intensity',field=True)
    f4 = cmds.floatSliderGrp('MeshLight_aiExposure',l='Exposure',field=True)
    f5 = cmds.checkBox('MeshLight_aiUseTemp',l='Use Temperature')
    f6 = cmds.floatSliderGrp('MeshLight_aiTemperature',l='Temperature',minValue=0.0,maxValue=20000.0,field=True)
    f7 = cmds.checkBox('MeshLight_aiVisible',l='Light Visible')
    f8 = cmds.intFieldGrp('MeshLight_aiSample',l='Sample')
    f9 = cmds.checkBox('MeshLight_aiNormalize',l='Normalize')
    f10 = cmds.checkBox('MeshLight_aiCastShadows',l='Cast Shadows')
    f11 = cmds.floatSliderGrp('MeshLight_aiShadowDensity',l='ShadowDensity',minValue=0.0,maxValue=1.0,field=True)
    f12 = cmds.colorSliderGrp('MeshLight_aiShadowColor',l='Shadow Color')
    f13 = cmds.checkBox('MeshLight_aiCastVolumeShadow',l='Cast Volumeric Shadow')
    f14 = cmds.intFieldGrp('MeshLight_aiVolumeSample',l='Volume Sample')
    f15 = cmds.textFieldGrp('MeshLight_aiAov',l='AOV Group')
    f16 = cmds.rowLayout(nc=2)
    f17 = cmds.button(l='List LightGroup',w=88,c=lambda *args:refreshLightGroupMenu())
    f18 = cmds.button(l='Set LightGroup',w=88,c=lambda *args:setLightGroupFromMenu())
    cmds.setParent(u=True)
    f19 = cmds.textFieldGrp('AOVString',l='AOVs String')
    f20 = cmds.textScrollList('MeshLight_LightGroupList',w=180,h=380)
    f21 = cmds.textScrollList('LightFilterList',w=180,h=380,ams=True)
    f22 = cmds.rowLayout(nc=3)
    cmds.button(l='List',w=58,c=lambda *args:refreshAiLightFilterList())
    cmds.button(l='Connect',w=58,c=lambda *args:connectAiLightFilter())
    cmds.button(l='Cut',w=58,c=lambda *args:disconnectExistsFilters())
    cmds.setParent(u=True)
    cmds.formLayout('MeshLight_FormLayout',e=True,af = [(f1,'top',0),(f1,'left',100),
                                                        (f2,'top',22),(f2,'left',-40),
                                                        (f3,'top',44),(f3,'left',-40),
                                                        (f4,'top',66),(f4,'left',-40),
                                                        (f5,'top',88),(f5,'left',90),
                                                        (f6,'top',110),(f6,'left',-40),
                                                        (f7,'top',132),(f7,'left',90),
                                                        (f8,'top',154),(f8,'left',-40),
                                                        (f9,'top',176),(f9,'left',90),
                                                        (f10,'top',198),(f10,'left',90),
                                                        (f11,'top',220),(f11,'left',-40),
                                                        (f12,'top',242),(f12,'left',-40),
                                                        (f13,'top',264),(f13,'left',90),
                                                        (f14,'top',286),(f14,'left',-40),
                                                        (f15,'top',308),(f15,'left',-40),
                                                        (f16,'top',355),(f16,'left',5),
                                                        (f19,'top',330),(f19,'left',-40),
                                                        (f20,'top',383),(f20,'left',5),
                                                        (f21,'top',383),(f21,'left',195),
                                                        (f22,'top',355),(f22,'left',195)
                                                        ])
    
    
    cmds.setParent(u=True)
    cmds.setParent(u=True)
    cmds.frameLayout(l='Mesh Light List',w=400)
    cmds.rowLayout(nc=5)
    cmds.button(l='aiAreaLight',w=80,c=lambda *ars:createAreaLight())
    cmds.textField('nodeTypeFilterText',w=130)
    cmds.popupMenu(p='nodeTypeFilterText')
    cmds.menuItem(l='getTypeBySelect',c=lambda *args:cmds.textField('nodeTypeFilterText',e=True,tx=cmds.nodeType(cmds.ls(sl=True)[0])))
    cmds.button(l='Selected',w=60,c=lambda args:cmds.select(cmds.ls(sl=True,dag=True,ni=True,type=cmds.textField('nodeTypeFilterText',q=True,tx=True)),r=True))
    cmds.button(l='Scene',w=60,c=lambda args:cmds.select(cmds.ls(dag=True,ni=True,type=cmds.textField('nodeTypeFilterText',q=True,tx=True)),r=True))
    cmds.button(l='Group',w=60,c=lambda args:cmds.select(groupAnalyzer(cmds.ls(dag=True,sl=True,ni=True),cmds.textField('nodeTypeFilterText',q=True,tx=True),'down'),r=True))
    cmds.setParent(u=True)
    cmds.formLayout('MeshLightList_FormLayout')
    cmds.radioCollection()
    w1 = cmds.radioButton('AllLightCheck',l='List All Light',sl=True)
    w2 = cmds.radioButton('SelLightCheck',l='List Sel Light')
    #w1 = cmds.button(l='ALL MESH light',c=lambda *args:lightListRefresh(True),w=100)
    #w2 = cmds.button(l='Sel MESH Light',c=lambda *args:lightListRefresh(False),w=100)
    w3 = cmds.checkBox('List_NormalLight',l='Normal_Light')
    w4 = cmds.checkBox('List_MeshLight',l='Mesh_Light')
    w5 = cmds.textFieldGrp('MeshLight_Template',l='Template',w=400)
    w6 = cmds.button(l='Set Template',c=lambda *args:cmds.textFieldGrp('MeshLight_Template',e=True,tx=cmds.ls(sl=True,dag=True,ni=True)[0]),w=100)
    w7 = cmds.button(l='Convert!',c=lambda *args:convertMeshToMeshLight(),w=100)
    w8 = cmds.textScrollList('MeshLightList',w=400,h=700,ams=True)
    w9 = cmds.text('ListTotalNumber',l='0',w=50,nbg=True)
    w10 = cmds.text('ListSelectNumber',l='0',w=50,nbg=True)
    cmds.radioCollection()
    w11 = cmds.radioButton('Single_Check',l='Single')
    w12 = cmds.radioButton('Double_Check',l='Double',sl=True)
    w13 = cmds.button('ListWireframeColor',l='Color Dis',w=70,c=lambda *args:displayLightColorAsWireframe())
    
    cmds.formLayout('MeshLightList_FormLayout',e=True,af = [(w1,'top',3),(w1,'left',0),
                                                            (w2,'top',3),(w2,'left',101),
                                                            (w3,'top',3),(w3,'left',205),
                                                            (w4,'top',3),(w4,'left',320),
                                                            (w5,'top',27),(w5,'left',-90),
                                                            (w6,'top',27),(w6,'left',297),
                                                            (w7,'top',52),(w7,'left',297),
                                                            (w8,'top',77),(w8,'left',0),
                                                            (w9,'top',57),(w9,'left',0),
                                                            (w10,'top',57),(w10,'left',50),
                                                            (w11,'top',55),(w11,'left',100),
                                                            (w12,'top',55),(w12,'left',160),
                                                            (w13,'top',52),(w13,'left',225)
                                                            ])
    cmds.popupMenu('MeshLightListMenu',p='MeshLightList')
    cmds.menuItem(l='Select...',p='MeshLightListMenu',c=lambda *args:cmds.select([item for item in cmds.textScrollList('MeshLightList',q=True,si=True)]))
    cmds.menuItem(l='Light Color Button Window',c=lambda *args:colorAnalyzer())
    cmds.menuItem(l='Key Light Color',c=lambda *args:hsvColorKeyframeWindow())
    cmds.showWindow('MeshLightSetter')

    cmds.textScrollList('MeshLightList',e=True,dcc=lambda *args:cmds.select(cmds.textScrollList('MeshLightList',q=True,si=True),r=True))
    cmds.textScrollList('MeshLightList',e=True,sc=lambda *args:getMeshLightAttrsAndShow())
    cmds.textScrollList('MeshLight_LightGroupList',e=True,ams=True,sc=lambda *args:genAovString(),dcc=lambda *args:selectLightByGroupName())
    cmds.optionMenu(f1,e=True,cc=lambda *args:setMeshLightAttrsAndShow('translator'))
    cmds.colorSliderGrp(f2,e=True,cc=lambda *args:setMeshLightAttrsAndShow('color'))
    cmds.floatSliderGrp(f3,e=True,cc=lambda *args:setMeshLightAttrsAndShow('intensity'))
    cmds.floatSliderGrp(f4,e=True,cc=lambda *args:setMeshLightAttrsAndShow('exposure'))
    cmds.checkBox(f5,e=True,cc=lambda *args:setMeshLightAttrsAndShow('useTemp'))
    cmds.floatSliderGrp(f6,e=True,cc=lambda *args:setMeshLightAttrsAndShow('temp'))
    cmds.checkBox(f7,e=True,cc=lambda *args:setMeshLightAttrsAndShow('visible'))
    cmds.intFieldGrp(f8,e=True,cc=lambda *args:setMeshLightAttrsAndShow('sample'))
    cmds.checkBox(f9,e=True,cc=lambda *args:setMeshLightAttrsAndShow('normalize'))
    cmds.checkBox(f10,e=True,cc=lambda *args:setMeshLightAttrsAndShow('castShadows'))
    cmds.floatSliderGrp(f11,e=True,cc=lambda *args:setMeshLightAttrsAndShow('shadowDensity'))
    cmds.colorSliderGrp(f12,e=True,cc=lambda *args:setMeshLightAttrsAndShow('shadowColor'))
    cmds.checkBox(f13,e=True,cc=lambda *args:setMeshLightAttrsAndShow('castVolumeShadow'))
    cmds.intFieldGrp(f14,e=True,cc=lambda *args:setMeshLightAttrsAndShow('volumeSample'))
    cmds.textFieldGrp(f15,e=True,cc=lambda *args:setMeshLightAttrsAndShow('aiAov'))
    cmds.radioButton('AllLightCheck',e=True,cc=lambda *args:lightListRefresh())
    cmds.radioButton('SelLightCheck',e=True,cc=lambda *args:lightListRefresh())
    cmds.checkBox('List_NormalLight',e=True,cc=lambda *args:lightListRefresh())
    cmds.checkBox('List_MeshLight',e=True,cc=lambda *args:lightListRefresh())
    cmds.textScrollList('LightFilterList',e=True,dcc=lambda *args:cmds.select(cmds.textScrollList('LightFilterList',q=True,si=True),r=True))

def getNormalLight(allNode):
    normalLightList = list()
    arnoldLightType = ['aiAreaLight','aiSkyDomeLight','aiMeshLight','aiPhotometricLight']
    if allNode == True:
        normalLightList = cmds.ls(lights=True)
        
        for lightType in arnoldLightType:
            for light in cmds.ls(type=lightType):
                normalLightList.append(light)
    else:
        normalLightList = cmds.ls(sl=True,dag=True,lights=True)
        
        for lightType in arnoldLightType:
            for light in cmds.ls(sl=True,dag=True,type=lightType):
                normalLightList.append(light)

    return normalLightList
    

def getMeshLight(allNode):
    meshLightList = list()
    if allNode == True:
        meshLightList = cmds.ls(dag=True,ni=True,type='mesh')
    else:
        meshLightList = cmds.ls(sl=True,dag=True,ni=True,type='mesh')

    availableMeshLight = list()
    for mesh in meshLightList:
        if cmds.getAttr(mesh+'.aiTranslator') == 'mesh_light':
            availableMeshLight.append(mesh)
    return availableMeshLight

def lightListRefresh():
    cmds.textScrollList('MeshLightList',e=True,ra=True)
    tempList = list()
    if cmds.radioButton('AllLightCheck',q=True,sl=True):
        if cmds.checkBox('List_NormalLight',q=True,v=True) == True and cmds.checkBox('List_MeshLight',q=True,v=True) == False:
            tempList = getNormalLight(True)
        elif cmds.checkBox('List_NormalLight',q=True,v=True) == False and cmds.checkBox('List_MeshLight',q=True,v=True) == True:
            tempList = getMeshLight(True)
        elif cmds.checkBox('List_NormalLight',q=True,v=True) == True and cmds.checkBox('List_MeshLight',q=True,v=True) == True:
            tempList = getNormalLight(True)+getMeshLight(True)
        else:
            pass
    if cmds.radioButton('SelLightCheck',q=True,sl=True):
        if cmds.checkBox('List_NormalLight',q=True,v=True) == True and cmds.checkBox('List_MeshLight',q=True,v=True) == False:
            tempList = getNormalLight(False)
        elif cmds.checkBox('List_NormalLight',q=True,v=True) == False and cmds.checkBox('List_MeshLight',q=True,v=True) == True:
            tempList = getMeshLight(False)
        elif cmds.checkBox('List_NormalLight',q=True,v=True) == True and cmds.checkBox('List_MeshLight',q=True,v=True) == True:
            tempList = getNormalLight(False)+getMeshLight(False)
        else:
            pass
    for item in tempList:
        cmds.textScrollList('MeshLightList',e=True,a=item)
    refreshCounts()


def getMeshLightAttrsAndShow():
    item = cmds.textScrollList('MeshLightList',q=True,si=True)[0]
    try:
        if cmds.getAttr(item+'.aiTranslator') == 'polyMesh':
            cmds.optionMenu('MeshLight_aiTranslator',e=True,sl=1)
        elif cmds.getAttr(item+'.aiTranslator') == 'mesh_light':
            cmds.optionMenu('MeshLight_aiTranslator',e=True,sl=2)
        elif cmds.getAttr(item+'.aiTranslator') == 'procedural':
            cmds.optionMenu('MeshLight_aiTranslator',e=True,sl=3)
        elif cmds.getAttr(item+'.aiTranslator') == 'quad':
            cmds.optionMenu('MeshLight_aiTranslator',e=True,sl=4)
        elif cmds.getAttr(item+'.aiTranslator') == 'cylinder':
            cmds.optionMenu('MeshLight_aiTranslator',e=True,sl=5)
        elif cmds.getAttr(item+'.aiTranslator') == 'disk':
            cmds.optionMenu('MeshLight_aiTranslator',e=True,sl=6)
    except:
        pass
    try:
        cmds.colorSliderGrp('MeshLight_aiColor',e=True,rgb=cmds.getAttr(item+'.color')[0])
    except:
        pass
    try:
        cmds.floatSliderGrp('MeshLight_aiIntensity',e=True,v=cmds.getAttr(item+'.intensity'))
    except:
        pass
    try:
        cmds.floatSliderGrp('MeshLight_aiExposure',e=True,v=cmds.getAttr(item+'.aiExposure'))
    except:
        pass
    try:
        cmds.checkBox('MeshLight_aiUseTemp',e=True,v=cmds.getAttr(item+'.aiUseColorTemperature'))
    except:
        pass
    try:
        cmds.floatSliderGrp('MeshLight_aiTemperature',e=True,v=cmds.getAttr(item+'.aiColorTemperature'))
    except:
        pass
    try:
        cmds.checkBox('MeshLight_aiVisible',e=True,v=cmds.getAttr(item+'.lightVisible'))
    except:
        pass
    try:
        cmds.intFieldGrp('MeshLight_aiSample',e=True,v1=cmds.getAttr(item+'.aiSamples'))
    except:
        pass
    try:
        cmds.checkBox('MeshLight_aiNormalize',e=True,v=cmds.getAttr(item+'.aiNormalize'))
    except:
        pass
    try:
        cmds.checkBox('MeshLight_aiCastShadows',e=True,v=cmds.getAttr(item+'.aiCastShadows'))
    except:
        pass
    try:
        cmds.floatSliderGrp('MeshLight_aiShadowDensity',e=True,v=cmds.getAttr(item+'.aiShadowDensity'))
    except:
        pass
    try:
        cmds.colorSliderGrp('MeshLight_aiShadowColor',e=True,rgb=cmds.getAttr(item+'.aiShadowColor')[0])
    except:
        pass
    try:
        cmds.checkBox('MeshLight_aiCastVolumeShadow',e=True,v=cmds.getAttr(item+'.aiCastVolumetricShadows'))
    except:
        pass
    try:
        cmds.intFieldGrp('MeshLight_aiVolumeSample',e=True,v1=cmds.getAttr(item+'.aiVolumeSamples'))
    except:
        pass
    try:
        cmds.textFieldGrp('MeshLight_aiAov',e=True,tx=cmds.getAttr(item+'.aiAov'))
    except:
        pass
    if cmds.radioButton('Single_Check',q=True,sl=True):
        cmds.select(item,r=True)
    elif cmds.radioButton('Double_Check',q=True,sl=True):
        pass
    refreshCounts()

    

def setMeshLightAttrsAndShow(attribute):
    for item in cmds.textScrollList('MeshLightList',q=True,si=True):
        try:
            if attribute == 'translator':
                cmds.setAttr(item+'.aiTranslator',cmds.optionMenu('MeshLight_aiTranslator',q=True,v=True),type='string')
        except:
            pass
        try:
            if attribute == 'color':
                color = cmds.colorSliderGrp('MeshLight_aiColor',q=True,rgb=True)
                cmds.setAttr(item+'.color',color[0],color[1],color[2],type='double3')
        except:
            pass
        try:
            if attribute == 'intensity':
                cmds.setAttr(item+'.intensity',cmds.floatSliderGrp('MeshLight_aiIntensity',q=True,v=True))
        except:
            pass
        try:
            if attribute == 'exposure':
                cmds.setAttr(item+'.aiExposure',cmds.floatSliderGrp('MeshLight_aiExposure',q=True,v=True))
        except:
            pass
        try:
            if attribute == 'useTemp':
                cmds.setAttr(item+'.aiUseColorTemperature',cmds.checkBox('MeshLight_aiUseTemp',q=True,v=True))
        except:
            pass
        try:
            if attribute == 'temp':
                cmds.setAttr(item+'.aiColorTemperature',cmds.floatSliderGrp('MeshLight_aiTemperature',q=True,v=True))
        except:
            pass
        try:
            if attribute == 'visible':
                cmds.setAttr(item+'.lightVisible',cmds.checkBox('MeshLight_aiVisible',q=True,v=True))
        except:
            pass
        try:
            if attribute == 'sample':
                cmds.setAttr(item+'.aiSamples',cmds.intFieldGrp('MeshLight_aiSample',q=True,v1=True))
        except:
            pass
        try:
            if attribute == 'normalize':
                cmds.setAttr(item+'.aiNormalize',cmds.checkBox('MeshLight_aiNormalize',q=True,v=True))
        except:
            pass
        try:
            if attribute == 'castShadows':
                cmds.setAttr(item+'.aiCastShadows',cmds.checkBox('MeshLight_aiCastShadows',q=True,v=True))
        except:
            pass
        try:
            if attribute == 'shadowDensity':
                cmds.setAttr(item+'.aiShadowDensity',cmds.floatSliderGrp('MeshLight_aiShadowDensity',q=True,v=True))
        except:
            pass
        try:
            if attribute == 'shadowColor':
                shadowColor = cmds.colorSliderGrp('MeshLight_aiShadowColor',q=True,rgb=True)
                cmds.setAttr(item+'.aiShadowColor',shadowColor[0],shadowColor[1],shadowColor[2],type='double3')
        except:
            pass
        try:
            if attribute == 'castVolumeShadow':
                cmds.setAttr(item+'.aiCastVolumetricShadows',cmds.checkBox('MeshLight_aiCastVolumeShadow',q=True,v=True))
        except:
            pass
        try:
            if attribute == 'volumeSample':
                cmds.setAttr(item+'.aiVolumeSamples',cmds.intFieldGrp('MeshLight_aiVolumeSample',q=True,v1=True))
        except:
            pass
        try:
            if attribute == 'aiAov':
                cmds.setAttr(item+'.aiAov',cmds.textFieldGrp('MeshLight_aiAov',q=True,tx=True),type='string')
        except:
            pass

def convertMeshToMeshLight():
    meshList = cmds.ls(sl=True,dag=True,ni=True)
    if len(meshList) > 0:
        for mesh in meshList:
            try:
                cmds.setAttr(mesh+'.aiTranslator','mesh_light',type='string')
            except:
                pass
            if len(cmds.textFieldGrp('MeshLight_Template',q=True,tx=True))>0:
                attrs = getTemplateAttrs()
                try:
                    cmds.setAttr(mesh+'.color',attrs[1][0][0],attrs[1][0][1],attrs[1][0][2],type='double3')
                except:
                    pass
                try:
                    cmds.setAttr(mesh+'.intensity',attrs[2])
                except:
                    pass
                try:
                    cmds.setAttr(mesh+'.aiExposure',attrs[3])
                except:
                    pass
                try:
                    cmds.setAttr(mesh+'.aiUseColorTemperature',attrs[4])
                except:
                    pass
                try:
                    cmds.setAttr(mesh+'.aiColorTemperature',attrs[5])
                except:
                    pass
                try:
                    cmds.setAttr(mesh+'.lightVisible',attrs[6])
                except:
                    pass
                try:
                    cmds.setAttr(mesh+'.aiSamples',attrs[7])
                except:
                    pass
                try:
                    cmds.setAttr(mesh+'.aiNormalize',attrs[8])
                except:
                    pass
                try:
                    cmds.setAttr(mesh+'.aiCastShadows',attrs[9])
                except:
                    pass
                try:
                    cmds.setAttr(mesh+'.aiShadowDensity',attrs[10])
                except:
                    pass
                try:
                    cmds.setAttr(mesh+'.aiShadowColor',attrs[11][0][1],attrs[11][0][1],attrs[11][0][2],type='double3')
                except:
                    pass
                try:
                    cmds.setAttr(mesh+'.aiCastVolumetricShadows',attrs[12])
                except:
                    pass
                try:
                    cmds.setAttr(mesh+'.aiVolumeSamples',attrs[13])
                except:
                    pass
                try:
                    cmds.setAttr(mesh+'.aiAov',attrs[14],type='string')
                except:
                    pass
        cmds.radioButton('SelLightCheck',e=True,sl=True)
        cmds.checkBox('List_NormalLight',e=True,v=1)
        cmds.checkBox('List_MeshLight',e=True,v=1)
        lightListRefresh()

def getTemplateAttrs():
    template = cmds.textFieldGrp('MeshLight_Template',q=True,tx=True)
    attrTempList = list()
    try:
        attrTempList.append(cmds.getAttr(template+'.aiTranslator'))
    except:
        attrTempList.append(' ')
    try:
        attrTempList.append(cmds.getAttr(template+'.color'))
    except:
        attrTempList.append(' ')
    try:
        attrTempList.append(cmds.getAttr(template+'.intensity'))
    except:
        attrTempList.append(' ')
    try:
        attrTempList.append(cmds.getAttr(template+'.aiExposure'))
    except:
        attrTempList.append(' ')
    try:    
        attrTempList.append(cmds.getAttr(template+'.aiUseColorTemperature'))
    except:
        attrTempList.append(' ')
    try:
        attrTempList.append(cmds.getAttr(template+'.aiColorTemperature'))
    except:
        attrTempList.append(' ')
    try:
        attrTempList.append(cmds.getAttr(template+'.lightVisible'))
    except:
        attrTempList.append(' ')
    try:
        attrTempList.append(cmds.getAttr(template+'.aiSamples'))
    except:
        attrTempList.append(' ')
    try:
        attrTempList.append(cmds.getAttr(template+'.aiNormalize'))
    except:
        attrTempList.append(' ')
    try:
        attrTempList.append(cmds.getAttr(template+'.aiCastShadows'))
    except:
        attrTempList.append(' ')
    try:
        attrTempList.append(cmds.getAttr(template+'.aiShadowDensity'))
    except:
        attrTempList.append(' ')
    try:
        attrTempList.append(cmds.getAttr(template+'.aiShadowColor'))
    except:
        attrTempList.append(' ')
    try:
        attrTempList.append(cmds.getAttr(template+'.aiCastVolumetricShadows'))
    except:
        attrTempList.append(' ')
    try:
        attrTempList.append(cmds.getAttr(template+'.aiVolumeSamples'))
    except:
        attrTempList.append(' ')
    try:
        attrTempList.append(cmds.getAttr(template+'.aiAov'))
    except:
        attrTempList.append(' ')
    return attrTempList

def getAllLights():
    lights = cmds.ls(lights=True)
    arnoldLightType = ['aiAreaLight','aiSkyDomeLight','aiMeshLight','aiPhotometricLight']
    #legacyMeshLight = list()
    
    for aiType in arnoldLightType:
        for aiLight in cmds.ls(type=aiType):
            lights.append(aiLight)
    for mesh in cmds.ls(ni=True,type='mesh'):
        if cmds.getAttr(mesh+'.aiTranslator') == 'mesh_light':
            lights.append(mesh)
        
    return lights

def getAllLightGroup():
    lightGroupNameList = list()
    for light in getAllLights():
        lightGroupName = cmds.getAttr(light+'.aiAov')
        lightGroupNameList.append(lightGroupName)
    return list(set(lightGroupNameList))    

def refreshLightGroupMenu():
    cmds.textScrollList('MeshLight_LightGroupList',e=True,ra=True)
    for i in getAllLightGroup():
        cmds.textScrollList('MeshLight_LightGroupList',e=True,a=i)

def setLightGroupFromMenu():
    for item in cmds.textScrollList('MeshLightList',q=True,si=True):
        cmds.setAttr(item+'.aiAov',cmds.textScrollList('MeshLight_LightGroupList',q=True,si=True)[0],type='string')

def selectLightByGroupName():
    satLight = list()
    for light in getAllLights():
        for groupName in cmds.textScrollList('MeshLight_LightGroupList',q=True,si=True):
        
            if cmds.getAttr(light+'.aiAov') == groupName:
                satLight.append(light)
    cmds.select(satLight,r=True)
    cmds.radioButton('SelLightCheck',e=True,sl=True)
    cmds.checkBox('List_NormalLight',e=True,v=1)
    cmds.checkBox('List_MeshLight',e=True,v=1)
    lightListRefresh()

def genAovString():
    stringTemp = str()
    for string in cmds.textScrollList('MeshLight_LightGroupList',q=True,si=True):
        stringTemp += string
        stringTemp += ' '
    cmds.textFieldGrp('AOVString',e=True,tx=stringTemp)

def refreshCounts():
    cmds.text('ListTotalNumber',e=True,l=cmds.textScrollList('MeshLightList',q=True,ni=True))
    cmds.text('ListSelectNumber',e=True,l=cmds.textScrollList('MeshLightList',q=True,nsi=True))

def displayLightColorAsWireframe():
    for item in cmds.textScrollList('MeshLightList',q=True,si=True):
        try:
            cmds.setAttr(item+'.overrideEnabled',1)
            cmds.setAttr(item+'.overrideRGBColors',1)
            lightColor = cmds.getAttr(item+'.color')
            cmds.setAttr(item+'.overrideColorRGB',lightColor[0][0],lightColor[0][1],lightColor[0][2],type='double3')
        except:
            print item
            continue

def createAreaLight():
    selectTransforms = cmds.ls(sl=True,ni=True,dag=True,tr=True)

    if len(selectTransforms) == 0:
        newlight = core.createArnoldNode('aiAreaLight')
        return newlight.name()
    else:
        for transform in cmds.ls(sl=True,dag=True,ni=True,tr=True):
            position = cmds.xform(transform,q=True,piv=True,ws=True)
            newAiAreaLight = core.createArnoldNode('aiAreaLight')
            cmds.move(position[0],position[1],position[2],newAiAreaLight.name())

def getAiLightFilters():
    aiLightFilterList = ['aiBarndoor','aiLightDecay','aiGobo','aiLightBlocker']
    allFilters = list()
    for filter in aiLightFilterList:
        for item in cmds.ls(type=filter):
            allFilters.append(item)
    return list(set(allFilters))

def refreshAiLightFilterList():
    cmds.textScrollList('LightFilterList',e=True,ra=True)
    for item in getAiLightFilters():
        cmds.textScrollList('LightFilterList',e=True,a=item)

def connectSpareFiltersIndice(fromAttr,toAttr):
    tempIndices = list()
    
    if cmds.getAttr(toAttr,mi=True) is None:
        cmds.connectAttr(fromAttr,toAttr+'[0]')
    for index in cmds.getAttr(toAttr,mi=True):
        if cmds.isConnected(fromAttr,toAttr+'['+str(index)+']'):
            return
        if len(cmds.connectionInfo(toAttr+'['+str(index)+']',sfd=True))==0:
            cmds.connectAttr(fromAttr,toAttr+'['+str(index)+']')            
            return
        tempIndices.append(index)
    tempIndices = sorted(tempIndices)
    cmds.connectAttr(fromAttr,toAttr+'['+str(len(tempIndices))+']')
    
def disconnectExistsFilters():
    for item in cmds.textScrollList('MeshLightList',q=True,si=True):
        for filter in cmds.textScrollList('LightFilterList',q=True,si=True):    
            for index in cmds.getAttr(item+'.aiFilters',mi=True):
                if cmds.isConnected(filter+'.message',item+'.aiFilters['+str(index)+']'):
                    cmds.disconnectAttr(filter+'.message',item+'.aiFilters['+str(index)+']')

def connectAiLightFilter():
    errors = list()
    filter_blocker_avaiableType = ['directionalLight','spotLight','pointLight','aiAreaLight','aiSkyDomeLight','aiMeshLight','mesh','aiPhotometricLight']
    filter_barndoor_avaiableType = ['spotLight']
    filter_decay_avaiableType = ['spotLight','pointLight','aiAreaLight','mesh','aiMeshLight','aiPhotometricLight']
    filter_gobo_avaiableType = ['spotLight']
    for item in cmds.textScrollList('MeshLightList',q=True,si=True):
    
        for filter in cmds.textScrollList('LightFilterList',q=True,si=True):
            if cmds.nodeType(filter) == 'aiLightBlocker' and filter_blocker_avaiableType.count(cmds.nodeType(item)) == 1:
                connectSpareFiltersIndice(filter+'.message',item+'.aiFilters')
                #errors.append(item +' cannot use the filter : ---- |' + filter + '| ---- ')
            if cmds.nodeType(filter) == 'aiBarndoor' and filter_barndoor_avaiableType.count(cmds.nodeType(item)) == 1:

                connectSpareFiltersIndice(filter+'.message',item+'.aiFilters')

            if cmds.nodeType(filter) == 'aiLightDecay' and filter_decay_avaiableType.count(cmds.nodeType(item)) == 1:
                connectSpareFiltersIndice(filter+'.message',item+'.aiFilters')

            if cmds.nodeType(filter) == 'aiGobo' and filter_gobo_avaiableType.count(cmds.nodeType(item)) == 1:
                connectSpareFiltersIndice(filter+'.message',item+'.aiFilters')
    #print errors

global objectColorCacheList

def colorAnalyzer():
    global objectColorCacheList
    buttonList = list()
    objectColorCacheList = list()
    tolerance = 0.01
    recurseColorFilter(cmds.textScrollList('MeshLightList',q=True,si=True),tolerance)
    
    if cmds.window('ColoredLightButtonWindow',ex=True):
        cmds.deleteUI('ColoredLightButtonWindow')
    
    cmds.window('ColoredLightButtonWindow',t='Select Light By Color')
    
    numbers = len(objectColorCacheList)
    recs = int(math.ceil(pow(numbers,0.5)))
    cmds.rowColumnLayout('ColoredButton_MainLayout',nc=numbers/recs)
    cmds.showWindow('ColoredLightButtonWindow')
    
    for button in range(0,numbers):
        color = cmds.getAttr(objectColorCacheList[button][0]+'.color')
        annotation = str()
        for object in objectColorCacheList[button]:
            annotation += object + ' '
            
        cmds.button(l=' ',p='ColoredButton_MainLayout',w=40,h=40,bgc=color[0],ann=annotation,c='cmds.select('+str(objectColorCacheList[button])+',r=True)')
    #button command require 'string' or 'function object', use string to parse arguments to function

def recurseColorFilter(objectNameList,tol):
    global objectColorCacheList

    subObjectList = list()
        
    if len(objectNameList) == 0:
        return
    if len(objectNameList) == 1:
        subObjectList.append(objectNameList[0])
        objectColorCacheList.append(subObjectList)
        return
    templateColorAttr = cmds.getAttr(objectNameList[0]+'.color')
    subObjectList.append(objectNameList[0])
    
    for i in range(1,len(objectNameList)):
        #print objectNameList[i]
        colorAttr = cmds.getAttr(objectNameList[i]+'.color')
        if abs(colorAttr[0][0] - templateColorAttr[0][0]) <= tol and abs(colorAttr[0][1] - templateColorAttr[0][1]) <= tol and abs(colorAttr[0][2] - templateColorAttr[0][2]) <= tol:
            subObjectList.append(objectNameList[i])

    for item in subObjectList:
        objectNameList.remove(item)
        
    objectColorCacheList.append(subObjectList)
    recurseColorFilter(objectNameList,tol)

def hsv2rgb(h,s,v):
    c = v * s
    h1 = h / 60.0
    x = c * (1.0 - abs((h1 % 2) - 1.0))
    m = v - c
    r = 0.0
    g = 0.0
    b = 0.0
    if h1>=0 and h1<1:
        r = c
        g = x
        b = 0
    elif h1>=1 and h1<2:
        r = x
        g = c
        b = 0
    elif h1>=2 and h1<3:
        r = 0
        g = c
        b = x
    elif h1>=3 and h1<4:
        r = 0
        g = x
        b = c
    elif h1>=4 and h1<5:
        r = x
        g = 0
        b = c
    elif h1>=5 and h1<=6: #如果不等于6，则360的时候会为黑色
        r = c
        g = 0
        b = x
    else:
        r = 0
        g = 0
        b = 0
    return (r+m,g+m,b+m)
        
def rgb2hsv(r,g,b):
    cmax = max(r,g,b)
    cmin = min(r,g,b)
    
    delta = cmax - cmin
    
    if delta == 0:
        h = 0
    elif cmax == r:
        h = 60 * ((g - b) / delta % 6)
    elif cmax == g:
        h = 60 * ((b - r) / delta + 2)
    elif cmax == b:
        h = 60 * ((r - g) / delta + 4)
    
    if cmax == 0:
        s = 0
    else:
        s = delta / cmax
    
    v = cmax
    
    return (h,s,v)

def colorSliderAction():
    color = cmds.colorInputWidgetGrp('Color_Sets',q=True,rgb=True)
    for item in cmds.ls(sl=True,dag=True,ni=True,s=True):
        cmds.setAttr(item+'.color',color[0],color[1],color[2])
        try:
            #cmds.setAttr(item+'.overrideEnabled',1)
            #cmds.setAttr(item+'.overrideRGBColors',1)
            cmds.setAttr(item+'.overrideColorRGB',color[0],color[1],color[2],type='double3')
        except:
            continue

def hsvColorKeyframeAction():
    fhsv = cmds.colorInputWidgetGrp('Color_From',q=True,hsv=True)
    thsv = cmds.colorInputWidgetGrp('Color_To',q=True,hsv=True)

    sTime = cmds.intFieldGrp('HSV_Color_StartTime',q=True,v1=True)
    eTime = cmds.intFieldGrp('HSV_Color_EndTime',q=True,v1=True)
    tStep = cmds.floatFieldGrp('HSV_Color_Step',q=True,v1=True)
    for item in cmds.ls(sl=True,dag=True,s=True,ni=True):
        for i in range(0,int(abs(eTime - sTime)/tStep)+1):
            if eTime - sTime < 0:
                i *= -1
            hchange = (thsv[0] - fhsv[0])/abs(eTime-sTime) * abs(i * tStep) + fhsv[0]
            schange = (thsv[1] - fhsv[1])/abs(eTime-sTime) * abs(i * tStep) + fhsv[1]
            vchange = (thsv[2] - fhsv[2])/abs(eTime-sTime) * abs(i * tStep) + fhsv[2]
            col = hsv2rgb(hchange,schange,vchange)
            try:
                cmds.setKeyframe(item,at='colorR',v=col[0], t=sTime + i * tStep)
                cmds.setKeyframe(item,at='colorG',v=col[1], t=sTime + i * tStep)
                cmds.setKeyframe(item,at='colorB',v=col[2], t=sTime + i * tStep)
            except:
                continue

def hsvColorKeyframeWindow():
    if cmds.window('HSV_Keyframe_Window',ex=True):
        cmds.deleteUI('HSV_Keyframe_Window')
    cmds.window('HSV_Keyframe_Window',t='Color_KeyframeWindow',w=800,h=400)

    cmds.columnLayout(bgc=[0.027,0.027,0.027])
    cmds.frameLayout(l='Color Settings',w=370,li=265,cll=True,bgc=[0.0,0.2,0.4])
    cmds.separator(w=370,h=1,bgc=[0,0.25,0.55],style='none')
    cmds.colorInputWidgetGrp('Color_Sets',cc=lambda *args:colorSliderAction())
    cmds.setParent(u=True)
    cmds.separator(w=370,h=1,bgc=[0,0.25,0.55],style='none')
    cmds.setParent(u=True)
    
    cmds.frameLayout(l='Color Range Keyframe',w=370,li=220,cll=True,bgc=[0.0,0.3,0.65])
    cmds.separator(w=370,h=1,bgc=[0,0.4,0.75],style='none')

    cmds.columnLayout()
    cmds.colorInputWidgetGrp('Color_From',l='From Color')
    cmds.colorInputWidgetGrp('Color_To',l='To Color')

    cmds.separator(w=370,h=20,bgc=[0,0.4,0.8],style='none')
    cmds.rowLayout(nc=2)
    cmds.columnLayout()
    cmds.intFieldGrp('HSV_Color_StartTime',l='Start Frame')
    cmds.intFieldGrp('HSV_Color_EndTime',l='End Frame')
    cmds.floatFieldGrp('HSV_Color_Step',l='Steps',v1=1.0)
    cmds.setParent(u=True)
    cmds.columnLayout()
    
    cmds.button(l='Set Keys',w=120,h=50,c='hsvColorKeyframeAction()',bgc=[0.0,0.1,0.36])
    cmds.setParent(u=True)

    cmds.showWindow('HSV_Keyframe_Window')

createWindow()



