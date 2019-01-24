#-*- coding: utf-8 -*-

import maya.cmds as cmds
import json

class exportAlembicMethod():
    __windowName = 'Reference_Alembic_Output_Group_Presets_Setting_Window'
    __fileVar = 'YM_Config_SettingFilePath'
    __configDict = dict()

    def __init__(self):
        pass
    
    def initialUI(self):
        if cmds.window(self.__windowName,ex=True):
            cmds.deleteUI(self.__windowName)
            
        cmds.window(self.__windowName,t='Config_Window',w=600)
        cmds.columnLayout()
        cmds.rowLayout(nc=3)
        cmds.text(l='Config File Path: ')
        cmds.textField('SettingFilePathField',w=460)
        cmds.button(l='File',c='config_path()',w=50)
        cmds.setParent(u=True)
        cmds.rowLayout(nc=2)
        cmds.frameLayout(l='Reference List')
        cmds.textScrollList('YM_AlembicExport_RederenceList',w=300,h=300)
        cmds.setParent(u=True)
        cmds.frameLayout('YM_AlembicExport_ExportGroupList',l='Export_Group List')
        cmds.textScrollList('',w=300,h=300)
        cmds.setParent(u=True)
        cmds.showWindow(self.__windowName)

        if cmds.optionVar(ex=self.__fileVar):
            cmds.textField('SettingFilePathField',e=True,tx=cmds.optionVar(q=self.__fileVar))


    #check json file and set default path
    def config_path():
        filepath = cmds.fileDialog2(fm=4,ff='*.json')
        if filepath is None:
            return
        cmds.textField('SettingFilePathField',e=True,tx=filepath[0])
        cmds.optionVar(sv=[__fileVar,filepath[0]])

    # Read the config file as json object and dump it to dict object
    def config_read():
        filepath = cmds.textField('SettingFilePathField',q=True,tx=True)
        if filepath is None:
            return
        with open(filepath,'r') as configFile:
            configDict = configFile.read()
        configFile.close()
        return json.loads(configDict)

    # Write the config file from dict to json object
    def config_write(configDict):
        filepath = cmds.textField('SettingFilePathField',q=True,tx=True)
        if filepath is None:
            return

        configFileContent = json.dumps(configDict)

        with open(filepath,'w') as configFile:
            configFile.write(configFileContent)    
        configFile.close()

    def refreshReferenceList():
        self.__configDict = self.config_read()
        
        cmds.textScrollList('YM_AlembicExport_RederenceList',e=True,ra=True)
        for key in self.__configDict.keys():
            if cmds.objExists(key) is False:
                continue
            cmds.textScrollList('YM_AlembicExport_RederenceList',a=key)
        
    def refreshExportGroupList():
        cmds.textScrollList('YM_AlembicExport_RederenceList',q=True,si=True)


a = exportAlembicMethod()
a.initialUI()