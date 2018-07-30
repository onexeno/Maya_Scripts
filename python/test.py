import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds
import maya.standalone as standalone


def outside(name='pythonCMD'):
    standalone.initialize(name)

outside('pythonCMD')

cmds.file('G:/Temp/wdas_cloud_2/wdas_cloud/cloud)test.mb',o=True)
