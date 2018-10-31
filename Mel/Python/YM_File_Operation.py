 #-*- coding: utf-8 -*-
import os
import time
import re
import shutil

def move_History_File(filepath):
    localTime = time.localtime()
    
    formatTime = '_' + str(localTime.tm_year) + '_' \
                     + str(localTime.tm_mon) + '_' \
                     + str(localTime.tm_mday) + '_' \
                     + str(localTime.tm_hour) + '_' \
                     + str(localTime.tm_min)

    #fileMatch = re.search('([^<>/\\\|:""\*\?]+)\.\w+$',filepath)
    
    #filename = fileMatch.string[fileMatch.start():fileMatch.end()]
    #dirpath = fileMatch.string[0:fileMatch.start()-1]

    filename = os.path.basename(filepath.split('.')[0])
    
    nameList = filepath.split('.')
    fileExt = ''
    if len(nameList)>1:
        for i in range(1,len(nameList)):
            fileExt += '.'
            fileExt += nameList[i]
    
    dirpath = os.path.dirname(filepath)

    filenewname = filename + formatTime + fileExt
    
    if os.path.exists(dirpath+'/history_version') is False:
        os.mkdir(dirpath+'/history_version')

    if os.path.exists(filepath):
        os.rename(filepath,dirpath+'/'+filenewname)
        shutil.move(dirpath+'/'+filenewname,dirpath+'/history_version/'+filenewname)
    



#move_History_File('//S3/文档库/综合部/JXB2_EP001_APPROVE_MOV_COLLECTION.dpl'.decode('utf-8'))
move_History_File('E:/新建文件夹/tpa.txt'.decode('utf-8'))

