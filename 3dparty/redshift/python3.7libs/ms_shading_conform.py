def conformlist():
    default='rs_shader'
    parmsdict = {
        'rs_shader': {
                'node': 'rs_megascan_shader::1.0',
                'maps': ['albedo', 'ao', 'bump', 'cavity', 'displacement', 'gloss', 'fuzz', 'mask', 'metalness', 'normal', 'normalbump', 'opacity', 'roughness', 'translucency'],
                'values': ['truedisplace', 'disp_scale', 'rough_scale', 'reflect_scale',  'use_opacity'],
                'albedo': ['basecolor_texture','albedo_texture','ms_diffuse'],
                'ao' : ['ao_texture','ao_texture','ms_ao'],
                'bump' : ['bump_tex','bump_texture','ms_bump'],
                'cavity' : ['ior_tex','ior_texture','ms_ior'],
                'displacement' : ['disp_tex','disp_texture','ms_disp'],
                'gloss' : ['reflect_tex','reflect_texture','ms_reflect'],
                'fuzz' : ['fuzz_texture','fuzz_texture','ms_fuss'],
                'mask' : ['mask_texture','mask_texture','ms_mask'],
                'metalness': ['metallic_texture','metallic_texture','ms_metal'],
                'normal' : ['norm_tex','normal_texture','ms_normal'],
                'normalbump' : ['normalb_texture','normalb_texture','ms_normalbump'],
                'opacity' : ['opac_tex','opaccolor_texture','ms_opac'],
                'roughness': ['rough_tex','rough_texture','ms_rough'],               
                'translucency' : ['trans_tex','trans_texture','ms_trans'],
                'truedisplace' :['vm_truedisplace','use_true','ms_usedisp'],
                'disp_scale' : ['disp_scale','dispTex_scale','ms_dscale'],
                'rough_scale' : ['refl_rough','rough', 'ms_rscale'],
                'reflect_scale' : ['refl_scale','reflect_scale', 'ms_reflectscale'],
                'use_opacity' : ['use_opacity','use_opacity','ms_opacval']
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
            }
            
    }
    return [parmsdict,default]
    

