#-*- coding: utf-8 -*-
import maya.cmds as cmds
from mtoa import aovs
import os
import re
#aovs.AOVInterface.addAOV()

cmds.setAttr('defaultRenderGlobals.currentRenderer','arnold',type='string')

def createAOVs(aovList):
    aov = aovs.AOVInterface()
    for aovName in aovList:
        aov.addAOV(aovName)


def createFile(name,type):
    tex2D = cmds.shadingNode("place2dTexture",n=name + "_placement2DTexture",au=True,ss=True)
    texNode = cmds.shadingNode(type,n=name,au=True,ss=True)
    if type == "file":
        cmds.connectAttr((tex2D + ".coverage"),(texNode + ".coverage"),f=True)
        cmds.connectAttr((tex2D + ".translateFrame"),(texNode + ".translateFrame"),f=True)
        cmds.connectAttr((tex2D + ".rotateFrame"),(texNode + ".rotateFrame"),f=True)
        cmds.connectAttr((tex2D + ".mirrorU"),(texNode + ".mirrorU"),f=True)
        cmds.connectAttr((tex2D + ".mirrorV"),(texNode + ".mirrorV"),f=True)
        cmds.connectAttr((tex2D + ".stagger"),(texNode + ".stagger"),f=True)
        cmds.connectAttr((tex2D + ".wrapU"),(texNode + ".wrapU"),f=True)
        cmds.connectAttr((tex2D + ".wrapV"),(texNode + ".wrapV"),f=True)
        cmds.connectAttr((tex2D + ".repeatUV"),(texNode + ".repeatUV"),f=True)
        cmds.connectAttr((tex2D + ".offset"),(texNode + ".offset"),f=True)
        cmds.connectAttr((tex2D + ".rotateUV"),(texNode + ".rotateUV"),f=True)
        cmds.connectAttr((tex2D + ".noiseUV"),(texNode + ".noiseUV"),f=True)
        cmds.connectAttr((tex2D + ".vertexUvOne"),(texNode + ".vertexUvOne"),f=True)
        cmds.connectAttr((tex2D + ".vertexUvTwo"),(texNode + ".vertexUvTwo"),f=True)
        cmds.connectAttr((tex2D + ".vertexUvThree"),(texNode + ".vertexUvThree"),f=True)
        cmds.connectAttr((tex2D + ".vertexCameraOne"),(texNode + ".vertexCameraOne"),f=True)
     
    cmds.connectAttr((tex2D+".outUV"),(texNode+".uv"),f=True)
    cmds.connectAttr((tex2D+".outUvFilterSize"),(texNode+".uvFilterSize"),f=True)
    return texNode

def materialNetwork(lightColorFile,darkColorFile,charname,shadingEngine,viewOrRender):
    
    component = charname + '_' + viewOrRender + '_' + shadingEngine

    outputSurfaceShader = cmds.shadingNode('surfaceShader',asShader=True,ss=True,n=component + '_Output_surfaceShader')
    

    ramp = cmds.shadingNode('ramp',at=True,ss=True,n=component + '_Ramp')
    cmds.setAttr(ramp + '.interpolation',0)
    cmds.setAttr(ramp + '.colorEntryList[0].color',1.0,1.0,1.0)
    cmds.setAttr(ramp + '.colorEntryList[0].position',0.0)
    cmds.setAttr(ramp + '.colorEntryList[1].color',0.0,0.0,0.0)
    cmds.setAttr(ramp + '.colorEntryList[1].position',0.2)

    sampler = ''
    if viewOrRender == 'View':
        if cmds.objExists('Global_View_Sampler') is False:
            sampler = cmds.shadingNode('lambert',asShader=True,ss=True,n='Global_View_Sampler')
            cmds.setAttr(sampler + '.color',1.0,1.0,1.0)
            cmds.setAttr(sampler + '.diffuse',1.0)
        sampler = 'Global_View_Sampler'
        cmds.connectAttr(sampler + '.outColorR',ramp + '.vCoord')
        existSurfaceShader = cmds.connectionInfo(shadingEngine + '.surfaceShader',sfd=True)
        if len(existSurfaceShader) > 0:
            cmds.disconnectAttr(existSurfaceShader,shadingEngine + '.surfaceShader')
        cmds.connectAttr(outputSurfaceShader + '.outColor',shadingEngine + '.surfaceShader',f=True)
    elif viewOrRender == 'Render':
        if cmds.objExists('Global_Render_Sampler') is False:
            sampler = cmds.shadingNode('surfaceLuminance',au=True,ss=True,n='Global_Render_Sampler')
        sampler = 'Global_Render_Sampler'
        cmds.connectAttr(sampler + '.outValue',ramp + '.vCoord')
        existAiSurfaceShader = cmds.connectionInfo(shadingEngine + '.aiSurfaceShader',sfd=True)
        if len(existAiSurfaceShader) > 0:
            cmds.disconnectAttr(existAiSurfaceShader,shadingEngine + '.aiSurfaceShader')
        cmds.connectAttr(outputSurfaceShader + '.outColor',shadingEngine + '.aiSurfaceShader',f=True)

    layeredTexture = cmds.shadingNode('layeredTexture',at=True,ss=True,n=component + '_LayeredTexture')

    cmds.connectAttr(darkColorFile + '.outColor',layeredTexture + '.inputs[0].color',f=True)
    cmds.connectAttr(lightColorFile + '.outColor',layeredTexture + '.inputs[1].color',f=True)
    cmds.connectAttr(ramp + '.outAlpha',layeredTexture + '.inputs[0].alpha',f=True)
    cmds.setAttr(layeredTexture + '.inputs[0].blendMode',1)

    cmds.connectAttr(layeredTexture + '.outColor',outputSurfaceShader + '.outColor')
    
    if viewOrRender == 'Render':
        lightColorTex = createFile(charname + '_' + shadingEngine + '_LightColor_File','file')
        darkColorTex = createFile(charname + '_' + shadingEngine + '_DarkColor_File','file')
        drawShadowTex = createFile(charname + '_' + shadingEngine + '_ShadowMask_File','file')
        lineColorTex = ''
        lineColorRamp = ''
        if cmds.checkBox('Line_Checkbox',q=True,v=True):
            lineColorTex = createFile(charname + '_' + shadingEngine + '_Line_File','file')

            lineColorRamp = cmds.shadingNode('ramp',at=True,ss=True,n=charname + '_' + shadingEngine + '_Line_Ramp')
            cmds.setAttr(lineColorRamp+'.colorEntryList[0].color',1.0,1.0,1.0)
            cmds.setAttr(lineColorRamp+'.colorEntryList[0].position',0.0)
            cmds.setAttr(lineColorRamp+'.colorEntryList[1].color',0.0,0.0,0.0)
            cmds.setAttr(lineColorRamp+'.colorEntryList[1].position',1.0)
            cmds.connectAttr(lineColorTex+'.outColorR',lineColorRamp+'.vCoord')

        shadowLayeredTex = cmds.shadingNode('layeredTexture',au=True,ss=True,n=charname + '_' + shadingEngine + '_ShadowLayeredTexture')
        cmds.connectAttr(ramp+'.outAlpha',shadowLayeredTex+'.inputs[0].alpha')
        cmds.setAttr(shadowLayeredTex+'.inputs[0].color',1.0,0.0,0.0)
        cmds.setAttr(shadowLayeredTex+'.inputs[0].blendMode',4)
        cmds.connectAttr(drawShadowTex+'.outColorB',shadowLayeredTex+'.inputs[1].alpha')
        cmds.setAttr(shadowLayeredTex+'.inputs[1].color',0.0,0.0,1.0)
        cmds.setAttr(shadowLayeredTex+'.inputs[1].blendMode',4)

        if re.search('([H|h]air|[T|t]ou[F|f]a|TF)',shadingEngine) is not None or cmds.checkBox('Spec_Checkbox',q=True,v=True):
            cmds.connectAttr(drawShadowTex+'.outColorG',shadowLayeredTex+'.inputs[2].alpha')
            cmds.setAttr(shadowLayeredTex+'.inputs[2].color',0.0,1.0,0.0)
        

        for i in cmds.getAttr(shadingEngine+'.aiCustomAOVs',mi=True):
            if cmds.getAttr(shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovName') == 'Light_Color':
                cmds.connectAttr(lightColorTex + '.outColor',shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovInput')
            if cmds.getAttr(shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovName') == 'Dark_Color':
                cmds.connectAttr(darkColorTex + '.outColor',shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovInput')
            if cmds.getAttr(shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovName') == 'Line_Mask' and cmds.checkBox('Line_Checkbox',q=True,v=True):
                cmds.connectAttr(lineColorRamp + '.outColor',shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovInput')
            if cmds.getAttr(shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovName') == 'Shadow_Mask':
                cmds.connectAttr(shadowLayeredTex + '.outColor',shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovInput')

def genPresetAOVs():
    aovList = ['Light_Color','Dark_Color','Line_Mask','Shadow_Mask','Component_ID1','Component_ID2']
    createAOVs(aovList)

def genMaterialNetwork():
    filename = os.path.basename(cmds.file(q=True,loc=True))
    charname = filename.split('_')[1]

    SGList = cmds.ls(sl=True,type='shadingEngine')

    for sg in SGList:
        lightColorFile = createFile(charname + '_' + sg + '_LightColor_Preview_File','file')
        darkColorFile = createFile(charname + '_' + sg + '_DarkColor_Preview_File','file')
        materialNetwork(lightColorFile,darkColorFile,charname,sg,'View')
        materialNetwork(lightColorFile,darkColorFile,charname,sg,'Render')
    
def getAllFile():
    tempFileList = list()
    for file in cmds.ls(type='file'):
        if len(cmds.getAttr(file+'.fileTextureName')) == 0:
            tempFileList.append(file)
    return tempFileList

def fileUI():
    if cmds.window('Filepath_UI',ex=True):
        cmds.deleteUI('Filepath_UI')
    cmds.window('Filepath_UI',w=500,h=600,t='SetMaps_UI')
    mainLayout = cmds.scrollLayout()
    tempFileList = list()
    for file in getAllFile():
        tempFileList.append(uiGroup(file,mainLayout))
    cmds.button(l='Set!',w=100,h=50,c=lambda args:setAllFilepath(tempFileList))
    cmds.showWindow('Filepath_UI')

def uiGroup(file,parentLayout):
    cmds.columnLayout(p=parentLayout)
    cmds.text(l=file)
    cmds.rowLayout(nc=2)
    textField = cmds.textField(w=400)
    cmds.button(l='Map',w=40,c=lambda args:cmds.textField(textField,e=True,tx=cmds.fileDialog2(fileMode=1)[0]))
    cmds.setParent(u=True)
    return (file,textField)

def setAllFilepath(fieldList):
    if len(fieldList) == 0:
        return
    for turple in fieldList:
        cmds.setAttr(turple[0]+'.fileTextureName',cmds.textField(turple[1],q=True,tx=True),type='string')
    
def globalRGBMaskUtility():
    colorMaskName = {'Red':(1.0,0.0,0.0),'Green':(0.0,1.0,0.0),'Blue':(0.0,0.0,1.0),'Purple':(1.0,0.0,1.0),'Cyan':(0.0,1.0,1.0),'Orange':(1.0,1.0,0.0)}
    for color in colorMaskName.keys():
        if cmds.objExists('Global_Mask_'+ color):
            continue
        utility = cmds.shadingNode('aiUtility',asShader=True,n='Global_Mask_'+color)
        cmds.setAttr(utility+'.shadeMode',2)
        cmds.setAttr(utility+'.color',colorMaskName.get(color)[0],colorMaskName.get(color)[1],colorMaskName.get(color)[2])

def splitSG():
    mesh = cmds.ls(sl=True,dag=True,ni=True,type='mesh')
    
    SGList = list(set(cmds.listConnections(mesh,type='shadingEngine')))
    attrList = ['surfaceShader','aiSurfaceShader','volumeShader','displacementShader','aiVolumeShader','aiCustomAOVs']
    
    if len(SGList) != 1:
        cmds.warning('Can only split 1 ShadingEngine on the time, or your mesh have face selection materials')
        return 

    newSet = cmds.sets(n=SGList[0]+'_Split',em=True,nss=True,r=True)
    cmds.sets(mesh,fe=newSet)
    for attr in attrList:
        #print attr
        srcConnections = cmds.connectionInfo(SGList[0]+'.'+attr,sfd=True)
        if attr == 'aiCustomAOVs':
            for i in cmds.getAttr(SGList[0]+'.'+attr,mi=True):
                for j in cmds.getAttr(newSet+'.'+attr,mi=True):
                    if cmds.getAttr(newSet+'.'+attr+'['+str(j)+'].aovName') == cmds.getAttr(SGList[0]+'.'+attr+'['+str(i)+'].aovName'):
                        srcAOVs = cmds.connectionInfo(SGList[0]+'.'+attr + '['+str(i)+'].aovInput',sfd=True)
                        if len(srcAOVs):
                            cmds.connectAttr(srcAOVs,newSet+'.'+attr+'['+str(j)+'].aovInput')
            continue
        #print srcConnections
        if len(srcConnections):
            cmds.connectAttr(srcConnections,newSet+'.'+attr)
    return newSet

#Generate a bbox index dictionary, stare a lot of memory
meshBoxDict = dict()

def analyseAllMeshBoxes():
    global meshBoxDict
    for mesh in cmds.ls(ap=True,dag=True,ni=True,type='transform'):
        absBox = list()
        bbox = cmds.xform(mesh,q=True,bb=True)
        absBox.append(abs(bbox[0]))
        absBox.append(abs(bbox[1]))
        absBox.append(abs(bbox[2]))
        absBox.append(abs(bbox[3]))
        absBox.append(abs(bbox[4]))
        absBox.append(abs(bbox[5]))
        absBox.sort()
        meshBoxDict[mesh] = absBox

def compareMeshs():
    global meshBoxDict
    if len(meshBoxDict) == 0:
        analyseAllMeshBoxes()
        
    meshList = cmds.ls(sl=True,ap=True,dag=True,ni=True,type='transform')
    matchSizeMesh = list()
    tol = 0.0001
    for referenceMesh in meshList:
        #print meshBoxDict.get(referenceMesh)
        matchSizeMesh.append(referenceMesh)
        for allMesh in meshBoxDict.keys():
            if abs(meshBoxDict.get(referenceMesh)[0] - meshBoxDict.get(allMesh)[0]) > tol:
                continue
            if abs(meshBoxDict.get(referenceMesh)[1] - meshBoxDict.get(allMesh)[1]) > tol:
                continue
            if abs(meshBoxDict.get(referenceMesh)[2] - meshBoxDict.get(allMesh)[2]) > tol:
                continue
            if abs(meshBoxDict.get(referenceMesh)[3] - meshBoxDict.get(allMesh)[3]) > tol:
                continue
            if abs(meshBoxDict.get(referenceMesh)[4] - meshBoxDict.get(allMesh)[4]) > tol:
                continue
            if abs(meshBoxDict.get(referenceMesh)[5] - meshBoxDict.get(allMesh)[5]) > tol:
                continue    
            matchSizeMesh.append(allMesh)
    cmds.select(matchSizeMesh,r=True)


def Material_Network_initializeUI():
    if cmds.window('MaterialNetwork_UI',ex=True):
        cmds.deleteUI('MaterialNetwork_UI')
    cmds.window('MaterialNetwork_UI',w=350,t='Material_Network_UI')
    mainLayout = cmds.columnLayout()
    cmds.rowLayout(nc=8)
    cmds.button(l='Create AOVs',c=lambda args:genPresetAOVs())
    cmds.button(l='Create Mats',c=lambda args:genMaterialNetwork())
    cmds.checkBox('Line_Checkbox',l='Line',v=1)
    cmds.checkBox('Spec_Checkbox',l='Spec',v=0)
    cmds.button(l='Set Maps',c=lambda args:fileUI())
    cmds.button(l='Mask_Shader',c=lambda args:globalRGBMaskUtility())
    cmds.button(l='sRGB',bgc=[0.5,0.0,0.0],c=lambda args:setFileColorSpace('sRGB'))
    cmds.button(l='Raw',bgc=[0.25,0.0,0.0],c=lambda args:setFileColorSpace('Raw'))
    cmds.setParent(u=True)
    cmds.rowLayout(nc=8)
    cmds.button(l='Select Similar',c=lambda args:compareMeshs())
    cmds.button(l='SplitSG',w=40,c=lambda args:splitSG())
    cmds.setParent(u=True)
    cmds.showWindow('MaterialNetwork_UI')

def setFileColorSpace(colorspace):
    for file in cmds.ls(type='file'):
        cmds.setAttr(file+'.colorSpace',colorspace,type='string')


Material_Network_initializeUI()