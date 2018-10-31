#-*- coding: utf-8 -*-
import sys
import maya.standalone
from YM_ABC_Export_Cmd import *
'''
sys.path.append('C:/ProgramData/Autodesk/ApplicationPlugins/MayaBonusTools-2015-2018/Contents/python-2016')
sys.path.append('C:/ProgramData/Autodesk/ApplicationPlugins/MayaBonusTools-2015-2018/Contents/python')
sys.path.append('C:/Program Files/Autodesk/Maya2016/bin')
sys.path.append('C:/ProgramData/Redshift/Plugins/Maya/Common/scripts')
sys.path.append('C:/Program Files/Autodesk/Maya2016/plug-ins/bifrost/scripts/presets')
sys.path.append('C:/Program Files/Autodesk/Maya2016/plug-ins/bifrost/scripts')
sys.path.append('C:/Program Files/Autodesk/Maya2016/FumeFX/scripts')
sys.path.append('C:/ProgramData/Autodesk/ApplicationPlugins/MayaBonusTools-2015-2018/Contents/scripts')
sys.path.append('C:/Program Files/PSOFT/Pencil+ 4 for Maya (OpenBeta)/modules/PSOFT Pencil+ 4 for Maya/scripts')
sys.path.append('C:/Program Files/Autodesk/Maya2016/phoenixfd/scripts')
sys.path.append('C:/Program Files/Autodesk/Maya2016/vray/scripts')
sys.path.append('C:/Program Files/Autodesk/Maya2016/plug-ins/fbx/scripts')
sys.path.append('C:/Users/Administrator/Documents/maya/Plugins/HardMeshTools/2016/scripts')
sys.path.append('C:/Program Files/Side Effects Software/Houdini 17.0.352/engine/maya/maya2016/scripts')
sys.path.append('C:/Users/Administrator/Documents/maya/Plugins/2016/scripts')
sys.path.append('C:/Program Files/Autodesk/mentalrayForMaya2016/scripts/AETemplates')
sys.path.append('C:/Program Files/Autodesk/mentalrayForMaya2016/scripts/mentalray')
sys.path.append('C:/Program Files/Autodesk/mentalrayForMaya2016/scripts/NETemplates')
sys.path.append('C:/Program Files/Autodesk/mentalrayForMaya2016/scripts/unsupported')
sys.path.append('C:/Program Files/Autodesk/mentalrayForMaya2016/scripts')
sys.path.append('C:/solidangle/mtoadeploy/2016/scripts')
sys.path.append('C:/Program Files/Autodesk/Maya2016/plug-ins/substance/scripts')
sys.path.append('C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/cafm')
sys.path.append('C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm')
sys.path.append('C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm/ui')
sys.path.append('C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm/xmaya')
sys.path.append('C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm/ui/brushes')
sys.path.append('C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm/ui/dialogs')
sys.path.append('C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm/ui/fxmodules')
sys.path.append('C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm/ui/tabs')
sys.path.append('C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm/ui/util')
sys.path.append('C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm/ui/widgets')
sys.path.append('C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts')
sys.path.append('C:/Program Files/Autodesk/Maya2016/bin/python27.zip')
sys.path.append('C:/Program Files/Autodesk/Maya2016/Python/DLLs')
sys.path.append('C:/Program Files/Autodesk/Maya2016/Python/lib')
sys.path.append('C:/Program Files/Autodesk/Maya2016/Python/lib/plat-win')
sys.path.append('C:/Program Files/Autodesk/Maya2016/Python/lib/lib-tk')
sys.path.append('C:/Program Files/Autodesk/Maya2016/bin')
sys.path.append('C:/Users/Administrator/AppData/Roaming/Python/Python27/site-packages')
sys.path.append('C:/Program Files/Autodesk/Maya2016/Python')
sys.path.append('C:/Program Files/Autodesk/Maya2016/Python/lib/site-packages')
sys.path.append('C:/Program Files/Autodesk/Maya2016/bin/python27.zip/lib-tk')
sys.path.append('C:/Users/Administrator/Documents/maya/2016/prefs/scripts')
sys.path.append('C:/Users/Administrator/Documents/maya/2016/scripts')
sys.path.append('C:/Users/Administrator/Documents/maya/scripts')
sys.path.append('C:/Users/Administrator/Documents/Phoenix FD/samples maya/scripts')
sys.path.append('C:/Program Files/Autodesk/Maya2016/phoenixfd/scripts')
sys.path.append('C:/solidangle/alShaders/ae')
'''


def external_Ops_exportABC(filepath):
    libPath = '//S3/软件库/P_插件目录/YunMan_Toolsets/Common/Python'
    arnoldPath = 'C:/solidangle/mtoadeploy/2016/scripts'
    

    try:
        maya.standalone.initialize('python')
        import pymel.core
        import maya.cmds as cmds
        if sys.path.count(libPath) == 0:
            sys.path.append(libPath)
        if sys.path.count(arnoldPath) == 0:
            sys.path.append('C:/solidangle/mtoadeploy/2016/scripts')
    except:
        print 'Cannot initialize the python standalone'
        return    

    try:
        cmds.file(filepath,open=True,f=True)
    except:
        print 'Cannot Open the file: ' + filepath
        maya.standalone.uninitialize()
        exit()
        return
    
    if cmds.pluginInfo('AbcExport',q=True,loaded=True) is False:
        cmds.loadPlugin('AbcExport')
    if cmds.pluginInfo('mtoa',q=True,loaded=True) is False:
        cmds.loadPlugin('mtoa')
        
    try:
        exportCamera()
    except:
        pass
    try:
        exportAbcCmd()
    except:
        pass

    maya.standalone.uninitialize()
    cmds.quit()
    sys.exit()

filepath = '//S2/Projects/JXB_Season2/ep003/Shot_work/Animation/cut212/approve/JXB02_ep003_cut212.mb'
#filepath = '//S2/Projects/JXB_Season2/ep003/Asset_work/chars/JXB2_ep003_LX_XZ/Rig/approve/JXB2_ep003_LX_XZ_rig_ok.mb'

external_Ops_exportABC(filepath)