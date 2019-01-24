#-*- coding: utf-8 -*-

import os
import re
import maya.cmds as cmds


import maya.standalone

nodeStr = 'testCubes'

def openMayaFile():
    maya.standalone.initialize(name='python')
    cmds.file(new=True,f=True,prompt=True)
    
    import importlib
    importlib.import_module('sys')
    print sys.argv[0]
    cmds.polyCube(n=nodeStr)
    print (cmds.ls())

    cmds.quit()

openMayaFile()
