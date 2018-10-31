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
    
    if(viewOrRender == 'Render'):
        lightColorTex = createFile(charname + '_' + shadingEngine + '_LightColor_File','file')
        darkColorTex = createFile(charname + '_' + shadingEngine + '_DarkColor_File','file')
        lineColorTex = createFile(charname + '_' + shadingEngine + '_Line_File','file')
        drawShadowTex = createFile(charname + '_' + shadingEngine + '_ShadowMask_File','file')
        highlightTex = ''

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

        if re.search('([H|h]air|[T|t]ou[F|f]a|TF)',shadingEngine) is not None:
            #highlightTex = createFile('Hightlight_Mask','file')
            cmds.connectAttr(drawShadowTex+'.outColorG',shadowLayeredTex+'.inputs[2].alpha')
            cmds.setAttr(shadowLayeredTex+'.inputs[2].color',0.0,1.0,0.0)
        

        for i in cmds.getAttr(shadingEngine+'.aiCustomAOVs',mi=True):
            if cmds.getAttr(shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovName') == 'Light_Color':
                cmds.connectAttr(lightColorTex + '.outColor',shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovInput')
            if cmds.getAttr(shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovName') == 'Dark_Color':
                cmds.connectAttr(darkColorTex + '.outColor',shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovInput')
            if cmds.getAttr(shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovName') == 'Line_Mask':
                cmds.connectAttr(lineColorRamp + '.outColor',shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovInput')
            if cmds.getAttr(shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovName') == 'Shadow_Mask':
                cmds.connectAttr(shadowLayeredTex + '.outColor',shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovInput')

'''
def aovNetwork(charname,shadingEngine):
    lightColorTex = createFile(charname + '_' + shadingEngine + '_LightColor_File','file')
    darkColorTex = createFile(charname + '_' + shadingEngine + '_DarkColor_File','file')
    lineColorTex = createFile(charname + '_' + shadingEngine + '_Line_File','file')
    drawShadowTex = createFile(charname + '_' + shadingEngine + '_ShadowMask_File','file')
    highlightTex = ''

    lineColorRamp = cmds.shadingNode('ramp',at=True,ss=True,n=charname + '_' + shadingEngine + '_Line_Ramp')
    cmds.setAttr(lineColorRamp+'.colorEntryList[0].color',1.0,1.0,1.0)
    cmds.setAttr(lineColorRamp+'.colorEntryList[0].position',0.0)
    cmds.setAttr(lineColorRamp+'.colorEntryList[1].color',0.0,0.0,0.0)
    cmds.setAttr(lineColorRamp+'.colorEntryList[1].position',1.0)
    cmds.connectAttr(lineColorTex+'.outColorR',lineColorRamp+'.vCoord')

    shadowLayeredTex = cmds.shadingNode('layeredTexture',au=True,ss=True,n=charname + '_' + shadingEngine + '_ShadowLayeredTexture')
    realShadowRamp = cmds.shadingNode('ramp',at=True,ss=True,n=charname + '_' + shadingEngine + '_RealShadow_Ramp')
    cmds.setAttr(realShadowRamp + '.colorEntryList[0].color',1.0,1.0,1.0)
    cmds.setAttr(realShadowRamp + '.colorEntryList[0].position',0.0)
    cmds.setAttr(realShadowRamp + '.colorEntryList[1].color',0.0,0.0,0.0)
    cmds.setAttr(realShadowRamp + '.colorEntryList[1].position',0.2)
    cmds.setAttr(realShadowRamp + '.interpolation',0)

    if cmds.objExists('Global_Render_Sampler') is False:
        cmds.shadingNode('surfaceLuminance',au=True,ss=True,n='Global_Render_Sampler')
    cmds.connectAttr('Global_Render_Sampler.outValue',realShadowRamp+'.vCoord')

    cmds.connectAttr(realShadowRamp+'.outAlpha',shadowLayeredTex+'.inputs[0].alpha')
    cmds.setAttr(shadowLayeredTex+'.inputs[0].color',1.0,0.0,0.0)
    cmds.setAttr(shadowLayeredTex+'.inputs[0].blendMode',4)
    cmds.connectAttr(drawShadowTex+'.outColorB',shadowLayeredTex+'.inputs[1].alpha')
    cmds.setAttr(shadowLayeredTex+'.inputs[1].color',0.0,0.0,1.0)
    cmds.setAttr(shadowLayeredTex+'.inputs[1].blendMode',4)

    if re.search('([H|h]air|[T|t]ou[F|f]a|TF)',shadingEngine) is not None:
        #highlightTex = createFile('Hightlight_Mask','file')
        cmds.connectAttr(drawShadowTex+'.outColorG',shadowLayeredTex+'.inputs[2].alpha')
        cmds.setAttr(shadowLayeredTex+'.inputs[2].color',0.0,1.0,0.0)
    

    for i in cmds.getAttr(shadingEngine+'.aiCustomAOVs',mi=True):
        if cmds.getAttr(shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovName') == 'Light_Color':
            cmds.connectAttr(lightColorTex + '.outColor',shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovInput')
        if cmds.getAttr(shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovName') == 'Dark_Color':
            cmds.connectAttr(darkColorTex + '.outColor',shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovInput')
        if cmds.getAttr(shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovName') == 'Line_Mask':
            cmds.connectAttr(lineColorRamp + '.outColor',shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovInput')
        if cmds.getAttr(shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovName') == 'Shadow_Mask':
            cmds.connectAttr(shadowLayeredTex + '.outColor',shadingEngine + '.aiCustomAOVs[' + str(i) + '].aovInput')
'''

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
    cmds.button(l='Set!',c=lambda args:setAllFilepath(tempFileList))
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
    
def Material_Network_initializeUI():
    if cmds.window('MaterialNetwork_UI',ex=True):
        cmds.deleteUI('MaterialNetwork_UI')
    cmds.window('MaterialNetwork_UI',w=450,t='Material_Network_UI')
    mainLayout = cmds.columnLayout()
    cmds.rowLayout(nc=3)
    cmds.button(l='Create AOVs',c=lambda args:genPresetAOVs())
    cmds.button(l='Create Mats',c=lambda args:genMaterialNetwork())
    cmds.button(l='Set Maps',c=lambda args:fileUI())
    cmds.setParent(u=True)
    cmds.showWindow('MaterialNetwork_UI')

Material_Network_initializeUI()