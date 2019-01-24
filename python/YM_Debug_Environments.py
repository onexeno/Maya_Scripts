#-*- coding: utf-8 -*-
import os,sys
import maya.cmds as cmds

global debugEnvList

debugEnvList = ['MAYA_MODULE_PATH',
                'MAYA_PLUG_IN_PATH',
                'MAYA_SCRIPT_PATH',
                'XBMLANGPATH',
                'MAYA_APP_DIR',
                'MAYA_CMD_FILE_OUTPUT',
                'MAYA_CONTENT_PATH',
                'MAYA_CUSTOM_TEMPLATE_WRITE_PATH',
                'MAYA_FILE_ICON_PATH',
                'MAYA_MOVIE_DIR',
                'MAYA_LOCATION',
                'MAYA_PRESET_PATH',
                'MAYA_PROJECT',
                'MAYA_PROJECTS_DIR',
                'MAYA_SHELF_PATH',
                'PYTHONPATH',
                'TEMP']


def refreshResultList():
    envDict = os.environ

    for item in cmds.textScrollList('DEBUG_TOOLS_ENVS_LIST',q=True,si=True):
        if envDict.has_key('MAYA_MODULE_PATH') is False:
            return
        cmds.textScrollList('DEBUG_TOOLS_PATHS_LIST',e=True,ra=True)
        if envDict.get(item) is None:
            return
        cmds.textScrollList('DEBUG_TOOLS_PATHS_LIST',e=True,a=envDict.get(item).split(';'))

def resultListAction():
    if cmds.textScrollList('DEBUG_TOOLS_PATHS_LIST',q=True,si=True) is None:
        return
    #os.startfile(cmds.textScrollList('DEBUG_TOOLS_PATHS_LIST',q=True,si=True)[0])
   
    for path in cmds.textScrollList('DEBUG_TOOLS_PATHS_LIST',q=True,si=True):
        if len(path) == 0 or os.path.exists(path) is False:
            return
        os.startfile(path)

def DEBUG_Window():
    global debugEnvList
    if cmds.window('DEBUG_TOOLS_ENV',ex=True):
        cmds.deleteUI('DEBUG_TOOLS_ENV')
    if cmds.windowPref('DEBUG_TOOLS_ENV',ex=True):
        cmds.windowPref('DEBUG_TOOLS_ENV',r=True)    
    cmds.window('DEBUG_TOOLS_ENV',t='Debug_Tools_Window',w=620,h=300)
    
    cmds.rowLayout(nc=2)
    cmds.columnLayout()
    cmds.textScrollList('DEBUG_TOOLS_ENVS_LIST',a=debugEnvList,w=220,h=300,sc='refreshResultList()')
    cmds.setParent(u=True)
    cmds.textScrollList('DEBUG_TOOLS_PATHS_LIST',w=400,h=300,dcc='resultListAction()')
    
    cmds.showWindow('DEBUG_TOOLS_ENV')

DEBUG_Window()
