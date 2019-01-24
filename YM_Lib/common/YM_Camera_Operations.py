#-*- coding: utf-8 -*-
import maya.cmds as cmds

def getRenderableCameras():
    cameraList = cmds.ls(ap=True,type='camera')
    renderableCameraList = {}
    for camera in cameraList:
        if cmds.getAttr(camera+'.renderable'):
            transforms = cmds.listRelatives(camera,f=True,parent=True,type='transform')
            renderableCameraList[camera] = transforms[0]
    return renderableCameraList

#获取所有的启动相机【即不能删除的相机，可能为多余的persp，top等等】
def getStartupCameras():
    cameraList = cmds.ls(type='camera')
    startupCameraList = {}
    for camera in cameraList:
        if cmds.camera(camera,q=True,sc=True):
            transforms = cmds.listRelatives(camera,f=True,parent=True,type='transform')
            startupCameraList[camera] = transforms[0]
    return startupCameraList


def getNoStartupCameras():
    cameraList = cmds.ls(type='camera')
    unstartupCameraList = {}
    for camera in cameraList:
        if cmds.camera(camera,q=True,sc=True) is False:
            transforms = cmds.listRelatives(camera,f=True,parent=True,type='transform')
            unstartupCameraList[camera] = transforms[0]
    return unstartupCameraList

