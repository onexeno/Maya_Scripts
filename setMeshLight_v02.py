#-*- coding:utf-8 -*-

import maya.cmds as cmds

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
    f19 = cmds.textFieldGrp('AOVString',l='AOVs')
    f20 = cmds.textScrollList('MeshLight_LightGroupList',w=200,h=372)
    
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
                                                        (f16,'top',333),(f16,'left',90),
                                                        (f19,'top',360),(f19,'left',-40),
                                                        (f20,'top',383),(f20,'left',90)
                                                        ])
    
    
    cmds.setParent(u=True)
    cmds.setParent(u=True)
    cmds.frameLayout(l='Mesh Light List',w=400)
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
    cmds.formLayout('MeshLightList_FormLayout',e=True,af = [(w1,'top',3),(w1,'left',0),
                                                            (w2,'top',3),(w2,'left',101),
                                                            (w3,'top',3),(w3,'left',205),
                                                            (w4,'top',3),(w4,'left',320),
                                                            (w5,'top',27),(w5,'left',-90),
                                                            (w6,'top',27),(w6,'left',297),
                                                            (w7,'top',52),(w7,'left',297),
                                                            (w8,'top',77),(w8,'left',0),
                                                            (w9,'top',55),(w9,'left',0),
                                                            (w10,'top',55),(w10,'left',50)
                                                            ])
    cmds.popupMenu('MeshLightListMenu',p='MeshLightList')
    cmds.menuItem(l='Select...',p='MeshLightListMenu',c=lambda *args:cmds.select([item for item in cmds.textScrollList('MeshLightList',q=True,si=True)]))

    cmds.showWindow('MeshLightSetter')

    cmds.textScrollList('MeshLightList',e=True,dcc=lambda *args:cmds.select(cmds.textScrollList('MeshLightList',q=True,si=True),r=True))
    cmds.textScrollList('MeshLightList',e=True,sc=lambda *args:getMeshLightAttrsAndShow())
    cmds.textScrollList('MeshLight_LightGroupList',e=True,ams=True,sc=lambda *args:genAovString(),dcc=lambda *args:selectLightByGroupName())
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
    cmds.radioButton('AllLightCheck',e=True,cc=lambda *args:lightListRefresh())
    cmds.radioButton('SelLightCheck',e=True,cc=lambda *args:lightListRefresh())
    cmds.checkBox('List_NormalLight',e=True,cc=lambda *args:lightListRefresh())
    cmds.checkBox('List_MeshLight',e=True,cc=lambda *args:lightListRefresh())

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
        meshLightList = cmds.ls(dag=True,type='mesh')
    else:
        meshLightList = cmds.ls(sl=True,dag=True,type='mesh')

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
        else:
            cmds.optionMenu('MeshLight_aiTranslator',e=True,sl=3)
    except:
        pass
    try:
        cmds.colorSliderGrp('MeshLight_aiColor',e=True,rgb=cmds.getAttr(item+'.color')[0])
    except:
        pass
    try:
        cmds.floatFieldGrp('MeshLight_aiIntensity',e=True,v1=cmds.getAttr(item+'.intensity'))
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
                cmds.setAttr(item+'.intensity',cmds.floatFieldGrp('MeshLight_aiIntensity',q=True,v1=True))
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

createWindow()