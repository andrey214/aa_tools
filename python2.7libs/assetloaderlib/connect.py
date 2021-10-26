import json,os,hou
import bridge_core as bc
import __future__ 
from PySide2 import  QtCore, QtGui, QtWidgets


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)



class Ui_MainWindow(QtWidgets.QDialog):
    Instance = []
    Settings = [0, 0, 0]
    Thread_Monitor = None
    
    def __init__(self,parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        MainWindow = self
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window) 
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(310, 75)
        MainWindow.setMinimumSize(QtCore.QSize(310, 75))
        MainWindow.setMaximumSize(QtCore.QSize(310, 75))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.changebtn = QtWidgets.QPushButton(self.centralwidget)
        self.changebtn.setGeometry(QtCore.QRect(220, 10, 81, 51))
        self.changebtn.setMinimumSize(QtCore.QSize(81, 51))
        self.changebtn.setMaximumSize(QtCore.QSize(81, 51))
        self.changebtn.setAutoDefault(False)
        self.changebtn.setDefault(False)
        self.changebtn.setFlat(False)
        self.changebtn.setObjectName(_fromUtf8("changebtn"))
        self.portlb = QtWidgets.QLabel(self.centralwidget)
        self.portlb.setGeometry(QtCore.QRect(10, 40, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.portlb.setFont(font)
        self.portlb.setObjectName(_fromUtf8("portlb"))
        self.hostln = QtWidgets.QLineEdit(self.centralwidget)
        self.hostln.setGeometry(QtCore.QRect(50, 10, 161, 20))
        self.hostln.setMinimumSize(QtCore.QSize(161, 20))
        self.hostln.setMaximumSize(QtCore.QSize(161, 20))
        self.hostln.setObjectName(_fromUtf8("hostln"))
        
        setting=bc.connectsettings() #####LOAD SETTINGS
        
        self.hostln.setText(setting[0]) 
        self.portln = QtWidgets.QLineEdit(self.centralwidget)
        self.portln.setGeometry(QtCore.QRect(50, 40, 161, 20))
        self.portln.setMinimumSize(QtCore.QSize(161, 20))
        self.portln.setMaximumSize(QtCore.QSize(161, 20))
        self.portln.setObjectName(_fromUtf8("portln"))
        port=str(setting[1])
        self.portln.setText(port)
        
        self.hostlb = QtWidgets.QLabel(self.centralwidget)
        self.hostlb.setGeometry(QtCore.QRect(10, 10, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.hostlb.setFont(font)
        self.hostlb.setObjectName(_fromUtf8("hostlb"))



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.changebtn.clicked.connect(self.changefn)
        
    def changefn(self):
        host=self.hostln.text()
        port=self.portln.text()
        hou.putenv('ms_connect',(host+','+port))
        bc.initbridgeconnect()
        self.close()
        
    def retranslateUi(self, MainWindow):
        self.setWindowTitle(_translate("MainWindow", "Connect Settings", None))
        self.changebtn.setText(_translate("MainWindow", "Change", None))
        self.portlb.setText(_translate("MainWindow", "port:", None))
        self.hostlb.setText(_translate("MainWindow", "host:", None))
        
def run():
    dialog=Ui_MainWindow()
    dialog.show()
