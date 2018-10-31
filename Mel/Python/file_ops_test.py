#-*- coding: utf-8 -*-
import sys
import os
import re
#print os.path.getsize('//S2/Projects/JXB_S2/小白第二季设定/场设/色稿/0725'.decode('utf-8'))
path = '//S2/Projects/JXB_Season2/ep001/Shot_work/Animation'.decode('utf-8')

def getApproveAnimationFiles():
    fileList = []
    for i in os.listdir(path):
        if os.path.isdir(path+'/'+i+'/approve') is True:
            fileList = os.listdir(path+'/'+i+'/approve')
            for file in fileList:
                if re.search('(\.m[a|b]$){1}',file) is not None:
                    #print (path+'/'+i+'/approve'+'/'+file)
                    fileList.append(path+'/'+i+'/approve'+'/'+file)
    return fileList