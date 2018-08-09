import os
import re
from pymel import core

fileNode = core.ls(type='file')
aiImageNode = core.ls(type='aiImage')
#change the extension
newExtension = '.tif'

for file in fileNode:
    filepath = core.getAttr(file+'.fileTextureName')
    newPath = filepath[0:re.search("[.]\D+$",filepath).start()]+newExtension
    if os.path.exists(newPath):
        core.setAttr(file+'.fileTextureName',newPath,type='string')
    else:
        continue

for file in aiImageNode:
    filepath = core.getAttr(file+'.filename')
    newPath = filepath[0:re.search("[.]\D+$",filepath).start()]+newExtension
    if os.path.exists(newPath):
        core.setAttr(file+'.filename',newPath,type='string')
    else:
        continue


