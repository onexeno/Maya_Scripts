'''
a = dict()

b = ['x[1]','x[3]','x[6]','y[2]','y[1]','z[2]']
c = [2,4,1,0,5,9]
for k in range(0,len(b)):
    a[c[k]] = b[k]

sorted(a)   
print a.values()'''



b = maya.cmds.ls(sl=True,fl=True)

c = [maya.cmds.xform(bComp,q=True,ws=True,t=True)[0] for bComp in b]


for i in range(0,len(c)):
    if c.count(c[i])>1:
        #print c[i],'\t',c[i]+c.count(c[i])*0.001,'\n'
        c[i] = c[i]+c.count(c[i])*0.0001
d = c
c = sorted(c,reverse=True)
e = list()

for i in range(0,len(c)):
    #print d.index(c[i]) 
    e.append(b[d.index(c[i])])
    
e