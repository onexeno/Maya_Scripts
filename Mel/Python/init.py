import sys
import os

YM_Scripts_Path = "//s3/软件库/P_插件目录/YunMan_Toolsets/Common/Python"

if (sys.path.count(YM_Scripts_Path) == False) and (os.path.exists("//s3/软件库/P_插件目录/YunMan_Toolsets/Common/Python")):
    sys.path.append(YM_Scripts_Path)

