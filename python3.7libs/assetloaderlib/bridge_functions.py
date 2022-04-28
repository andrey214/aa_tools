import hou,os
from . import hda_core as hc
import __future__ 
#############################################################################
def collectpath(pathtex,jobvar,name):
    if hou.getenv(jobvar)!=None:
        job=hou.getenv(jobvar)
        addpath='/data/tex/megascans'
        dirs=addpath.split('/')
        if not os.path.isdir(job+addpath):
            for d in dirs:
                job=job+'/'+d
                if not os.path.isdir(job):
                    os.mkdir(job, 0o777)
        else:
            job=(job+addpath)
            texname=pathtex.split('/')[-1]
            if os.path.isfile(pathtex):
                newfiledir=job+'/'+name
                if not os.path.isdir(newfiledir):
                    os.mkdir(newfiledir, 0o777)
                newfile=newfiledir+'/'+texname
                if not os.path.isfile(newfile):
                    os.system('cp '+pathtex+' '+newfile)
                pathtex=newfile.replace(hou.getenv(jobvar), '$'+jobvar)
    return pathtex
#############################################################################
##RAT REPLACE
def rplacerat(path):
    types=['.jpg','.jpeg','.tiff','.tif','.tga','.exr','png']
    pathf=path
    for t in types:
        if path.endswith(t):
            path= path.replace(t, '.rat')
            break
        
    path=path.replace('\\','/')
    return path
##JOB REPLACE
############################################################################
##Create Node geometry
def crnode():
    obj=hou.node('/obj')
    srcc=hou.node('/obj/megascans')
    if srcc==None:
        srcc = obj.createNode('geo', 'megascans')
        srcc.setColor( hou.Color( (0.5, 0.7882 , 0.5) ) )
        srcc.setDisplayFlag(True)
    return srcc
############################################################################
            
#######
def rendernode(node):
    try:
        node.setDisplayFlag(True)
        node.setRenderFlag(True)
    except:
        pass
def assetnode(name,json='',res='2K'):
    asset= None
    try:
        sel=hou.selectedNodes()
        if len(sel)>0:
            seltp=sel[0].type()
            try:
                seldef=seltp.definition()
            except:
                pass
            b=seltp.category()
            if b.name() == 'Sop' or b.name() == 'Object':
                selname=''
                if seldef is not None:
                    selname=seldef.nodeTypeName()
                sop=b.name()
                if sop == 'Sop' and 'asset_loader' not in selname:
                    asset=sel[0].createOutputNode('asset_loader',name)
                elif sop == 'Object' and not sel[0].isLockedHDA() and not sel[0].isSubNetwork():
                    nodesinside=sel[0].children()
                    if len(nodesinside)>0:
                        for n in nodesinside:
                            if n.isDisplayFlagSet():
                                asset=n.createOutputNode('asset_loader',name)
                                break
                    else:
                        asset=sel[0].createNode('asset_loader',name)
                        
                elif 'asset_loader' in selname:
                    asset=sel[0]
                    asset.setName(name)
                    asset.parm('json').set(json)
                    asset.parm('resolution').set(res)
                    
                    
                    #print(asset.parm('json').eval())
                    #print('ok')
                else:
                    asset=sel[0].createNode('asset_loader',name)
                    
            else:
                if b.name() == 'Lop' and seldef is not None:
                    if seldef.nodeTypeName()=='sopcreate':
                        asset=sel[0].createNode('asset_loader',name)
                
        else:
            try:
                currenrui=hou.ui.curDesktop().paneTabOfType(hou.paneTabType.TreeView).pwd().type().name()
                if currenrui=='geo':
                    geonode=hou.ui.curDesktop().paneTabOfType(hou.paneTabType.TreeView).pwd()
                    asset=geonode.createNode('asset_loader::1.0',name)
                elif currenrui=='stage':
                    stagenode=hou.node(hou.ui.curDesktop().paneTabOfType(hou.paneTabType.TreeView).pwd().path())
                    lopnode=stagenode.createNode('sopcreate','megascans')
                    createnode=hou.node(lopnode.path()+'/sopnet/create')
                    asset=createnode.createNode('asset_loader::1.0',name)
                    asset.moveToGoodPosition()
                #elif currenrui=='obj':
                else:
                    obj=hou.node('/obj')
                    srcc=hou.node('/obj/megascans')
                    if srcc==None:
                        srcc = obj.createNode('geo', 'megascans')
                        srcc.setColor( hou.Color( (0.5, 0.7882 , 0.5) ) )
                        srcc.setDisplayFlag(True)
                    asset = srcc.createNode('asset_loader::1.0',name)
            except:        
                raise                                                   
    except:
        pass
    
    if json !='' and asset!= None:
        asset.parm("json").set(json)
        asset.parm('resolution').set(res)
        asset.parm('load').pressButton()
        if asset.isSelected():
            hc.refresh(asset)

    rendernode(asset)
    return asset
###########################################################################
#########################################################################
###Separator

def geometry_asset(self, subnet, meshList, material,json,res='2K'):
    separated_items = []
    c = 0
    for mesh in meshList:
        if self.Workflow=='Custom MRP Shader':
            flec = subnet.createNode('file')
            flec.parm('file').set(mesh[1])
            flec.moveToGoodPosition()
            trans_node = flec.createOutputNode('xform')
            trans_node.parm('scale').set('0.05')
            mtl_node = trans_node.createOutputNode('material')
            mtl_node.setDisplayFlag(True)
            mtl_node.setRenderFlag(True)
            rel_path = str( mtl_node.relativePathTo(material))
            mtl_node.parm('shop_materialpath1').set(rel_path)
            soup=mtl_node.createOutputNode('polysoup') #convertpolysoup
            soup.setDisplayFlag(True) #display
            soup.setRenderFlag(True)
            separated_items.append(soup)
        if self.Workflow=='Custom Asset Loader' and material !=None:
            material.parm('geometry').set(mesh[1])
            material.setDisplayFlag(True) #display
            material.setRenderFlag(True)
            separated_items.append(material)
            if material.parm("json")!=None:
                material.parm("json").set(self.json)
            if material.parm('resolution')!=None:
                material.parm('resolution').set(res)
            if material.parm('load')!=None:
                material.parm('load').pressButton()   

    return separated_items
########################################################################
