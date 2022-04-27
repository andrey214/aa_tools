def conformlist():
    default='rs_shader'
    parmsdict = {
        'rs_shader': {
                'node': 'rs_megascan_shader',
                'maps': ['albedo', 'ao', 'bump', 'cavity', 'displacement', 'gloss', 'fuzz', 'mask', 'metalness', 'normal', 'normalbump', 'opacity', 'roughness', 'translucency'],
                'values': ['truedisplace', 'disp_scale', 'rough_scale', 'reflect_scale',  'use_opacity'],
                'albedo': ['ms_diffuse','albedo_texture','ms_diffuse'],
                'ao' : ['ms_ao','ao_texture','ms_ao'],
                'bump' : ['ms_bump','bump_texture','ms_bump'],
                'cavity' : ['ms_ior','ior_texture','ms_ior'],
                'displacement' : ['ms_disp','disp_texture','ms_disp'],
                'gloss' : ['ms_reflect','reflect_texture','ms_reflect'],
                'fuzz' : ['ms_fuss','fuzz_texture','ms_fuss'],
                'mask' : ['ms_mask','mask_texture','ms_mask'],
                'metalness': ['ms_metal','metallic_texture','ms_metal'],
                'normal' : ['ms_normal','normal_texture','ms_normal'],
                'normalbump' : ['ms_normalbump','normalb_texture','ms_normalbump'],
                'opacity' : ['ms_opac','opaccolor_texture','ms_opac'],
                'roughness': ['ms_rough','rough_texture','ms_rough'],               
                'translucency' : ['ms_trans','trans_texture','ms_trans'],
                'truedisplace' :['ms_usedisp','use_true','ms_usedisp'],
                'disp_scale' : ['ms_dscale','dispTex_scale','ms_dscale'],
                'rough_scale' : ['ms_rscale','rough', 'ms_rscale'],
                'reflect_scale' : ['ms_reflectscale','reflect_scale', 'ms_reflectscale'],
                'use_opacity' : ['ms_opacval','use_opacity','ms_opacval']
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
    os.environ.putenv("MSWORKFLOW","redshift")
    os.environ.putenv("RATPROCESS",'0')
addenv()
