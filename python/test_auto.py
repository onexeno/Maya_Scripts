import sys

import os
import re


allfile = list()

for i,j,k in os.walk("\\\\S2\\Projects\\JXB_Season2\\ep002"):
    count = 0
    if len(j) and count<3:
        if re.search('[r|R]ig',j[0]):
            count+=1
            print i+'\\'+j[0]
        continue

print "It's over"
