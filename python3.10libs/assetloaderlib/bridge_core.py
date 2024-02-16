from __future__ import print_function
import os, json, sys, socket, time, re, hou
from .importer import importerSetup

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    try:
        from PySide.QtGui import *
        from PySide.QtCore import *
    except:
        try:
            from PyQt5.QtGui import *
            from PyQ5.QtCore import *
            from PyQ5.QtWidgets import *
        except:
            try:
                from PyQt4.QtGui import *
                from PyQ4.QtCore import *
            except:
                pass

def hostnm():
    return socket.gethostname()
    
def connectsettings():
    setting=hou.getenv('ms_connect')
    if setting!=None:
        arrset=setting.split(',')
        host=arrset[0]
        port=int(arrset[1])
    else:
        host= 'localhost' ###str(hostnm())
        port=24981
    return [host,port]
        
    
class PortMonitor(QThread):

    bridge_call = Signal()
    Instance = []

    def __init__(self, importer):
        QThread.__init__(self)
        self.TotalData = b""
        self.Importer = importer
        PortMonitor.Instance=[self]

    def refresh(self, importer):
        Instance = []
        
    def __del__(self):
        self.quit()
        self.wait()

    def stop(self):
        self.terminate()

    def run(self):
        time.sleep(0.025)
        setting=connectsettings()
        try:
            socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_.bind((setting[0], setting[1]))
            while True:
                socket_.listen(5)
                client, address = socket_.accept()
                data = ""
                data = client.recv(4096*2)
                
                if data != "":
                    self.TotalData = b""
                    self.TotalData += data
                    while True:
                        data = client.recv(4096*2)
                        if data : 
                            self.TotalData += data
                        else : break
                    time.sleep(0.05)
                    self.bridge_call.emit()
                    time.sleep(0.05)
        except:
            pass
            
    def restart(self):
        self.terminate()
        Instance = []
        
    def InitializeImporter(self):
        try:
            json_array = json.loads(self.TotalData)
            for asset_ in json_array:
                self = importerSetup.Identifier
                self.set_Asset_Data(asset_)
                self.importData()
        except:
            pass
                  

def initbridgeconnect(rs=0):
    _importerSetup_ = importerSetup()
    bridge_monitor = PortMonitor(_importerSetup_)
    bridge_monitor.bridge_call.connect(bridge_monitor.InitializeImporter)
    bridge_monitor.start()
    return bridge_monitor
