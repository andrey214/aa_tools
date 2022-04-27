from __future__ import print_function
import os,json,shutil,sys,re,hou #glob,
import subprocess
import atexit
import toolutils

from . import bridge_core as bridge
##########
from . import connect as conn
conf=None
try:
    import ms_shading_conform as conf
except:
    pass
if conf is None:
    from . import conform as conf
    
from . import convert as conv

if hou.isUIAvailable():
    import nodegraphutils as utils


hou.putenv('Bridge_pid','')

def collectdir(node):
    data=hou.getenv('JOB')+'/data/cache'
    if os.path.isdir(data):
        val="$JOB/data/cache/generic/megascans/"+"`chs("+'"category"'+")`"+"/`chs("+'"name"'+")`"
        node.parm("job_path").set(val)
        
def dorat(node):
    rtconv=hou.getenv('RATPROCESS')
    if rtconv=='1':
        node.parm('crat').set(1)
    elif rtconv=='0':
        node.parm('crat').set(0)
        
def doaces(node):
    rtconv=hou.getenv('OCIO')
    if rtconv is not None:
        node.parm('aces').set(1)
    else:
        node.parm('aces').set(0)
                
def evars(node):
################EnvVars
    enviroments=[]
    try:
        work_dir_raw=node.parm('job_path').rawValue()
        tmpenv=work_dir_raw.split('/')
        for t in tmpenv:
            if '$' in t:
                for n in t.split('_'):
                    if n.startswith('$'):
                        enviroments.append(n.replace('$',''))
    except:
        pass
##################End Vars   
    return enviroments
    
def jobreplace(path,env='JOB'):
    job=hou.getenv(env)
    filepath=path
    try:
        if job in path:
            filepath=path.replace(job,'$'+env)
    except:
        pass
    
    try:
        if get_platform()=='Windows':
            filepath=path.replace('\\','/')
    except:
        pass
    filepath=path.replace('\\','/')
    return filepath
#####
def checkcollect(path,jbpath):
    job=hou.getenv('JOB')
    if not job in path:
        filepath=jbpath+'/'+os.path.basename(path)
        if os.path.isfile(filepath):
            newpath=filepath
        else:
            newpath=path
    return newpath
        
def checkbridge(node):
#####Detect Bridge
    a=1
    try:
        env=hou.getenv('QMEGASCAN_LIB')
        if env is not None:
            a=0
    except:
        pass
    node.parm('open_bridge').hide(a)
    

def categorytype(node):
    cat=node.parm('category').eval()
    geo={'geometry','Geometry','Mesh','mesh','3d','3dplant'}
    atlas={'Atlas','atlas'}
    if cat in geo:
        out = 0
    elif cat in atlas:
        out = 1
    else:
        out = 2
    node.parm('type').set(out)
    return out
######
import signal

def kill_child(child_pid):
    if child_pid is None:
        pass
    else:
        try:
            os.kill(child_pid, signal.SIGTERM)
        except:
            pass

def init_connect():
    bridgesetup=hou.getenv('bridgesetup')
    if bridgesetup == None:
        bridge.initbridgeconnect()
        hou.putenv('bridgesetup','initialised')
        
def start_bridge():
    init_connect()
    try: 
        path=hou.getenv('QMEGASCAN_LIB')
        DETACHED_PROCESS = 0x00000008
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        if os.path.isfile(path):
            launch=os.path.normpath(path.replace('\\','/'))
        else:
            launch=os.path.normpath((path+"/Bridge.AppImage").replace('\\','/'))
        if os.path.isfile(launch):
            try:
                with open(os.devnull, 'w') as fp:
                    proc = subprocess.Popen(launch, shell=False , stdout=fp, creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
                    child_pid = proc.pid
                    atexit.register(kill_child,child_pid)
            except:
                pass
        else:
            print('No found Application')
                
    except:
        print("No found Bridge Connector")


#####################        
def cleannodeparm(node):
    try:
        parms=node.type()       
        parms=parms.definition()
        parms=parms.parmTemplateGroup()
        parms=parms.find("parameters_1")
        parms=parms.parmTemplates()
        for p in parms:
            if type(p.eval()).__name__=='str':
                node.parm(p.name()).set("")
    except:
        pass
        
######On create functions
def nodeprop(node):
    color=hou.Color((0.92,0.35,0.35))
    node.setColor(color)
##Lods_menu_set


def lodslist(node):
    if node.parm('mergevars').eval()==0:
        try:
            data = node.userData('geometry').split("*?*")
            idlength=0
            menu = []
            for i in data:
                k=i.split('!!')
                #menu += [data.index(i)[0], i]
                if len(k)==2:
                    menu += [k[1], k[0]]
        except:
            menu = ['None', 'None']
    else:
        try:
            data = node.userData('geometry').split("*?*")
            menu = []
            testlist = []
            tst=0
            for i in data:
                k=i.split('!!')
                #menu += [data.index(i)[0], i]
                if len(k)==2:
                    if 'var' in  k[0]:
                        tst=1
                        tp=k[0].split("_")
                        if tp[1] not in testlist:
                            menu += [k[1], tp[1]]
                            testlist.append(tp[1])
                    else:
                        menu += [k[1], k[0]]


                
        except:
            menu = ['None', 'None']
        
    return menu
    



def varscheck(node):
    try:
        data = node.userData('geometry').split("*?*")
        menu = []
        a=0
        for i in data:
            k=i.split('!!')
            if len(k)==2:        
                if 'var' in  k[0]:
                    a=1
                    break
                else:
                    a=0
                    node.parm('mergevars').set(0)
                    
        node.parm('mergevars').hide(a)

    except:
        pass
    
    return a
    
def checkidxlods(node):
    try:
        items=node.parm('lods').menuItems()
        if len(items)>0: 
            node.parm('lods').set(items[0])       
            node.parm('geometry').set(items[0])
    except:
        pass

#####LOD set to menu
def lodset(node):
    glibpath=hou.getenv('ASSETS_LIBRARY')
    items=node.parm('lods').menuItems()
    if len(items)>0 and node.parm('lods').eval()=="": 
        geometryfile=items[0]
        if glibpath !=None and glibpath in geometryfile:
            geometryfile=jobreplace(geometryfile,'ASSETS_LIBRARY')
        geometryfile=geometryfile.replace('\\','/')      
        node.parm('lods').set(geometryfile)
        node.parm('geometry').set(geometryfile)
    else:
        if node.parm('collected').eval():
            jb=node.parm('job_path').eval()
            geometryfile=jobreplace(checkcollect(node.parm('lods').eval(),jb))
        else:
            geometryfile=node.parm('lods').eval()
            
        if glibpath !=None and glibpath in geometryfile:
            geometryfile=jobreplace(geometryfile,'ASSETS_LIBRARY')
            
        geometryfile=geometryfile.replace('\\','/')
        node.parm('geometry').set(geometryfile)

    ###try packed
    packedfromgeo(node)
#####Get OS name        
def get_platform():
    platforms = {
        'linux1' : 'Linux',
        'linux2' : 'Linux',
        'darwin' : 'OS X',
        'win32' : 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform   
    return platforms[sys.platform]
####UdimFunctions
def udimfilename(file,udim):
    if int(hou.applicationVersionString().split(".")[0])>=18:
        filename=file.replace('<UDIM>',str(int(1001+udim)))
    else:
        filename=file.replace('%(UDIM)d',str(int(1001+udim)))
    return filename
    
def replaceudim(file,out=0):
    ftype=file.split('.')
    ####Udim start udim to textures    
    if out!=0:
        ftype[1]='1001'
    else:
        if int(hou.applicationVersionString().split(".")[0])>=18:
            ftype[1]='<UDIM>'
        else:
            ftype[1]='%(UDIM)d'
    filename='.'.join(ftype)
    return filename
    
####RAT
def convertrat(node,tex,tconvert=0,acesuse=0):
    if acesuse==1:
        node.parm('aces').set(0)
        
    res=2048
    sres='_2K_'
    str_res=['_1K_','_2K_','_4K_','_8K_']
    if node.parm('resolution') is not None:
        res=int(node.parm('resolution').eval()[0])*1024
        sres='_'+node.parm('resolution').eval()+'_'        
    job=os.path.normpath(hou.getenv('JOB'))
    if 'acescg.rat' in tex[1] or 'raw.rat' in tex[1] and acesuse==0:
        new=tex[1].split(".")
        new.pop()
        new.pop()
        a=0
        new=".".join(new)
    else:
        new=tex[1].split(".")
        new.pop()
        a=0
        new=".".join(new)
    
    parmaces={'albedo_texture','trans_texture','sss_texture'}
    if node.parm('aces').eval()==1 and acesuse==0:
        if tex[0] in parmaces:
            newname=new+'.'+'acescg.rat'
            a=0
        else:
            newname=new+'.'+'raw.rat'
            
            a=1
    else:
        newname=new+'.rat'
  
    if tconvert==1:
        for s in str_res:
            if s in newname:
                tmp_name=os.path.basename(newname)
                tmp_path=os.path.dirname(newname)
                tmp_name=tmp_name.replace(s,sres)
                newname=tmp_path+'/'+tmp_name
                break  
    newname=os.path.normpath(newname)
    if get_platform()=='Windows':
        newname=newname.replace('\'','/') 
####Execute  Cop
    if not os.path.exists(newname):
        readnode=hou.node(node.path()+"/rat/input")
        linnode=hou.node(node.path()+"/rat/linear")
        writenode=hou.node(node.path()+"/rat/output")
        linnode.parm('linear').set(a)
        readnode.parm('filename1').set(tex[1])
        
        if node.parm('aces').eval()==1 and acesuse==0:
            aceseval=node.parm('aces').eval()
        elif acesuse==1:
            aceseval=node.parm('aces').set(0)
        else:
            aceseval=0
            
        if tconvert==1:
            writenode.parm('tres').set(9)
            writenode.parm('res1').set(res)
            writenode.parm('res2').set(res)
            if tex[1].endswith('.rat'):
                node.parm('aces').set(0)
        writenode.parm('copoutput').set(newname)
        writenode.parm('execute').pressButton()
        node.parm('aces').set(aceseval)

        
        ###CleanParms
        writenode.parm('tres').set(6)
        writenode.parm('copoutput').set('')
        readnode.parm('filename1').set('')    

    newname=jobreplace(newname)     
    glibpath=hou.getenv('ASSETS_LIBRARY')
    if glibpath !=None and glibpath in newname:
        newname=jobreplace(newname,'ASSETS_LIBRARY')       
    return newname

def loadjsdata(node):
    jsonpath=''
    jsondata={}
    try:
        jsonpath=node.parm('input_data').eval()
    except:
        pass
    if jsonpath == '':
        jsonparm=node.parm('json').eval()
    else:
        jsonparm=jsonpath
        node.parm('json').set(jsonpath)
    if os.path.isfile(jsonparm):
        opfile=open(jsonparm, 'r')
        jsondata=json.load(opfile)
    return jsondata    
    
    
    
def resizetex(node):
    ####json
    jsondata=loadjsdata(node)
    ####CustomProperties
    udimed=0
    udimcount=1
    acesval=0
    try:
        udimed=int(jsondata['udim'])
    except:
        udimed=0
    try:
        udimcount=int(jsondata['udimcount'])
    except:
        udimcount=1
    try:
        acesval=int(jsondata['ocio'])
    except:
        acesval=0          
   
    #####
    parms=node.type()       
    parms=parms.definition()
    parms=parms.parmTemplateGroup()
    parms=parms.find("parameters_1")
    parms=parms.parmTemplates()

    for p in parms:
    
        cont=str(node.parm(p.name()).eval())
        if 'texture' in p.name() and  cont !='':
            if udimed==1 and udimcount>1:
            ####
                cont=replaceudim(cont,0)
                tmp_cont=cont
                for i in range(udimcount):
                    contex=udimfilename(cont,i)
                    resized=convertrat(node,[p.name(),contex],1,acesval)
                resized=replaceudim(udimfilename(resized,0))
            else:    
                resized=convertrat(node,[p.name(),cont],1,acesval)
            node.parm(p.name()).set(resized)
            
    shader_parm=node.parm('setcustom_shader').eval()        
    shader=hou.node(shader_parm)    
    if node.parm('converted').eval()!=0 and shader is not None:
        node.parm('convertshader').pressButton()


####Collect
def collect(node):           
    work_dir=node.parm('job_path').eval()
    orig_geo=node.parm('geometry').eval()
    jsonfile=node.parm('json').eval()
    jsondir=work_dir
    if node.parm('ver').eval()!="":
        work_dir+='/'+node.parm('ver').eval()
    work_dir=os.path.normpath(work_dir)
    if get_platform()=='Windows':
        work_dir=work_dir.replace('\'','/')
    if not os.path.isdir(work_dir):
        try:
            os.makedirs(work_dir, 0o777)
        except OSError:
            print(("Creation of the directory %s failed" % work_dir))
    parms=node.type()       
    parms=parms.definition()
    parms=parms.parmTemplateGroup()
    parms=parms.find("parameters_1")
    parms=list(parms.parmTemplates())
    previewparm=node.parm('prv_path')
    job=os.path.normpath(hou.getenv('JOB'))
    
    parms.append(previewparm)
    for p in parms:
        cont=node.parm(p.name()).eval()
        if str(cont)!="" and type(cont).__name__=='str':
            if not 'UDIM' in cont:
                newcont=work_dir+'/'+os.path.basename(cont)
                newcont=os.path.normpath(newcont)
                if get_platform()=='Windows':
                    newcont=newcont.replace('\'','/')
                    job=job.replace('\'','/')
                if not os.path.exists(newcont) and cont!=newcont and os.path.exists(cont):
                    dest = shutil.copyfile(cont, newcont)
            else:
                try:
                    a=0
                    for i in range(100):
                        contex=udimfilename(cont,i)
                        newcont=work_dir+'/'+os.path.basename(contex)
                        newcont=os.path.normpath(newcont)
                        if not os.path.exists(newcont) and contex!=newcont and os.path.exists(contex):
                            dest = shutil.copyfile(contex, newcont)
                        if not os.path.exists(contex):
                            a+=1
                            if a>3:
                                break
                            
                    newcont=work_dir+'/'+os.path.basename(cont)
                    newcont=os.path.normpath(newcont)
                except:
                    pass
#            else:
#                print('Content path do not exists!!!')
                
            if job in newcont:
                newcont=newcont.replace(job,'$'+'JOB')
            
            envcont=newcont
            try:    
                for e in evars(node):
                    envcont=jobreplace(envcont,e)
            except:
                pass
                
            node.parm(p.name()).set(envcont)
    try:
        if node.parm('stick').eval()==1:
            stickprev(node,1)
    except:
        pass
    ######Geometry collect
    if categorytype(node)!=2: #and node.parm('geometry').eval()!="":
        #print(categorytype(node))
        #if categorytype(node)==0:
        #   basename=os.path.basename(node.parm('geometry').eval())
        #    basepath=os.path.dirname(orig_geo)
        #if categorytype(node)==1:
        #    basename=os.path.basename(node.parm('json').eval())
        #    basepath=os.path.dirname(jsonfile)
        #print(basepath)
        basepath=os.path.dirname(jsonfile)
        #bgeos=glob.glob(basepath+'/*.bgeo.sc')
        bgeos = [dir+'/'+f for (dir, subdirs, fs) in os.walk(basepath) for f in fs if f.endswith(".bgeo.sc")]
        for bgeo in bgeos:
            name=os.path.basename(bgeo)
            #if hou.node(node.path()+'/python1').parm('bool').eval()!=0:
            #    name=os.path.basename(bgeo)
            #else:
            #    name=(os.path.basename(node.parm('geometry').eval())).split(".")[0]
            newcont=work_dir+'/'+name
            if not os.path.isfile(newcont):
                shutil.copyfile(bgeo, newcont)
        node.parm('reload').pressButton()
    color=hou.Color((0.35,0.92,0.35))
    node.setColor(color)  
    node.parm('collected').set(1)
    
    shader_parm=node.parm('setcustom_shader').eval()        
    shader=hou.node(shader_parm)    
    if node.parm('converted').eval()!=0 and shader is not None:
        node.parm('convertshader').pressButton()
    
def bakegeo(node):
        origcolor=node.color()
        origpos=node.position()
        node.parm('reload').pressButton()
        bake_node=hou.node(node.path()+'/bake')
        bake_node.parm('execute').pressButton()
        filepath=bake_node.parm('sopoutput').eval()
        job=hou.getenv('JOB')
        filepath=jobreplace(filepath,'ASSETS_LIBRARY')
        filepath=jobreplace(filepath,'JOB')
        
        try:    
            for e in evars(node):
                filepath=jobreplace(filepath,e)
        except:
            pass
            
        file=node.changeNodeType("file",keep_parms=False) ###Change to filenode
        file.parm("file").set(filepath)
        if file.parm('application') is not None:
            ptg=file.parmTemplateGroup()
            ptg.remove(ptg.find("application"))
            file.setParmTemplateGroup(ptg)
            
def bakesurface(node):
    con_parm=node.parm('converted').eval()
    shader_parm=node.parm('setcustom_shader').eval()
    shader=hou.node(shader_parm)
    if con_parm==0 or shader is None:
        parameters=node.parms()
        values=[]
        
        if node.parm('use_true').eval()==1:
            mat=['shop_materialpath',"/obj/megascans_shading1/ms_shading/megascans_shader_simple1"]
        else:
            mat=['shop_materialpath',"/obj/megascans_shading1/ms_shading/megascans_shader_simple2"]
        json=node.parm('json').eval()
        
        values.append(mat)
        for p in parameters:
            tps=p.eval()
            if str(tps)!="" and type(tps).__name__=='str':
                if p.name()=='ao_texture':values.append(['ms_ao',p.eval()])
                if p.name()=='albedo_texture':values.append(['ms_diffuse',p.eval()])
                if p.name()=='bump_texture':values.append(['ms_bump',p.eval()])
                if p.name()=='ior_texture':values.append(['ms_ior',p.eval()])
                if p.name()=='disp_texture':values.append(['ms_displace',p.eval()])
                if p.name()=='reflect_texture':values.append(['ms_reflect',p.eval()])
                if p.name()=='spec_texture':values.append(['ms_spec',p.eval()])
                if p.name()=='metallic_texture':values.append(['ms_metal',p.eval()])
                if p.name()=='normal_texture':values.append(['ms_normal',p.eval()])
                if p.name()=='sss_texture':
                    values.append(['ms_sss',p.eval()])
                    if p.eval()!="":
                        values.append(['ms_usesss',1])
                
                if p.name()=='opaccolor_texture':values.append(['ms_opac',p.eval()])
                if p.name()=='trans_texture':values.append(['ms_trans',p.eval()])
                if p.name()=='fuzz_texture':values.append(['ms_fuzz',p.eval()])
                if p.name()=='mask_texture':values.append(['ms_mask',p.eval()])
                if p.name()=='rough_texture':values.append(['ms_rough',p.eval()])
                if p.name()=='normalb_texture':values.append(['ms_normalbump',p.eval()])
                if p.name()=='rough':values.append(['ms_rscale',p.eval()])
                if p.name()=='dispTex_scale':values.append(['ms_dscale',p.eval()])
                if p.name()=='reflect_scale':values.append(['reflect_scale',p.eval()])
                if p.name()=='use_opacity':values.append(['use_opacity',p.eval()])
                
        newnode=node.changeNodeType("attribcreate::2.0",keep_parms=False,keep_network_contents=False)
        newnode.parm('numattr').set(len(values)+1)
        for idx, val  in enumerate(values):
            newnode.parm('name'+str(idx+1)).set(val[0])
            newnode.parm('class'+str(idx+1)).set(1)
            newnode.parm('precision'+str(idx+1)).set(1)
            if type(val[1]).__name__=='str':
                newnode.parm('type'+str(idx+1)).set(3)
                newnode.parm('string'+str(idx+1)).set(val[1])
            if type(val[1]).__name__=='float':
                newnode.parm('type'+str(idx+1)).set(0)
                newnode.parm('value'+str(idx+1)+'v1').set(val[1])
                newnode.parm('name'+str(idx+1)).set(val[0])
    #####JSON_Attr
        newnode.parm('name'+str(len(values)+1)).set('json')
        newnode.parm('class'+str(len(values)+1)).set(0)
        newnode.parm('precision'+str(len(values)+1)).set(1)
        newnode.parm('type'+str(len(values)+1)).set(3)
        newnode.parm('string'+str(len(values)+1)).set(json)
    else:
        newnode=node.changeNodeType("material",keep_parms=False,keep_network_contents=False)
        newnode.parm('num_materials').set(1)
        newnode.parm('shop_materialpath1').set(shader_parm)
        
    ###Clean    
    if newnode.parm('application') is not None:
        ptg=newnode.parmTemplateGroup()
        ptg.remove(ptg.find("application"))
        newnode.setParmTemplateGroup(ptg)
        
    

def bake(node):
    with hou.undos.group("Bake of My Asset"):
        if categorytype(node)==2:
            bakesurface(node)
        else:
            bakegeo(node)


    
####EndCollect
############Remap
def remaprange(value, inMin, inMax, outMin, outMax):
    value = min(value, inMax)
    value = max(value, inMin)
    inSpan = inMax - inMin
    outSpan = outMax - outMin
    scaled = float(value - inMin) / float(inSpan)
    return outMin + (scaled * outSpan)
################
if hou.isUIAvailable(): #For Afanasy
    from PySide2 import QtCore, QtGui, QtWidgets
#preview
if hou.isUIAvailable(): #For Afanasy
    class assetPreview(QtWidgets.QDialog):
        def __init__(self):
            super(assetPreview, self).__init__()
    
            hbox = QtWidgets.QVBoxLayout()
            self.l = QtWidgets.QLabel(self)
            hbox.addWidget(self.l)        
           
            self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
            
        def center(self):
            qr = self.frameGeometry()
            cp = QtWidgets.QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())
            
        def showWindow(self, name, img):
            #pixmap = QtGui.QPixmap()
            scaleval=500
            pixmap = QtGui.QPixmap(img)
            #pixmap = pixmap.scaledToHeight(scaleval)
            nhid=pixmap.size().height()
            prop=float(scaleval)/float(nhid)
            rewid=pixmap.size().width()
            nwid=int(float(rewid)*prop)
            pixmap=pixmap.scaled(nwid ,scaleval, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.l.setPixmap(pixmap)
            #cp = QtWidgets.QDesktopWidget().availableGeometry().center()
            ##xpos=int(cp.x()-int(float(nwid)/2))
            ##ypos=int(cp.y()-int(float(scaleval)/2))
            #self.setGeometry(xpos, ypos, nwid, scaleval)
            self.setMinimumSize(QtCore.QSize(nwid, scaleval))
            self.setMaximumSize(QtCore.QSize(nwid, scaleval))
            self.setWindowTitle(name)

if hou.isUIAvailable(): #For Afanasy
    dialog = assetPreview()
    
def preview(node):
    img = node.parm('prv_path').eval()
    name = node.parm('name').eval()
    exists = os.path.isfile(img)
    
    if hou.isUIAvailable() and exists: #For Afanasy
        #Call window widget
        dialog = assetPreview() 
        dialog.showWindow(name, img)
        dialog.show()

def stickprev(node,tog=1):
    img = node.parm('prv_path').eval()
    stick = node.parm('stick').eval()
    pixmap = QtGui.QPixmap(img)
    try:
        imgs=[]
        if img !="":
            pixmap = QtGui.QPixmap(img)
            scaleval=2
            nhid=pixmap.size().height()
            rewid=pixmap.size().width()
            prop=float(scaleval)/float(nhid)
            nwid=float(rewid)*prop
        
            npos=node.position()
            editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
            image = hou.NetworkImage()
            image.setPath(img)
            ofst=0.01
            x=npos.x()+ofst
            y=npos.y()+ofst
            bound=hou.BoundingRect(0, 0, nwid, scaleval)
            #bound.translate(npos)
            image.setRect(bound)
            image.setRelativeToPath(node.path())
            imgs=list(editor.backgroundImages())
            chk=1
            if len(imgs)>0:
                for i in imgs:
                    if i.relativeToPath()==node.path():
                        chk=0
                        break
                    
                if chk==0 and i.path()!=img:
                    i.setPath(img)
            else:
                chk=1
            
            if chk==1:
                imgs.append(image)
#####Toggle
            if stick==1 and tog:
                editor.setBackgroundImages(tuple(imgs))
                try:
                    utils.saveBackgroundImages(editor.pwd(), tuple(imgs))
                except:
                    pass            
            else:
                for i in imgs:
                    if i.relativeToPath()==node.path() or i.relativeToPath()=="":
                        imgs.remove(i)
                editor.setBackgroundImages(tuple(imgs))
                try:
                    utils.saveBackgroundImages(editor.pwd(), tuple(imgs))
                except:
                    pass
    except:
        pass


def cleanstring(name=''):
    chars=[' ','`',"'",'"',':',';','|']
    for c in chars:
        name=name.replace(c,"_")
    
    return name

####LOAD
def load3djson(node,jsondata,file):
    tags=jsondata['tags']
    ####CustomProperties
    udimed=0
    udimcount=1
    acesval=0
    try:
        if jsondata['pack']=="MRP":
            node.parm('re_scale').set(0)
    except:
        pass
     
    try:
        udimed=int(jsondata['udim'])
    except:
        udimed=0
    try:
        udimcount=int(jsondata['udimcount'])
    except:
        udimcount=1        
    try:
        acesval=int(jsondata['ocio'])
    except:
        acesval=0         
    categories=jsondata['categories']
    
    
    id=jsondata['id']
    asset_path=file.split("/")
    asset_path.pop()
###Version
    try:
        ver=jsondata['version'][len(jsondata['version'])-1]
    except:
        ver=""
####resolution
    resparm=node.parm('resolution')
    pixel=int(resparm.eval()[0])*1024
    pres=str(pixel)+'x'+str(pixel)
    try:
        res=((asset_path[len(asset_path)-1]).split("_"+id+"_")[1]).split("_")[0]
        newval=""
        for v in res:
            if v.isnumeric() or v in '.,':
                newval+=v 
        resolution=str(int(newval)*1024)+'x'+str(int(newval)*1024)
    except:
        resolution=pres
    
    
###Asset_DIR    
    asset_dir=os.path.dirname(os.path.normpath(file))
###NAME
    try:
        name=(jsondata['name'].replace(" ","_"))+'_'+id
    except:
        name=(asset_path[len(asset_path)-1]).split("_"+id)[0]+'_'+id
    name=cleanstring(name)
    
###PREVIEW
    preview1 = ""
    if preview1 == "":
        prefiles=os.listdir(asset_dir)
        for f in prefiles:
            prename=os.path.basename(f)
            ptags=['Preview','preview','Thumb','thumb']
            for tg in ptags:
                if tg in  prename and os.path.isfile(asset_dir+'/'+prename) and not prename.endswith('.rat'):
                    preview1=prename
                    break
    preview2=id+'_'+categories[0]+'_Preview.png'
    preview3=id+'_Preview.png'
    previews=[preview1,preview2,preview3]
    for p in previews:
        preview_file=asset_dir+'/'+p
        pfile=os.path.normpath(preview_file)
        if os.path.isfile(pfile):
            preview_file=pfile
            break
    if get_platform()=='Windows':
        preview_file=preview_file.replace('\'','/')
    preview_file=os.path.abspath(preview_file)
#####DisplaceVal Compute
    meta=jsondata['meta']
    length = ''
    width = ''
    height = ''
    for m in meta:
        if m["key"].lower() == "length" and length == "":
            length = m['value']

            length = float( length.replace('m','') )
        if m["key"].lower() == "width" and width == "":
            width = m['value']
            width = float( width.replace('m','') )

        if m["key"].lower() == "height" and height == "":
            height = m['value']
            height = float( height.replace('m','') )
            
    if type(length).__name__=='float' and type(width).__name__=='float' and type(height).__name__=='float':
        volume = length*width*height
        dval = remaprange(volume, 0.01, 20, 0.001, 0.3)
    elif type(height).__name__=='float':        
        dval = height
    else:
        dval=0.05
  ###MAPS LOAD AND FIND
    mapsjs=[]
    try:
        a=0
        for m in jsondata['maps']:
            if m['uri'] !='':
                a+=1
        if a >0:        
            mapsjs=jsondata['maps']
            tg=1
    except:
        pass
    if mapsjs==[]:
        mapsjs=jsondata['components']   
        tg=2
    mapsprm=[]
    map=''
    resparmval=node.parm('resolution').eval()
    for idx, val  in enumerate(mapsjs):
        mp="test"
        if tg==1:
            mp='tg'
            map=asset_dir+ver+"/"+val['uri']
            parmval=val['name']
        if tg==2:
            ress=val['uris'][0]['resolutions']
            try:
                for r in ress:
                    if r['resolution']==pres:
                        form=r['formats']
                        for ftype in form:
                            namef=ftype['uri']
                            fullname=asset_dir+ver+"/"+namef
                            if udimed==1 and udimcount>1:
                                tmpmap=replaceudim(fullname,out=0)
                                for i in range(udimcount):
                                    chkkko=0
                                    contex=udimfilename(tmpmap,i)
                                    if os.path.isfile(contex):
                                        chkkko=1
                                        break
                            else:
                                chkkko=os.path.exists(fullname)
                            if chkkko:
                                mp=namef
                                resparmval=str(int(pres.split('x')[0])/1024)+'K'
                                break
                                break
            except:
                pass
            if mp=="test":
                for r in ress:
                    try:        
                        form=r['formats']
                        for ftype in form:
                            namef=ftype['uri']
                            fullname=asset_dir+ver+"/"+namef
                            if udimed==1 and udimcount>1:
                                
                                tmpmap=replaceudim(fullname,out=0)
                                for i in range(udimcount):
                                    chkkko=0
                                    contex=udimfilename(tmpmap,i)
                                    if os.path.isfile(contex):
                                        chkkko=1
                                        break
                            else:
                                chkkko=os.path.exists(fullname)
                            if chkkko:
                                mp=namef
                                resparmval=str(int(r['resolution'].split('x')[0])/1024)+'K'
                                break
                                break
                    except:
                        pass
                            
                            
            
            map=asset_dir+ver+"/"+mp
            parmval=val['name']
        if mp!="test":
            map=os.path.normpath(map)
            if get_platform()=='Windows':
                map=map.replace('\'','/')
            nametx=""
            
            
            
            if udimed==1 and udimcount>1:
                chkky=0
                tmpmap=replaceudim(map,out=0)
                for i in range(udimcount):
                    contex=udimfilename(tmpmap,i)
                    if os.path.isfile(contex):
                        chkky=1
                        break
            else:
                chkky=os.path.isfile(map)
                
            if chkky: #and map.endswith('.jpg') or map.endswith('.exr'):
                ###########InterpretationName to Parm:
                if parmval=='AO':nametx='ao_texture'
                if parmval=='Albedo':nametx='albedo_texture'
                if parmval=='Bump':nametx='bump_texture'
                if parmval=='Cavity':nametx='ior_texture'
                if parmval=='Displacement':nametx='disp_texture'
                if parmval=='Gloss':nametx='reflect_texture'
                if parmval=='Specular':nametx='spec_texture'
                if parmval=='Metalness':nametx='metallic_texture'
                if parmval=='Normal':nametx='normal_texture'
                if parmval=='SSS':nametx='sss_texture'
                if parmval=='Opacity':nametx='opaccolor_texture'
                if parmval=='Translucency':nametx='trans_texture'
                if parmval=='Fuzz':nametx='fuzz_texture'
                if parmval=='Mask':nametx='mask_texture'
                if parmval=='Roughness':nametx='rough_texture'
                if parmval=='Normalbump':nametx='normalb_texture' 
                if parmval=='SSS':nametx='sss_texture'
                exr=map.replace('.jpg','.exr')
                if os.path.isfile(exr):
                    map=exr            
                mapsprm.append([nametx,map])
                
    ####Try Fuzz and Mask
    if len(mapsprm)>0 and mapsprm[0][1] is not None:
        names=['Albedo','AO','Bump','Displacement','Cavity','Gloss','Normal','Opacity']
        tempfile=mapsprm[0][1]
        for n in names:
            if n in tempfile:
                fuzz=tempfile.replace(n,'Fuzz')
                if os.path.isfile(fuzz):
                    mapsprm.append(['fuzz_texture',fuzz])
                elif os.path.isfile(fuzz.replace('.exr','.jpg')):
                    mapsprm.append(['fuzz_texture',fuzz.replace('.exr','.jpg')])
                    break
        for n in names:
            if n in tempfile:
                mask=tempfile.replace(n,'Mask')
                if os.path.isfile(mask):
                    mapsprm.append(['mask_texture',mask])
                elif os.path.isfile(mask.replace('.exr','.jpg')):
                    mapsprm.append(['fuzz_texture',mask.replace('.exr','.jpg')])
                    break
                
    glibpath=hou.getenv('ASSETS_LIBRARY')
    for m in mapsprm:
        try:
            tex=m[1]
            if node.parm('crat').eval()==1:
                if node.parm('resolution').eval()!=resparmval:
                    node.parm('resolution').set(resparmval)
                    if udimed==1 and udimcount>1:
                        m[1]=replaceudim(m[1],0)
                        tmp_tex=m[1]
                        for i in range(udimcount):
                            try:
                                contex=udimfilename(m[1],i)
                                tex=convertrat(node,[m[0],contex],1,acesval)
                            except:
                                pass
                        tex=replaceudim(udimfilename(tex,0))
                    else:
                        tex=convertrat(node,m,1,acesval)
                else:
                    if udimed==1 and udimcount>1:
                        m[1]=replaceudim(m[1],0)
                        tmp_tex=m[1]
                        for i in range(udimcount):
                            contex=udimfilename(m[1],i)
                            tex=convertrat(node,[m[0],contex],0,acesval)
                        tex=replaceudim(udimfilename(tex,0))
                    else:
                        tex=convertrat(node,m,0,acesval)
                        
                node.parm('resolution').set(resparmval)
            else:
                if udimed==1:
                    tex=replaceudim(udimfilename(tex,0))
                    
            if glibpath !=None and glibpath in tex:
                tex=jobreplace(tex,'ASSETS_LIBRARY')
            tex=jobreplace(tex) 
            node.parm(m[0]).set(tex)
        except:
            pass
    ####Set Parameters
    
    node.parm('prv_path').set(preview_file)
    node.parm('category').set(categories[0])
    node.parm('name').set(name)
    node.parm('dispTex_scale').set(dval)
############################################################################
def getsizejs(jsondata):
    sizeval=[0,0,0]
    x=0
    y=0
    z=0
    try:
        meta=jsondata['meta']
        for m in meta:
            if m['name']=='Length':
                x=float(m['value'].replace('m',''))
            if m['name']=='Width':
                z=float(m['value'].replace('m',''))
            if m['name']=='Height':
                y=float(m['value'].replace('m',''))            
    except:
        pass
    
    sizeval=[x,y,z]
    return sizeval

def loadmesh(node,jsondata,file):
    try:
        ver=jsondata['version'][len(jsondata['version'])-1]
    except:
        ver=""
    tags=jsondata['tags']
    categories=jsondata['categories']
    id=jsondata['id']
    asset_dir=os.path.dirname(os.path.normpath(file))
    if get_platform()=='Windows':
        asset_dir=asset_dir.replace('\'','/')
###NAME    
    geolist=[]
    lodlist=[]
    try:        
        meshlist=jsondata['meshes']
        for mesh in meshlist:
            if mesh['type']=='original':
                for m in mesh['uris']:
                    meshpath=asset_dir+'/'+m['uri']
                    if os.path.isfile(meshpath):
                        geolist.append('original'+'!!'+ meshpath)
            if mesh['type']=='lod':
                for m in mesh['uris']:
                    meshpath=asset_dir+'/'+m['uri']
                    if os.path.isfile(meshpath):
                       ldtype=meshpath.split(".")[-1]
                       lodnum=re.findall(r"[-+]?\d*\.?\d+|\d+",m['uri'])
                       if len(lodnum)>1:
                           lld=lodnum[-1]
                       else:
                           lld=lodnum[0]
                       lodlist.append(('lod_'+lld,meshpath))
    except:
        pass   
    if len(lodlist)==0:
        try:
            meshlist=jsondata['models']
            for m in meshlist:
                if m['type']=='original':
                    meshpath=asset_dir+'/'+m['uri']
                    if os.path.isfile(meshpath):
                        geolist.append('original'+'!!'+ meshpath)
                if m['type']=='lod':
                    meshpath=asset_dir+'/'+m['uri']
                    lodname=((m['uri'].split('/')[-1]).split('.')[0]).lower()
                    if os.path.isfile(meshpath):
                        ldtype=(meshpath.split(".")[-1]).lower()
                        lodnum=re.findall(r"[-+]?\d*\.?\d+|\d+",m['uri'])
                        if len(lodnum)>1:
                            lld=lodnum[-1]
                        else:
                            lld=lodnum[0]
                        if lodname !="":
                            lodnm=lodname
                        else:
                            lodnm='lod_'+lld
                        lodlist.append((lodnm,meshpath))
        
        except:
            pass
        
    lodlist=sorted(lodlist, key=lambda lod: lod[0])
    newlodlist=[]
    for l in lodlist:
        newlodlist.append(l[0]+'!!'+l[1]) 
    fulllistgeo= "*?*".join(newlodlist+geolist)
    if node.userData('geometry') !=None:
        node.destroyUserData('geometry') 
    node.setUserData('geometry',fulllistgeo)
    
    assetsize=getsizejs(jsondata)
    
    if assetsize[0]+assetsize[1]+assetsize[2]>0:
        try:
            node.parm('sizex').set(assetsize[0])
            node.parm('sizey').set(assetsize[1])
            node.parm('sizez').set(assetsize[2])
        except:
            pass
    else:
        try:
            node.parm('sizex').set(0)
            node.parm('sizey').set(0)
            node.parm('sizez').set(0)
        except:
            pass        
        
        
####################################################################
def refreshtex(node=''):
    try:
        hou.hscript("glcache -c")
        hou.hscript("texcache -c")
        hou.hscript('opupdate')
        viewer = toolutils.sceneViewer()
        viewport = viewer.curViewport()
        viewport.settings().updateMaterials()
        viewport.draw()
        #rnode=node.path()+'/output0'
        #rnode.setCurrent(1)
        #node.setCurrent(1)
    except:
        pass

def refresh(node):
    hou.node("/").setSelected(1)
    hou.node("/").setSelected(0)
    node.setSelected(1)
###Load Asset
def loadasset(node):
    tmpstick=0
    if node.parm('stick').eval()==1:
        tmpstick=1
        stickprev(node,0)
    
    boolsel=node.isSelected()
    node.parm('lods').set('')
    node.parm('geometry').set('')
    jsonpath=''
    try:
        jsonpath=node.parm('input_data').eval()
    except:
        pass
    if jsonpath == '':
        jsonparm=node.parm('json').eval()
    else:
        jsonparm=jsonpath
        node.parm('json').set(jsonpath)
    cleannodeparm(node)
    if os.path.isfile(jsonparm):
        if node.userData('geometry') !=None:
            node.destroyUserData('geometry')
        node.parm('lods').set('')
        opfile=open(jsonparm, 'r')
        jsondata=json.load(opfile)
        load3djson(node,jsondata,jsonparm)
        ###pack for geo
        if categorytype(node)==0:
            loadmesh(node,jsondata,jsonparm)
            varscheck(node)
            lodslist(node)
            lodset(node)
            packedfromgeo(node)
       ###pack for atlas    
        elif categorytype(node)==1:
            packedfromgeo(node)
            
        opfile.close()
        

    nodename=node.parm('name').eval()
    nodename=nodename.replace('.','_')
    if nodename !="":
        node.setName(nodename,unique_name=True)
    
    shader_parm=node.parm('setcustom_shader').eval()        
    shader=hou.node(shader_parm)    
    if node.parm('converted').eval()!=0 and shader is None:
        node.parm('convertshader').pressButton()
    if boolsel==1:
        refresh(node)
    nodeprop(node)
    if tmpstick==1:
        stickprev(node,1)
    refreshtex(node)
    
#########Convert Workflow


def convertWF(node):
    workflow=hou.getenv("MSWORKFLOW")
    shadername=node.parm('shader').eval()
    if workflow is None:
        workflow="Mantra"
    builders={'renderman':'pxrmaterialbuilder','arnold':'arnold_materialbuilder',
'vray':'vray_vop_material','redshift':'redshift_vopnet'}        
    name=node.parm('name').eval() #name
    nd=node.parm('matn').eval() #root of shader
    ops=conf.conformlist()[0] 
    properties=ops[node.parm('shader').eval()] #properties
    matnet=node.node(nd)
    materialnode=hou.node(node.parm('setcustom_shader').eval()) #shader
    material = materialnode
    if workflow.lower() == 'mantra' or workflow.lower() == 'redshift':
        if matnet is not None:
            if materialnode is None:
                materialnode = matnet.createNode(properties['node'],name)
                materialnode.moveToGoodPosition()
            material = materialnode
    else:
        if materialnode is None:
            materialnode = matnet.createNode(builders[workflow.lower()],name)
            materialnode.moveToGoodPosition()
        else:
            materialnode.setName(name , unique_name=True)
            
        if workflow.lower() == 'arnold':
            outputnode=hou.node(materialnode.path()+'/OUT_material')
            diffuse=hou.node(materialnode.path()+'/'+name)
            if diffuse is None:
                diffuse=materialnode.createNode(properties['node'],name)
                diffuse.setPosition([(outputnode.position()[0]-3),outputnode.position()[1]])
            outputnode.setInput(0,diffuse,0) 
            outputnode.setInput(1,diffuse,1)             
            material = diffuse       

                

    conv.copyvalues(node,shadername,material)
    node.parm('converted').set(1)
    refreshtex(node)
        

        
#####################################packed:
#####################################################
def packedfromgeo(node):
    if categorytype(node)!=2:
        convert=node.parm('execute')
        usepdisk=node.parm('pdisk')
        reloadprm=node.parm('reload')
        pythonnode=hou.node(node.path()+'/python1')
        
        if convert!=None and usepdisk!=None and reloadprm!=None:
            if usepdisk.eval()==1:
                try:
                    pfile=hou.node(node.path()+'/out_packed').parm('sopoutput').eval()
                    if not os.path.isfile(pfile):
                        convert.pressButton()
                        
                    reloadprm.pressButton()
                    pythonnode.cook(1)    
                except:
                    pass
                
########Connect
def connect_chng():
    conn.run()
    
########Conform
def shaderoplist(node):
    opmenu=[]
    try:
        ops=conf.conformlist()[0]
        for key in ops.keys():
            op=str(key)
            opmenu += [op, op]
    except:
        pass
#    if len(ops.keys())>0:
#        node.parm('shader').set(str((ops.keys())[0]))
    return opmenu
    
def setmenustart(node):
    try:
        ops=(conf.conformlist()[0]).keys()
        default=conf.conformlist()[1]
        
        if len(ops)>0:
            if default in ops:
                node.parm('shader').set(str(default))
            else:
                node.parm('shader').set(str(ops[0]))
    except:
        pass
#####################
