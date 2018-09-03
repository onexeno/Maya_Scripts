
import alembic

import maya.cmds as cd

if cd.window('Telsa',ex=True):
    cd.deleteUI('Telsa')
    
cd.window('Telsa',w=500,h=300)
cd.columnLayout('TelsaMainLayout')
cd.rowLayout(nc=3)
cd.textFieldGrp('ABC_FILE_TEXTFIELD',l='test')
cd.button('ABCFILEBTN',l='Click',c=lambda x:cd.textFieldGrp('ABC_FILE_TEXTFIELD',e=True,tx=cd.fileDialog2(fm=1,cap="Alembic Nodes",ff="Alembic Node(*.abc)")[0]))
cd.button('ABCANALYSE',l='Analyse',c='updateVars()')
cd.setParent('..')
cd.showWindow('Telsa')

global abcPoint

def updateVars():
    global abcPoint
    abcPoint = alembic.Abc.IArchive(str(cd.textFieldGrp('ABC_FILE_TEXTFIELD',q=True,tx=True)))
    if len(abcPoint.getName())>0:
        if cd.textScrollList('AbcInfo',q=True,ex=True)==False:
            cd.textScrollList('AbcInfo',parent='TelsaMainLayout')
        cd.textScrollList('AbcInfo',e=True,ra=True,w=600) 
        infos = alembic.Abc.GetArchiveInfo(abcPoint)  #This object is a dictionary object
        for info,keys in infos.iteritems():
            cd.textScrollList('AbcInfo',e=True,a=str(info) + " : "+str(keys))
        
abcPoint.getName()
abcPoint.getCoreType()
abcPoint.getNumTimeSamplings()

a = alembic.Abc.GetArchiveInfo(abcPoint)
import shiboken2




def polyCube(name,width,height,depth):
    name = 'n | name'
    width = 'w | width'
    height = 'h | height'
    depth = 'd | depth'
    pass

polyCube(height=100)

