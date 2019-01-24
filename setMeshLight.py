#-*- coding:utf-8 -*-

import maya.cmds as cmds

def createWindow():
    if cmds.window('MeshLightSetter',ex=True):
        cmds.deleteUI('MeshLightSetter')

    cmds.window('MeshLightSetter',t='MeshLight Setter',w=600,h=800)
    cmds.rowLayout(nc=2)
    cmds.frameLayout(l='aiTranslatorAttributes',w=450)
    cmds.formLayout('MeshLight_FormLayout')
    f1 = cmds.optionMenu('MeshLight_aiTranslator')
    cmds.menuItem(l='polymesh',p='MeshLight_aiTranslator')
    cmds.menuItem(l='mesh_light',p='MeshLight_aiTranslator')
    cmds.menuItem(l='procedural',p='MeshLight_aiTranslator')
    f2 = cmds.colorSliderGrp('MeshLight_aiColor',l='Color')
    f3 = cmds.floatFieldGrp('MeshLight_aiIntensity',l='Intensity')
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
    f17 = cmds.button(l='List LightGroup',c=lambda *args:refreshLightGroupMenu(),w=98)
    f18 = cmds.button(l='Set LightGroup',c=lambda *args:setLightGroupFromMenu(),w=98)
    cmds.setParent(u=True)
    f19 = cmds.textScrollList('MeshLight_LightGroupList',w=200,h=372)
    cmds.formLayout('MeshLight_FormLayout',e=True,af = [(f1,'top',0),(f1,'left',140),
                                                        (f2,'top',22),(f2,'left',0),
                                                        (f3,'top',44),(f3,'left',0),
                                                        (f4,'top',66),(f4,'left',0),
                                                        (f5,'top',88),(f5,'left',130),
                                                        (f6,'top',110),(f6,'left',0),
                                                        (f7,'top',132),(f7,'left',130),
                                                        (f8,'top',154),(f8,'left',0),
                                                        (f9,'top',176),(f9,'left',130),
                                                        (f10,'top',198),(f10,'left',130),
                                                        (f11,'top',220),(f11,'left',0),
                                                        (f12,'top',242),(f12,'left',0),
                                                        (f13,'top',264),(f13,'left',130),
                                                        (f14,'top',286),(f14,'left',0),
                                                        (f15,'top',308),(f15,'left',0),
                                                        (f16,'top',333),(f16,'left',130),
                                                        (f19,'top',360),(f19,'left',130)
                                                        ])
    
    
    cmds.setParent(u=True)
    cmds.setParent(u=True)
    cmds.frameLayout(l='Mesh Light List')
    cmds.rowLayout(nc=5)
    cmds.button(l='ALL MESH light',c=lambda *args:lightListRefresh(True))
    cmds.button(l='Sel MESH Light',c=lambda *args:lightListRefresh(False))
    cmds.textFieldGrp('MeshLight_Template',l='Template')
    cmds.button(l='Set Template',c=lambda *args:cmds.textFieldGrp('MeshLight_Template',e=True,tx=cmds.ls(sl=True,dag=True,ni=True,type='mesh')[0]))
    cmds.button(l='Convert!',c=lambda *args:convertMeshToMeshLight())
    cmds.setParent(u=True)
    
    cmds.textScrollList('MeshLightList',w=600,h=700,ams=True)
    cmds.setParent(u=True)

    cmds.popupMenu('MeshLightListMenu',p='MeshLightList')
    cmds.menuItem(l='Select...',p='MeshLightListMenu',c=lambda *args:cmds.select([item for item in cmds.textScrollList('MeshLightList',q=True,si=True)]))

    cmds.showWindow('MeshLightSetter')

    cmds.textScrollList('MeshLightList',e=True,dcc=lambda *args:cmds.select(cmds.textScrollList('MeshLightList',q=True,si=True),r=True))
    cmds.textScrollList('MeshLightList',e=True,sc=lambda *args:getMeshLightAttrsAndShow())
    cmds.textScrollList('MeshLight_LightGroupList',e=True,dcc=lambda *args:selectLightByGroupName())
    cmds.optionMenu(f1,e=True,cc=lambda *args:setMeshLightAttrsAndShow('translator'))
    cmds.colorSliderGrp(f2,e=True,cc=lambda *args:setMeshLightAttrsAndShow('color'))
    cmds.floatFieldGrp(f3,e=True,cc=lambda *args:setMeshLightAttrsAndShow('intensity'))
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

def getMeshLight(allNode):
    meshLightList = list()
    
    if allNode == True:
        meshLightList = cmds.ls(dag=True,type='mesh')
    else:
        meshLightList = cmds.ls(sl=True,dag=True,type='mesh')

    availableMeshLight = list()
    for mesh in meshLightList:
        if cmds.getAttr(mesh+'.aiTranslator') == 'mesh_light':
            availableMeshLight.append(mesh)
    return availableMeshLight


def lightListRefresh(allNode):
    cmds.textScrollList('MeshLightList',e=True,ra=True)
    for item in getMeshLight(allNode):
        cmds.textScrollList('MeshLightList',e=True,a=item)



def getMeshLightAttrsAndShow():
    item = cmds.textScrollList('MeshLightList',q=True,si=True)[0]
    if cmds.getAttr(item+'.aiTranslator') == 'polyMesh':
        cmds.optionMenu('MeshLight_aiTranslator',e=True,sl=1)
    elif cmds.getAttr(item+'.aiTranslator') == 'mesh_light':
        cmds.optionMenu('MeshLight_aiTranslator',e=True,sl=2)
    else:
        cmds.optionMenu('MeshLight_aiTranslator',e=True,sl=3)
    
    cmds.colorSliderGrp('MeshLight_aiColor',e=True,rgb=cmds.getAttr(item+'.color')[0])
    cmds.floatFieldGrp('MeshLight_aiIntensity',e=True,v1=cmds.getAttr(item+'.intensity'))
    cmds.floatSliderGrp('MeshLight_aiExposure',e=True,v=cmds.getAttr(item+'.aiExposure'))
    cmds.checkBox('MeshLight_aiUseTemp',e=True,v=cmds.getAttr(item+'.aiUseColorTemperature'))
    cmds.floatSliderGrp('MeshLight_aiTemperature',e=True,v=cmds.getAttr(item+'.aiColorTemperature'))
    cmds.checkBox('MeshLight_aiVisible',e=True,v=cmds.getAttr(item+'.lightVisible'))
    cmds.intFieldGrp('MeshLight_aiSample',e=True,v1=cmds.getAttr(item+'.aiSamples'))
    cmds.checkBox('MeshLight_aiNormalize',e=True,v=cmds.getAttr(item+'.aiNormalize'))
    cmds.checkBox('MeshLight_aiCastShadows',e=True,v=cmds.getAttr(item+'.aiCastShadows'))
    cmds.floatSliderGrp('MeshLight_aiShadowDensity',e=True,v=cmds.getAttr(item+'.aiShadowDensity'))
    cmds.colorSliderGrp('MeshLight_aiShadowColor',e=True,rgb=cmds.getAttr(item+'.aiShadowColor')[0])
    cmds.checkBox('MeshLight_aiCastVolumeShadow',e=True,v=cmds.getAttr(item+'.aiCastVolumetricShadows'))
    cmds.intFieldGrp('MeshLight_aiVolumeSample',e=True,v1=cmds.getAttr(item+'.aiVolumeSamples'))
    cmds.textFieldGrp('MeshLight_aiAov',e=True,tx=cmds.getAttr(item+'.aiAov'))


def setMeshLightAttrsAndShow(attribute):
    for item in cmds.textScrollList('MeshLightList',q=True,si=True):
        if attribute == 'translator':
            cmds.setAttr(item+'.aiTranslator',cmds.optionMenu('MeshLight_aiTranslator',q=True,v=True),type='string')
        if attribute == 'color':
            color = cmds.colorSliderGrp('MeshLight_aiColor',q=True,rgb=True)
            cmds.setAttr(item+'.color',color[0],color[1],color[2],type='double3')
        if attribute == 'intensity':
            cmds.setAttr(item+'.intensity',cmds.floatFieldGrp('MeshLight_aiIntensity',q=True,v1=True))
        if attribute == 'exposure':
            cmds.setAttr(item+'.aiExposure',cmds.floatSliderGrp('MeshLight_aiExposure',q=True,v=True))
        if attribute == 'useTemp':
            cmds.setAttr(item+'.aiUseColorTemperature',cmds.checkBox('MeshLight_aiUseTemp',q=True,v=True))
        if attribute == 'temp':
            cmds.setAttr(item+'.aiColorTemperature',cmds.floatSliderGrp('MeshLight_aiTemperature',q=True,v=True))
        if attribute == 'visible':
            cmds.setAttr(item+'.lightVisible',cmds.checkBox('MeshLight_aiVisible',q=True,v=True))
        if attribute == 'sample':
            cmds.setAttr(item+'.aiSamples',cmds.intFieldGrp('MeshLight_aiSample',q=True,v1=True))
        if attribute == 'normalize':
            cmds.setAttr(item+'.aiNormalize',cmds.checkBox('MeshLight_aiNormalize',q=True,v=True))
        if attribute == 'castShadows':
            cmds.setAttr(item+'.aiCastShadows',cmds.checkBox('MeshLight_aiCastShadows',q=True,v=True))
        if attribute == 'shadowDensity':
            cmds.setAttr(item+'.aiShadowDensity',cmds.floatSliderGrp('MeshLight_aiShadowDensity',q=True,v=True))
        if attribute == 'shadowColor':
            shadowColor = cmds.colorSliderGrp('MeshLight_aiShadowColor',q=True,rgb=True)
            cmds.setAttr(item+'.aiShadowColor',shadowColor[0],shadowColor[1],shadowColor[2],type='double3')
        if attribute == 'castVolumeShadow':
            cmds.setAttr(item+'.aiCastVolumetricShadows',cmds.checkBox('MeshLight_aiCastVolumeShadow',q=True,v=True))
        if attribute == 'volumeSample':
            cmds.setAttr(item+'.aiVolumeSamples',cmds.intFieldGrp('MeshLight_aiVolumeSample',q=True,v1=True))
        if attribute == 'aiAov':
            cmds.setAttr(item+'.aiAov',cmds.textFieldGrp('MeshLight_aiAov',q=True,tx=True),type='string')


def convertMeshToMeshLight():
    meshList = cmds.ls(sl=True,dag=True,ni=True,type='mesh')
    if len(meshList) > 0:
        for mesh in meshList:
            cmds.setAttr(mesh+'.aiTranslator','mesh_light',type='string')
            if len(cmds.textFieldGrp('MeshLight_Template',q=True,tx=True))>0:
                attrs = getTemplateAttrs()
                cmds.setAttr(mesh+'.color',attrs[1][0][0],attrs[1][0][1],attrs[1][0][2],type='double3')
                cmds.setAttr(mesh+'.intensity',attrs[2])
                cmds.setAttr(mesh+'.aiExposure',attrs[3])
                cmds.setAttr(mesh+'.aiUseColorTemperature',attrs[4])
                cmds.setAttr(mesh+'.aiColorTemperature',attrs[5])
                cmds.setAttr(mesh+'.lightVisible',attrs[6])
                cmds.setAttr(mesh+'.aiSamples',attrs[7])
                cmds.setAttr(mesh+'.aiNormalize',attrs[8])
                cmds.setAttr(mesh+'.aiCastShadows',attrs[9])
                cmds.setAttr(mesh+'.aiShadowDensity',attrs[10])
                cmds.setAttr(mesh+'.aiShadowColor',attrs[11][0][1],attrs[11][0][1],attrs[11][0][2],type='double3')
                cmds.setAttr(mesh+'.aiCastVolumetricShadows',attrs[12])
                cmds.setAttr(mesh+'.aiVolumeSamples',attrs[13])
                cmds.setAttr(mesh+'.aiAov',attrs[14],type='string')
        lightListRefresh(False)

def getTemplateAttrs():
    template = cmds.textFieldGrp('MeshLight_Template',q=True,tx=True)
    return [cmds.getAttr(template+'.aiTranslator'),
            cmds.getAttr(template+'.color'),
            cmds.getAttr(template+'.intensity'),
            cmds.getAttr(template+'.aiExposure'),
            cmds.getAttr(template+'.aiUseColorTemperature'),
            cmds.getAttr(template+'.aiColorTemperature'),
            cmds.getAttr(template+'.lightVisible'),
            cmds.getAttr(template+'.aiSamples'),
            cmds.getAttr(template+'.aiNormalize'),
            cmds.getAttr(template+'.aiCastShadows'),
            cmds.getAttr(template+'.aiShadowDensity'),
            cmds.getAttr(template+'.aiShadowColor'),
            cmds.getAttr(template+'.aiCastVolumetricShadows'),
            cmds.getAttr(template+'.aiVolumeSamples'),
            cmds.getAttr(template+'.aiAov')]


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
    lightListRefresh(False)

createWindow()