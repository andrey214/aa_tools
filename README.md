# aaTools

My various assets for Houdini


1. "ms_asset_loader" - Custom importer assets from Quixel Bridge
2. "asset_placer" - Tool for placment sop geometry on viewport

(3dparty folder contait shaders for arnold and redshift renderers for use with ms_asset_loader)

# Example videos:
1. ms_asset_loader (surfaces)

[![Watch the video](https://github.com/andrey214/aa_tools/raw/main/imgs/asset_loader_01.jpg)](https://vimeo.com/638435887)

2. ms_asset_loader (3d assets)

[![Watch the video](https://github.com/andrey214/aa_tools/raw/main/imgs/asset_loader_02.jpg)](https://vimeo.com/638435845)

3. ms_asset_loader_lop

[![Watch the video](https://github.com/andrey214/aa_tools/raw/main/imgs/asset_loader_03.jpg)](https://vimeo.com/765291814)

4. asset_placer

[![Watch the video](https://github.com/andrey214/aa_tools/raw/main/imgs/asset_placer_01.jpg)](https://vimeo.com/638435766)


# Installation:

1. Edit package jsonfile (root/packages/aatools.json). Set "hpath" to folder where you cloned repository.
"QMEGASCAN_LIB" is path to bridge application
2. Copy edited json to "packages" folder in home Houdini directory.($HOUDINI_USER_PREF_DIR/packages)

Optional Variables:
"MS_AUTOSHADING" enables automatic shader creation when loading an asset.
"MS_AUTOCONNECT" enables automatic connection to the Bridge when the program starts.
"MS_COLLECT" sets the path to the directory for the asset collection.