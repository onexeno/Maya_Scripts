#-*- coding: utf-8 -*-
import sys
import os
import time
import subprocess
import shlex
from YM_Camera_Ops import *
# Filename ShotNumber StartFrame EndFrame 
import maya.cmds as cmds
import maya.mel as mel

#check FramePerSecond
FPS = mel.eval("currentTimeUnitToFPS")
minFrame = cmds.playbackOptions(q=True,min=True)
maxFrame = cmds.playbackOptions(q=True,max=True)

filepath = cmds.file(q=True,loc=True)
fileDir = os.path.basename(filepath)

cameras = getRenderableCameras()

def listFiles():
    texList = cmds.ls(type='file')
    aiTexList = cmds.ls(type='aiImage')
    mrTexList = cmds.ls(type='mentalrayTexture')
    