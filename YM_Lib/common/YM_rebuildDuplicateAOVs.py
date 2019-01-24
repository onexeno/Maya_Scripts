#-*- coding: utf-8 -*-
import mtoa.aovs as aov

myAOV = aov.AOVInterface()

duplicateAOVs = list()

for aov in myAOV.getAOVs(group=True):
    if len(aov[1])>1:
        #for nodes in myAOV.getAOVNodes(aov[0]):
            #print nodes
        print aov[0]
        duplicateAOVs.append(aov[0])

if len(duplicateAOVs) == 0:
    duplicateAOVs = ['']

else:
    myAOV.removeAOVs(duplicateAOVs)
    for newaov in duplicateAOVs:
        myAOV.addAOV(newaov)
    
