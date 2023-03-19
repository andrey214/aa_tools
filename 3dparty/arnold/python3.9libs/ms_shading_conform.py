def conformlist():
    default='arnold_shader'
    parmsdict = {
            'arnold_shader': {
                'node': 'ms_arnold_shader',
                'maps': ['albedo', 'cavity', 'gloss', 'metalness', 'normal', 'opacity', 'roughness' ,'displacement'],
                'values': ['disp_scale', 'rough_scale', 'reflect_scale'],
                'albedo': ['colorMap','albedo_texture','ms_diffuse'],
                'cavity' : ['iorMap','ior_texture','ms_ior'],
                #'spec' : ['glossMap','spec_texture','ms_spec'],
                'gloss' : ['specularMap','reflect_texture','ms_reflect'],
                #'metalness': ['metallic_texture','metallic_texture','ms_metal'],
                'normal' : ['normalMap','normal_texture','ms_normal'],
                'displacement' : ['dispMap','disp_texture','ms_disp'],
                #'normalbump' : ['normalb_texture','normalb_texture','ms_normalbump'],
                'opacity' : ['opacityMap','opaccolor_texture','ms_opac'],
                'roughness': ['roughMap','rough_texture','ms_rough'],               
                #'translucency' : ['trans_texture','trans_texture','ms_trans'],
                #'truedisplace' :['vm_truedisplace','use_true','ms_usedisp'],
                'disp_scale' : ['dispScale','dispTex_scale','ms_dscale'],
                'rough_scale' : ['rough','rough', 'ms_rscale'],
                'reflect_scale' : ['specularr','reflect_scale', 'ms_reflectscale'],
                #'use_opacity' : ['use_opacity','use_opacity','ms_opacval']
  ############## type  : [parm name on shader , parm name on assetloader , attribute name]              
            },
        'ms_simple': {
                'node': 'megascans_shader_simple::1.1',
                'maps': ['albedo', 'ao', 'bump', 'cavity', 'displacement', 'gloss', 'fuzz', 'mask', 'metalness', 'normal', 'normalbump', 'opacity', 'roughness', 'translucency'],
                'values': ['truedisplace', 'disp_scale', 'rough_scale', 'reflect_scale',  'use_opacity'],
                'albedo': ['albedo_texture','albedo_texture','ms_diffuse'],
                'ao' : ['ao_texture','ao_texture','ms_ao'],
                'bump' : ['bump_texture','bump_texture','ms_bump'],
                'cavity' : ['ior_texture','ior_texture','ms_ior'],
                'displacement' : ['disp_texture','disp_texture','ms_disp'],
                'gloss' : ['reflect_texture','reflect_texture','ms_reflect'],
                'fuzz' : ['fuzz_texture','fuzz_texture','ms_fuss'],
                'mask' : ['mask_texture','mask_texture','ms_mask'],
                'metalness': ['metallic_texture','metallic_texture','ms_metal'],
                'normal' : ['normal_texture','normal_texture','ms_normal'],
                'normalbump' : ['normalb_texture','normalb_texture','ms_normalbump'],
                'opacity' : ['opaccolor_texture','opaccolor_texture','ms_opac'],
                'roughness': ['rough_texture','rough_texture','ms_rough'],               
                'translucency' : ['trans_texture','trans_texture','ms_trans'],
                'truedisplace' :['vm_truedisplace','use_true','ms_usedisp'],
                'disp_scale' : ['dispTex_scale','dispTex_scale','ms_dscale'],
                'rough_scale' : ['rough','rough', 'ms_rscale'],
                'reflect_scale' : ['reflect_scale','reflect_scale', 'ms_reflectscale'],
                'use_opacity' : ['use_opacity','use_opacity','ms_opacval']
  ############## type  : [parm name on shader , parm name on assetloader , attribute name]              
            },
        'asset_textures': {
                'node': 'asset_textures::1.0',
                'maps': ['albedo', 'ao', 'bump', 'cavity', 'displacement', 'gloss', 'specular', 'fuzz', 'mask', 'metalness', 'normal', 'normalbump', 'opacity', 'roughness', 'translucency'],
                'values': [],
                'albedo': ['albedo_texture','albedo_texture','ms_diffuse'],
                'ao' : ['ao_texture','ao_texture','ms_ao'],
                'bump' : ['bump_texture','bump_texture','ms_bump'],
                'cavity' : ['ior_texture','ior_texture','ms_ior'],
                'displacement' : ['disp_texture','disp_texture','ms_disp'],
                'gloss' : ['reflect_texture','reflect_texture','ms_reflect'],
                'specular' : ['spec_texture','spec_texture','ms_spec'],
                'fuzz' : ['fuzz_texture','fuzz_texture','ms_fuss'],
                'mask' : ['mask_texture','mask_texture','ms_mask'],
                'metalness': ['metallic_texture','metallic_texture','ms_metal'],
                'normal' : ['normal_texture','normal_texture','ms_normal'],
                'normalbump' : ['normalb_texture','normalb_texture','ms_normalbump'],
                'opacity' : ['opaccolor_texture','opaccolor_texture','ms_opac'],
                'roughness': ['rough_texture','rough_texture','ms_rough'],               
                'translucency' : ['trans_texture','trans_texture','ms_trans']
            },

  ############## type  : [parm name on shader , parm name on assetloader , attribute name]        
         'ms_bombing': {
                'node': 'megascans_shader_bombing::1.1',
                'maps': ['albedo', 'ao', 'bump', 'cavity', 'displacement', 'gloss', 'fuzz', 'mask', 'metalness', 'normal', 'normalbump', 'opacity', 'roughness', 'translucency'],
                'values': ['truedisplace', 'disp_scale', 'rough_scale', 'reflect_scale',  'use_opacity'],
                'albedo': ['albedo_texture','albedo_texture','ms_diffuse'],
                'ao' : ['ao_texture','ao_texture','ms_ao'],
                'bump' : ['bump_texture','bump_texture','ms_bump'],
                'cavity' : ['ior_texture','ior_texture','ms_ior'],
                'displacement' : ['disp_texture','disp_texture','ms_disp'],
                'gloss' : ['reflect_texture','reflect_texture','ms_reflect'],
                'fuzz' : ['fuzz_texture','fuzz_texture','ms_fuss'],
                'mask' : ['mask_texture','mask_texture','ms_mask'],
                'metalness': ['metallic_texture','metallic_texture','ms_metal'],
                'normal' : ['normal_texture','normal_texture','ms_normal'],
                'normalbump' : ['normalb_texture','normalb_texture','ms_normalbump'],
                'opacity' : ['opaccolor_texture','opaccolor_texture','ms_opac'],
                'roughness': ['rough_texture','rough_texture','ms_rough'],               
                'translucency' : ['trans_texture','trans_texture','ms_trans'],
                'truedisplace' :['vm_truedisplace','use_true','ms_usedisp'],
                'disp_scale' : ['dispTex_scale','dispTex_scale','ms_dscale'],
                'rough_scale' : ['rough','rough', 'ms_rscale'],
                'reflect_scale' : ['reflect_scale','reflect_scale', 'ms_reflectscale'],
                'use_opacity' : ['use_opacity','use_opacity','ms_opacval']            
            },
        'ms_bombing_spec': {
                'node': 'megascans_shader_bombing::1.0',
                'maps': ['albedo', 'ao', 'bump', 'cavity', 'displacement', 'gloss', 'fuzz', 'mask', 'metalness', 'normal', 'normalbump', 'opacity', 'roughness', 'translucency'],
                'values': ['truedisplace', 'disp_scale', 'rough_scale', 'reflect_scale',  'use_opacity'],
                'albedo': ['albedo_texture','albedo_texture','ms_diffuse'],
                'ao' : ['ao_texture','ao_texture','ms_ao'],
                'bump' : ['bump_texture','bump_texture','ms_bump'],
                'cavity' : ['spec_texture','ior_texture','ms_ior'],
                'displacement' : ['disp_texture','disp_texture','ms_disp'],
                'gloss' : ['reflect_texture','reflect_texture','ms_reflect'],
                'fuzz' : ['fuzz_texture','fuzz_texture','ms_fuss'],
                'mask' : ['mask_texture','mask_texture','ms_mask'],
                'metalness': ['metallic_texture','metallic_texture','ms_metal'],
                'normal' : ['normal_texture','normal_texture','ms_normal'],
                'normalbump' : ['normalb_texture','normalb_texture','ms_normalbump'],
                'opacity' : ['opaccolor_texture','opaccolor_texture','ms_opac'],
                'roughness': ['rough_texture','rough_texture','ms_rough'],               
                'translucency' : ['trans_texture','trans_texture','ms_trans'],
                'truedisplace' :['vm_truedisplace','use_true','ms_usedisp'],
                'disp_scale' : ['dispTex_scale','dispTex_scale','ms_dscale'],
                'rough_scale' : ['rough','rough', 'ms_rscale'],
                'reflect_scale' : ['reflect_scale','reflect_scale', 'ms_reflectscale'],
                'use_opacity' : ['use_opacity','use_opacity','ms_opacval']
  ############## type  : [parm name on shader , parm name on assetloader , attribute name]              
            }
            
    }
    return [parmsdict,default]
    
def addenv():
    import os
    os.putenv("MSWORKFLOW","arnold")
    os.putenv("RATPROCESS",'0')
addenv()
