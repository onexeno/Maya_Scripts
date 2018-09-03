from maya.cmds import *
from pymel.all import *
def mainWindow():
    if window('RenderPassManager',ex=True):
        deleteUI('RenderPassManager')
    
    window('RenderPassManager',t='RPM',h=200,w=400)
    frameLayout(l='RPM for Mentalray',bgc=[0.5,0.2,0.1])
    scrollLayout(w=600,h=200)
    rowLayout(nc=2)
    columnLayout()
    textField(w=300)
    fristCol = textScrollList(w=300,h=600)
    setParent('..')
    columnLayout()
    textField(w=300)
    secondCol = textScrollList(w=300,h=600)
    setParent('..')
    setParent('..')
    showWindow('RenderPassManager')
#
def checkRenderPassStatus(renderPass):
    getAttr(renderPass+'.renderable')
    
    
def createWTBNode(*name):
    if(len(name)>0):
        print('Successful for created <<'+name[0]+'>> Node!')
        return createNode('writeToColorBuffer',n=name[0])
    else:
        print('Successful for created <<writeToColorBuffer>> Node!')
        return createNode('writeToColorBuffer')
        
#
def createWTBBySelectedMaterials(renderPassMenu):
    #matList = ls(mat=True)
    renderPass = optionMenu(renderPassMenu,q=True,v=True)
    matList = ls(sl=True,mat=True)
    if(len(matList)!=2):
        warning("Select Two Material")
    else:
        newName = matList[0]+'_'+renderPass+'_WTCB'
        if(objExists(newName)==False):
            newWTCB = createWTBNode(newName)
            lockNode(newWTCB,l=1)  #writeToColorBuffer sometimes will be delete when save as... so lock the node...
            try:
                connectAttr(matList[0]+'.outColor',newWTCB+'.evaluationPassThrough')
                print('################# Info ##################\n')
                print('| '+matList[0]+'.outColor'+newWTCB+'.evaluationPassThrough | Connection Successful!')
            except:
                warning('| '+matList[0]+'.outColor'+newWTCB+'.evaluationPassThrough | Connection Failed')
            try:
                connectAttr(matList[1]+'.outColor',newWTCB+'.color')
                print('| '+matList[1]+'.outColor'+newWTCB+'.color | Connection Successful!')
            except:
                warning('| '+matList[1]+'.outColor'+newWTCB+'.color | Connection Failed!')
            try:
                connectAttr(renderPass+'.message',newWTCB+'.renderPass')
                print('| '+renderPass+'.message'+newWTCB+'.renderPass | Connection Successful!\n')
                print('################# Info ##################')
            except:
                warning('| '+renderPass+'.message'+newWTCB+'.renderPass | Connection Failed!')
                
        else:
            warning(' > > > > > >> | ' + newName + ' | << < < < < < is already exists in this sence !!')
#           
def connectSelectWTBtoRenderPass(renderPassMenu):
    wtb = ls(sl=True,typ='writeToColorBuffer')
    for i in wtb:
        try:
            connectAttr(optionMenu(renderPassMenu,q=True,v=True)+'.message',i+'.renderPass')
        except:
            disconnectAttr(connectionInfo(i+'.renderPass',sfd=True),i+'.renderPass')
            connectAttr(optionMenu(renderPassMenu,q=True,v=True)+'.message',i+'.renderPass')
#
def lockSelNode():
    selectNodes = ls(sl=True)
    for node in selectNodes:
        try:
            lockNode(node,l=1)
        except:
            continue

def unlockNode():
    selectNodes = ls(sl=True)
    for node in selectNodes:
        try:
            lockNode(node,l=0)
        except:
            continue

def createWTBWindow():
    global menuGrp
    if (window('WTBWindow',ex=True)):
        deleteUI('WTBWindow')
    #window('WTBWindow',t='WTBWindow',w=120,h=100,cc=Callback(resetMenuGrp))
    window('WTBWindow',t='WTBWindow',w=120,h=100) 
    columnLayout()
    renderPassMenu = optionMenu(w=230)
    
    createMenuItem(renderPassMenu)
    rowLayout(nc=5)
    
    button(l='Surface',w=50,h=36,c='shadingNode("surfaceShader",asShader=True)',bgc=[0.1,0.3,0.3])
    button(l='Create',w=70,h=36,c=Callback(createWTBBySelectedMaterials,renderPassMenu),bgc=[0.2,0.3,0.2])
    button(l='Connect',w=50,h=36,c=Callback(connectSelectWTBtoRenderPass,renderPassMenu),bgc=[0.3,0.1,0.3])
    button(l='L',w=25,h=36,c=lambda x:lockSelNode(),bgc=[0.6,0.1,0.3])
    button(l='O',w=25,h=36,c=lambda x:unlockNode(),bgc=[0.1,0.3,0.6])
    
    scriptJob(e=['renderLayerManagerChange',Callback(createMenuItem,renderPassMenu)],p='WTBWindow')
    #scriptJob(e=['SelectionChanged',Callback(createMenuItem,renderPassMenu)],p='WTBWindow')
    showWindow('WTBWindow')
global menuGrp
menuGrp = []
#menuItem
def resetMenuGrp():
    global menuGrp
    menuGrp = []
    £
def createMenuItem(parentMenu):
    itemList = relationToRenderlayer()
    itemList.sort()
    global menuGrp
    if(len(menuGrp)>0):
        for item in menuGrp:
            deleteUI(item,mi=True)
       
        menuGrp = []
        menuGrp.append(menuItem(l='<None>',p=parentMenu))
        for i in itemList:
            menuGrp.append(menuItem(l=i,p=parentMenu))
        #print menuGrp
    else:
        menuGrp = []        
        menuGrp.append(menuItem(l='<None>',p=parentMenu))
        for i in itemList:
            menuGrp.append(menuItem(l=i,p=parentMenu))
#
def relationToRenderlayer():
    
    renderPassOwner = editRenderLayerGlobals(q=True,crl=True)
    renderPassInLayer = connectionInfo(renderPassOwner+'.renderPass',dfs=True)
    renderPass = []
    for renderPassFilter in renderPassInLayer:
        renderPasses = renderPassFilter.split('.')
        renderPass.append(renderPasses[0])
    return renderPass
    
    
createWTBWindow()
#createWTBBySelectedMaterials('surfaceShader1','surfaceShader2','renderPass1')
    
#createWTB('abc')
