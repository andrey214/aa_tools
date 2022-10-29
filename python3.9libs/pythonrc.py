import hou,assetloaderlib
if hou.isUIAvailable():
	try:
		auto=hou.getenv("MS_AUTOCONNECT")
		if int(auto)==1:
			assetloaderlib.hda_core.init_connect()
	except:
		pass