prismmod=None
import hou
try:
    import PrismInit as prismmod
except:
    pass
    
def prismcollectpath(path=''):
    res=path
    if prismmod is not None:
        asset=hou.getenv('PRISM_ASSET')
        shot=hou.getenv('PRISM_SHOT')
        if asset is None:
            res='$JOB'+'/03_Workflow/Shots/'+'$PRISM_SHOT/Export/'
            res+="megascans/"+"`chs("+'"category"'+")`"+"/`chs("+'"name"'+")`"
        else:
            res='$JOB'+'/03_Workflow/Assets/'+'$PRISM_ASSET/Export/'
            res+="megascans/"+"`chs("+'"category"'+")`"+"/`chs("+'"name"'+")`"
            
        
    return res
    