import hou
import hda_core
conform=None
try:
    import ms_shading_conform as conform
except:
    pass
if conform is None:
    from . import conform
    
import __future__ 

#########Check Convert
def convertassets(node):
    split_custom_materials(node)

    
##############Convert To simple Shader     
def split_custom_materials(node):
    basenode=node
    srcnode=hou.node(node.path()+'/source')
    geo=srcnode.geometry()
    mat_attr = geo.findPrimAttrib(basenode.parm("material_attrib").eval())
    folder=basenode.parm("mat_lib").eval()
    
    shadertp=node.parm('shader').eval()
    ops=conform.conformlist()[0]
    properties=ops[shadertp]
    type=properties['node']
    
    #Offsets
    offset_y = 0
    offset_x = 0

    primgroups = geo.primGroups()
    for primgroup in primgroups:
        index = primgroups.index(primgroup)
        m=primgroup.name()
        mn=m.replace(" ","_")
        shadernet=hou.node(folder+'/'+mn)
        if shadernet == None:
            shadernet = hou.node(folder).createNode(type, mn)
        if primgroup.prims()>0:
            prim=primgroup.prims()[0]
            copyvaluesattr(prim,shadertp,shadernet)

            if index % 10 == 0:  
                offset_y -= 2
                offset_x = 0
            else:
                offset_x = offset_x + 2
                
            shadernet.setPosition([offset_x,offset_y])
        else:
            print("group "+m+" dont have primitives!!!")
  
#####Advance Convert
def string2parm(node,val,strparm):
    try:
        enabletex=node.parm(val.replace('texture','enable'))
        usetex=node.parm(val.replace('texture','useTexture'))
        if node.parm(strparm) is not None:
            node.parm(strparm).set(val)
        if enabletex is not None:
            enabletex.set(1)
        if usetex is not None:
            usetex.set(1)
        
    except:
        pass
def advance_custom_materials(node):
    basenode=node
    node=hou.node((hou.pwd()).path()+'/source')
    geo=node.geometry()
    mat_attr = geo.findPrimAttrib(basenode.parm("material_attrib").eval())
    folder=basenode.parm("mat_lib").eval()
    #Offsets
    offset_y = 0
    offset_x = 0
    
def copyvalues(node,name,shader):
    if node != None and name !="":
        
        ops=conform.conformlist()[0]
        properties=ops[name]
        maps=properties['maps']
        vals=properties['values']
        if len(maps)>0:
            for m in maps:
                try:
                    bsparm=node.parm(properties[m][1])
                    shparm=shader.parm(properties[m][0])
                    if shparm is not None and bsparm is not None:
                        val=node.parm(properties[m][1]).rawValue()
                        shparm.set(val)
                except:
                    pass
        if len(vals)>0:
            for v in vals:
                try:
                    bsparm=node.parm(properties[v][1])
                    shparm=shader.parm(properties[v][0])
                    if shparm is not None and bsparm is not None:
                        val=node.parm(properties[v][1]).eval()
                        shparm.set(val)
                except:
                    pass

def copyvaluesattr(prim,name,shader):
    if prim != None:
        ops=conform.conformlist()[0]
        properties=ops[name]
        maps=properties['maps']
        vals=properties['values']
        if len(maps)>0:
            for m in maps:
                try:
                    bsparm=prim.stringAttribValue(properties[m][2])
                    shparm=shader.parm(properties[m][0])
                    if shparm is not None and bsparm is not None:
                        val=hda_core.jobreplace(bsparm)
                        shparm.set(val)
                except:
                    pass
        if len(vals)>0:
            for v in vals:
                try:
                    bsparm=prim.AttribValue(properties[v][2])
                    shparm=shader.parm(properties[v][0])
                    if shparm is not None and bsparm is not None:
                        val=node.parm(bsparm)
                        shparm.set(val)
                except:
                    pass
