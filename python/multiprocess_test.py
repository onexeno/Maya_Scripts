#-*- coding: utf-8 -*-
#file status
import os
import sys
import time
import multiprocessing

def writeFile(filepath):
    file = open(filepath,'w')
    for i in range(100):
        file.write('//s2/jxl/animation/cut'+str(i)+'/approve/abc_caches' + ' ' + 'wait\n')
    file.close()

filepath = 'F:/test.txt'
#print ('dad da'.split(' '))
#writeFile(filepath)

def findMark(filepath):
    file = open(filepath,'r')
    temp = list()
    for line in file.readlines():
        tempList = line.split(' ')
        if tempList[1].strip('\n') == 'wait':
            #time.sleep(0.1)
            print tempList[0]
            temp.append(tempList[0] + ' ' + 'complete\n')
        else:
            temp.append(line)
    
    file.close()
    file = open(filepath,'w')
    file.writelines(temp)
    file.close()


p = multiprocessing.Pool(5)
print(p.map(findMark,['filepath']))

#findMark(filepath)
