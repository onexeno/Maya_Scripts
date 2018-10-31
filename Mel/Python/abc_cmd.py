#-*- coding: utf-8 -*-
import sys
#libPath = '//S3/软件库/P_插件目录/YunMan_Toolsets/Common/Python'
libPath = 'F:/Works/Codes/Git/Maya_Scripts/Mel/Python'

if sys.path.count(libPath) == 0:
    sys.path.append(libPath)

from YM_ABC_Export_Cmd import *

try:
    exportCamera()
except:
    pass
try:
    exportAbcCmd()
except:
    cmds.warning('Check your scene!!!')
