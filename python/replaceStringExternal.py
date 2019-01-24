#-*- coding:utf-8 -*-
import sys
import maya.standalone
import re


def replaceString(pattern,string,toString):
    findString = re.search(pattern,string)
    if findString is None:
        return
    return toString + findString.string[findString.end()+1:len(findString.string)]

def loopForFiles():
    for file in cmds.ls(type='file'):
        
    #    cmds.setAttr(file+'.fileTextureName','J',type='string')
        try:
            print (file + '\t :')
            newString = replaceString('\/\/[s|S]2\/[p|P]rojects\/JXB_Season2',cmds.getAttr(file+'.fileTextureName'),'J:/')
            #print cmds.getAttr(file+'.fileTextureName') + "\t | to | \t" + replaceString('\/\/S2\/Projects',cmds.getAttr(file+'.fileTextureName'),'J:/')
            print newString
            if newString is None:
                continue
            cmds.setAttr(file+'.fileTextureName',newString,type='string')
        except:
            continue
        
        
def external_replaceString(filepath):
    
    try:
        maya.standalone.initialize('python')
    except:
        print 'Cannot initialize the python standalone'
        return 
    
    import pymel.core
    import maya.cmds as cmds

    print 1
    libPath = '//S3/软件库/P_插件目录/YunMan_Toolsets/Common/Python'.decode('utf-8')
    arnoldPath = 'C:/solidangle/mtoadeploy/2016/scripts'
    print 2
    if sys.path.count(libPath) == 0:
        sys.path.append(libPath)
    if sys.path.count(arnoldPath) == 0:
        sys.path.append(arnoldPath)
    print 3   
    try:
        cmds.file(filepath,open=True,f=True)
        print 4
    except:
        print 'Cannot Open the file: ' + filepath
        #maya.standalone.uninitialize()
        return
    
    if cmds.pluginInfo('mtoa',q=True,loaded=True) is False:
        cmds.loadPlugin('mtoa')
    
    try:
        loopForFiles()
    except:
        pass
