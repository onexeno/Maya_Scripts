import maya.cmds as cmds
import maya.mel as mel
import re
#Directly use the listAttr command flags

def YM_AttributeUI():
    attrFlags = ['array',
                'connectable',
                'caching',
                'channelBox',
                'changedSinceFileOpen',
                'extension',
                'fromPlugin',
                'hasData',
                'hasNullData',
                'inUse',
                'keyable',
                'locked',
                'leaf',
                'multi',
                'read',
                'ramp',
                'readOnly',
                'scalar',
                'scalarAndArray',
                'settable',
                'shortNames',
                'unlocked',
                'userDefined',
                'usedAsFilename',
                'visible',
                'write']

    global_YM_Attribute_Left_List = []
    global_YM_Attribute_Right_List = []

    if cmds.window('AttributeList',ex=True):
        cmds.deleteUI('AttributeList')

    checkerList = []    
        
    cmds.window('AttributeList',w=600,h=450,t='AttributeListWindow')
    cmds.rowLayout(nc=4)
    cmds.columnLayout('CheckerList')
    cmds.rowLayout(nc=2)
    cmds.textField()
    cmds.button(l='<<')
    cmds.setParent(u=True)
    cmds.setParent(u=True)

    cmds.columnLayout()
    cmds.textField('YM_AttributeFilter_Left',w=300)
    cmds.textScrollList('YM_AttributeList_Left',ams=True,w=300,h=450)
    cmds.setParent(u=True)

    cmds.columnLayout()
    cmds.button('YM_Attribute_Left_Button',l='>>')
    cmds.separator(h=10)
    cmds.button('YM_Attribute_Right_Button',l='<<')
    cmds.setParent(u=True)

    cmds.columnLayout()
    cmds.textField('YM_AttributeFilter_Right',w=300)
    cmds.textScrollList('YM_AttributeList_Right',ams=True,w=300,h=450)
    cmds.setParent(u=True)

    cmds.button('YM_Attribute_Left_Button',e=True,c=lambda x: updateList('YM_AttributeList_Right','YM_AttributeList_Left','YM_AttributeFilter_Left'))
    cmds.button('YM_Attribute_Right_Button',e=True,c=lambda x: updateList('YM_AttributeList_Left','YM_AttributeList_Right','YM_AttributeFilter_Right'))
    cmds.textField('YM_AttributeFilter_Left',e=True,tcc=lambda x:filterList('YM_AttributeFilter_Left','YM_AttributeList_Left'))
    cmds.textField('YM_AttributeFilter_Right',e=True,tcc=lambda x:filterList('YM_AttributeFilter_Right','YM_AttributeList_Right'))
    cmds.showWindow('AttributeList')

    for attrFlag in attrFlags:
        checkerList.append(cmds.checkBox(l=attrFlag,parent='CheckerList'))

    for checker in checkerList:
        cmds.checkBox(checker,e=True,cc=lambda x:checkListCheck(checkerList))
    
def checkListCheck(checkerList):
    checkLabel = []
    for checker in checkerList:
        if cmds.checkBox(checker,q=True,v=True):
            checkLabel.append(cmds.checkBox(checker,q=True,l=True))
            #print checkLabel
    tempString = ''            
    for label in checkLabel:
        tempString += ("-"+label+" ")
    #temp = cmds.textScrollList('YM_AttributeList_Left',q=True,ai=True)
    
    try:        
        attrList = mel.eval("listAttr " + tempString)
    except:
        attrList = []
    
    cmds.textScrollList('YM_AttributeList_Left',e=True,ra=True)
    
    resultListCheck = cmds.textScrollList('YM_AttributeList_Right',q=True,ai=True)
    if resultListCheck is None:
        resultListCheck = []

    if attrList is not None:
        for attr in attrList:
            if resultListCheck.count(attr)==0:
                cmds.textScrollList('YM_AttributeList_Left',e=True,a=attr)
  
    global global_YM_Attribute_Left_List
    global global_YM_Attribute_Right_List
    global_YM_Attribute_Left_List = cmds.textScrollList('YM_AttributeList_Left',q=True,ai=True)
    global_YM_Attribute_Right_List = cmds.textScrollList('YM_AttributeList_Right',q=True,ai=True)

    
def updateList(fromList,toList,checkFieldItem):
    global global_YM_Attribute_Left_List
    global global_YM_Attribute_Right_List
    rightItemList = cmds.textScrollList(fromList,q=True,ai=True)
    leftItemList = cmds.textScrollList(toList,q=True,si=True)
    cmds.textField('YM_AttributeFilter_Left',e=True,tx='')
    cmds.textField('YM_AttributeFilter_Right',e=True,tx='')

    if rightItemList is None:
        rightItemList = []
    if leftItemList is not None:
        for item in leftItemList:
            rightItemList.append(item)
            cmds.textScrollList(toList,e=True,ri=item)
        cmds.textScrollList(fromList,e=True,ra=True)
        for rightItem in rightItemList:
            cmds.textScrollList(fromList,e=True,a=rightItem)

    global_YM_Attribute_Left_List = cmds.textScrollList('YM_AttributeList_Left',q=True,ai=True)
    global_YM_Attribute_Right_List = cmds.textScrollList('YM_AttributeList_Right',q=True,ai=True)
    

    

def filterList(filterField,targetList):
    global global_YM_Attribute_Left_List
    global global_YM_Attribute_Right_List
    pattern = cmds.textField(filterField,q=True,tx=True)
    tempOldList = []
    if targetList == 'YM_AttributeList_Left':
        tempOldList = global_YM_Attribute_Left_List
    elif targetList == 'YM_AttributeList_Right':
        tempOldList = global_YM_Attribute_Right_List

    if tempOldList is not None:
        filterList = []
        if pattern is not None:
            for item in tempOldList:
                try:
                    reObject = re.search(pattern,item)
                except:
                    reObject = ''
                if reObject is not None:
                    filterList.append(reObject.string)
                
            if filterList is not None:
                cmds.textScrollList(targetList,e=True,ra=True)
                for item in filterList:
                    cmds.textScrollList(targetList,e=True,a=item)
        else:
            if  len(tempOldList)>0:
                for item in tempOldList:
                    cmds.textScrollList(targetList,e=True,a=item)
    else:
        pass        


def getFilteredAttributes():
    global global_YM_Attribute_Right_List
    if global_YM_Attribute_Right_List is not None:
        pass
    else:
        pass


def attributeInfoWindow(attribute,node):
     
    attrType = ''
    attrValue = ''
    attrInputConnection = ''
    attrInputConnection = []
    
    if cmds.attributeQuery(attribute,ex=True,n=node) is True:
        try:
            attrType = cmds.getAttr(node+'.'+attribute,type=True)
            attrValue = cmds.getAttr(node+'.'+attribute,asString=True)
            attrInputConnection = cmds.connectionInfo(node+'.'+attribute,sfd=True)    
            attrOutputConnection = cmds.connectionInfo(node+'.'+attribute,dfs=True)
        except:
            cmds.warning(attribute+'can not be accessed')

    if cmds.window('YM_AttributeInfoWIndow',ex=True):
        cmds.deleteUI('YM_AttributeInfoWindow')
    
    if len(attrInputConnection)==0:
        attrInputConnection = 'No Input Connection Exists'
    if len(attrOutputConnection)==0:
        attrOutputConnection.append('No Output Connection Exists')

    cmds.window('YM_AttributeInfoWindow',w=600,h=800,t='YM_AttributeInfoWindow')
    cmds.columnLayout()

    cmds.textField('YM_AttributeInfo_AttributeName',w=600,tx=attribute,en=False)
    cmds.textField('YM_AttributeInfo_AttributeType',w=600,tx=attrType,en=False)
    cmds.textField('YM_AttributeInfo_AttributeValue',w=600,tx=attrValue,en=False)
    cmds.textField('YM_AttributeInfo_AttributeInput',w=600,tx=attrInputConnection,en=False)
    cmds.textScrollList('YM_AttributeInfo_AttributeOutput',w=600)
    for output in attrOutputConnection:
        cmds.textScrollList('YM_AttributeInfo_AttributeOutput',e=True,a=output)

    cmds.showWindow('YM_AttributeInfoWindow')



