from __future__ import print_function
import assetloaderlib as asll
import os, json, sys, re, hou, numpy
from . import bridge_functions as mrpf

class importerSetup():
    #########################################################################################

    Identifier = None
    def __init__(self,):
        self._path_ = os.path.dirname(asll.__file__).replace("\\", "/")
        importerSetup.Identifier = self

    def set_Asset_Data(self, json_data):
        self.json_data = json_data
        try:
            self.resolution = self.json_data['resolution']
        except:
            pass
        if self.resolution!=None:
            self.assetres=self.resolution
        else:
            self.assetres='2K'
        

        self.TexturesList = []
        self._textures_ = ["albedo", "displacement", "cavity", "normal", "roughness", "specular", "normalbump",
                               "ao", "opacity", "translucency", "gloss", "metalness", "bump", "fuzz", "mask"]
        
        self.preview_file = self.json_data["previewImage"]
        self.json = self.json_data["path"]+"/"+self.json_data["id"]+".json"
        if sys.platform=='win32':
            self.json=self.json.replace('\\','/')

        if "name" in list(self.json_data.keys()):
            self.Name = self.json_data["name"].replace(" ", "_")

        else:
            self.Name = os.path.basename(self.json_data["path"]).replace(" ", "_")

            if len(self.Name.split("_")) >= 2:
                self.Name = "_".join(self.Name.split("_")[:-1])

        self.materialName = self.Name + '_' + self.json_data["id"]
        self.materialName = re.sub('[^A-Za-z0-9]+', '_', self.materialName)
#############################################################################################
    def importData(self):
        js=self.json
        try:
            if js!=None:
                material=mrpf.assetnode(self.materialName,js,self.assetres)
                return material.path()
        except:
            pass








