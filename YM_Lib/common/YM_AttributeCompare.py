import maya.cmds as cmds


def compareObjects(objects):
    if(len(objects)!=2 or cmds.nodeType(objects[0])!=cmds.nodeType(objects[1])):
        cmds.error("Must select two node & ensure they are same type")
        return
    
    a_Attrs = cmds.listAttr(objects[0],v=True,w=True,hd=True,settable=True)
    b_Attrs = cmds.listAttr(objects[1],v=True,w=True,hd=True,settable=True)

    temp_Attrs = [] 
    if(len(a_Attrs)-len(b_Attrs)>=0):
        temp_Attrs = [attr for attr in a_Attrs]
    else:
        temp_Attrs = [attr for attr in b_Attrs]
    
    notEqualAttributes = []
    notExistAttributes = []
    
    for attribute in temp_Attrs:
        if(cmds.attributeQuery(attribute,ex=True,n=objects[0]) == cmds.attributeQuery(attribute,ex=True,n=objects[1])):
            try:
                if cmds.getAttr(objects[0]+'.'+attribute,asString=True) != cmds.getAttr(objects[1]+'.'+attribute,asString=True):
                    notEqualAttributes.append(attribute)
                else:
                    continue    
            except:
                continue  
        else:
            notExistAttributes.append(attribute)
            continue
         
    
    return notEqualAttributes+notExistAttributes
    
def resultDialogue(attributesList):
    
    if cmds.window('attributeCompareWindow',ex=True):
        cmds.deleteUI('attributeCompareWindow')

    cmds.window('attributeCompareWindow',t='Compare Results',w=500,h=500)
    cmds.scrollLayout()
    mainLayout = cmds.rowLayout(nc=3)
    col1 = cmds.columnLayout(w=150,p=mainLayout)
    cmds.textField(w=150,tx='Object/Attribute',p=col1)
    col2 = cmds.columnLayout(w=150,p=mainLayout)
    cmds.textField(w=150,tx=cmds.ls(sl=True)[0],p=col2)
    col3 = cmds.columnLayout(w=150,p=mainLayout)
    cmds.textField(w=150,tx=cmds.ls(sl=True)[1],p=col3)
    
    for attribute in attributesList:
        aError_Code = 'Null'
        bError_Code = 'Null'

        if(cmds.attributeQuery(attribute,ex=True,n=cmds.ls(sl=True)[0])==False):
            aError_Code = 'Attribute Not Exist'

        if(cmds.attributeQuery(attribute,ex=True,n=cmds.ls(sl=True)[1])==False):
            bError_Code = 'Attribute Not Exist'
 
        try:
            cmds.textField(w=150,tx=str(cmds.getAttr(cmds.ls(sl=True)[0]+'.'+attribute,asString=True)),bgc=[0.767,0,0],p=col2)
        except:
            cmds.textField(w=150,tx=aError_Code,bgc=[0.3,0.3,0.3],p=col2)
        try:
            cmds.textField(w=150,tx=str(cmds.getAttr(cmds.ls(sl=True)[1]+'.'+attribute,asString=True)),bgc=[0,0.767,0],p=col3)
        except:
            cmds.textField(w=150,tx=bError_Code,bgc=[0.27,0.27,0.27],p=col3)
            
        cmds.textField(w=150,tx=attribute,bgc=[0.3,0.3,0.3],p=col1)
        

    cmds.showWindow('attributeCompareWindow')


if __name__ == '__main__':
    resultDialogue(compareObjects(cmds.ls(sl=True)))





