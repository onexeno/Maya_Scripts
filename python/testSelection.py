#-*- coding: utf-8 -*-
import maya.cmds as cmds
import sys

if sys.path.count('\\\\S3\\软件库\\P_插件目录\\YunMan_Toolsets\\Common\\Python') == 0:
    sys.path.append('\\\\S3\\软件库\\P_插件目录\\YunMan_Toolsets\\Common\\Python')

from YM_Group_Analyzer import *



if cmds.window('selectFilter',ex=True):
    cmds.deleteUI('selectFilter')
    
cmds.window('selectFilter',t='Filter',w=150,h=50,sizeable=True)
cmds.columnLayout()
cmds.rowLayout(nc=4)
cmds.textField('nodeTypeFilterText',w=150)
cmds.button(l='Selection',c=lambda args:cmds.select(cmds.ls(sl=True,dag=True,ni=True,type=cmds.textField('nodeTypeFilterText',q=True,tx=True)),r=True))
cmds.button(l='All in Scene',c=lambda args:cmds.select(cmds.ls(dag=True,ni=True,type=cmds.textField('nodeTypeFilterText',q=True,tx=True)),r=True))
cmds.button(l='In Group',c=lambda args:cmds.select(groupAnalyzer(cmds.ls(dag=True,sl=True,ni=True),cmds.textField('nodeTypeFilterText',q=True,tx=True),'down'),r=True))
cmds.setParent(u=True)
#cmds.textScrollList('nodeTypeFilterList',w=400,h=400)

cmds.showWindow()



