from pymel import core


def overrideObjectColor(object,objectColor):
    core.setAttr(object+'.overrideEnabled',1)
    core.setAttr(object+'.overrideRGBColors',1)
    core.setAttr(object+'.overrideColorRGB',objectColor)
    
    
overrideObjectColor('pCube1',[1,1,1])