from ticsummary.ui import ConnectionConfigurationDialog
from ticsummary.ui.CountDetectorsWidget import CountScintillators
from ticsummary.ui.OpenSqlDataDialog import OpenSQLData
from ticsummary.ui.ProfilePlotWidget import ProfilePlot
from ticsummary.ui.ViewGraphicsDialog import ViewGraphicsDialog
from ticsummary.ui.WaveDetectorsWidget import WaveScintillators
from ticsummary.ui.ProfileBeamDock import ProfileBeamDock

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import numpy as np
from enum import Enum

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 672)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBoxType = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.comboBoxType.setFont(font)
        self.comboBoxType.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.comboBoxType.setObjectName("comboBoxType")
        self.horizontalLayout.addWidget(self.comboBoxType)
        self.comboBoxListData = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.comboBoxListData.setFont(font)
        self.comboBoxListData.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.comboBoxListData.setEditable(True)
        self.comboBoxListData.setObjectName("comboBoxListData")
        self.horizontalLayout.addWidget(self.comboBoxListData)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayoutGraphics = QtWidgets.QHBoxLayout()
        self.horizontalLayoutGraphics.setObjectName("horizontalLayoutGraphics")
        self.verticalLayout.addLayout(self.horizontalLayoutGraphics)
        self.progressBarTask = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBarTask.setProperty("value", 24)
        self.progressBarTask.setObjectName("progressBarTask")
        self.verticalLayout.addWidget(self.progressBarTask)
        self.horizontalLayout_Information = QtWidgets.QHBoxLayout()
        self.horizontalLayout_Information.setObjectName("horizontalLayout_Information")
        self.verticalLayout.addLayout(self.horizontalLayout_Information)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 34))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.menuFile.setFont(font)
        self.menuFile.setObjectName("menuFile")
        self.menuOpen = QtWidgets.QMenu(self.menuFile)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.menuOpen.setFont(font)
        self.menuOpen.setObjectName("menuOpen")
        self.menuExport = QtWidgets.QMenu(self.menuFile)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.menuExport.setFont(font)
        self.menuExport.setObjectName("menuExport")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.menuEdit.setFont(font)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionFrom_sql_database = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.actionFrom_sql_database.setFont(font)
        self.actionFrom_sql_database.setObjectName("actionFrom_sql_database")
        self.actionmeasured_data_to_csv = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.actionmeasured_data_to_csv.setFont(font)
        self.actionmeasured_data_to_csv.setObjectName("actionmeasured_data_to_csv")
        self.actionConnectionSqlDatabase = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.actionConnectionSqlDatabase.setFont(font)
        self.actionConnectionSqlDatabase.setObjectName("actionConnectionSqlDatabase")
        self.actionPlots = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.actionPlots.setFont(font)
        self.actionPlots.setObjectName("actionPlots")
        self.actionReset_position = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.actionReset_position.setFont(font)
        self.actionReset_position.setObjectName("actionReset_position")
        self.menuOpen.addAction(self.actionFrom_sql_database)
        self.menuExport.addAction(self.actionmeasured_data_to_csv)
        self.menuFile.addAction(self.menuOpen.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menuEdit.addAction(self.actionConnectionSqlDatabase)
        self.menuView.addAction(self.actionPlots)
        self.menuView.addAction(self.actionReset_position)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TICSummary"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuOpen.setTitle(_translate("MainWindow", "Open.."))
        self.menuExport.setTitle(_translate("MainWindow", "Export.."))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionFrom_sql_database.setText(_translate("MainWindow", "from sql database"))
        self.actionmeasured_data_to_csv.setText(_translate("MainWindow", "measured data to csv"))
        self.actionConnectionSqlDatabase.setText(_translate("MainWindow", "Connection to sql database"))
        self.actionPlots.setText(_translate("MainWindow", "Plots"))
        self.actionReset_position.setText(_translate("MainWindow", "Reset position"))


class DockAreaWithUncloseableDocks(pg.dockarea.DockArea):
    def makeContainer(self, typ):
        new = super(DockAreaWithUncloseableDocks, self).makeContainer(typ)
        new.setChildrenCollapsible(False)
        return new

class ModeInterface(Enum):
    DEFFAULT            = (False)
    DBISCONNECTED       = (True)
    
    def __init__(self,chartEnabled):
        self.chartEnabled = chartEnabled


class MainWindow(QtWidgets.QMainWindow, QtCore.QObject):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionPlots.triggered.connect(self.__openViewGraphics__)
        self.ui.actionReset_position.triggered.connect(lambda : self.dockAreaChart.restoreState(self.dockAreaState))

        self.dockAreaChart = DockAreaWithUncloseableDocks()

        self.profileDockX1 = ProfileBeamDock(name="profileX1", size=(1,1))
        self.profileDockX2 = ProfileBeamDock(name="profileX2", size=(1,1))
        self.profileDockY1 = ProfileBeamDock(name="profileY1", size=(1,1))
        self.profileDockY2 = ProfileBeamDock(name="profileY2", size=(1,1))

        self.dockAreaChart.addDock(self.profileDockX1)
        self.dockAreaChart.addDock(self.profileDockX2)
        self.dockAreaChart.addDock(self.profileDockY1)
        self.dockAreaChart.addDock(self.profileDockY2)
        self.ui.horizontalLayoutGraphics.addWidget(self.dockAreaChart)
        
        self.dockAreaState = self.dockAreaChart.saveState()
        
        self.ui.comboBoxType.addItem("Manual")
        self.ui.comboBoxType.addItem("Online")
        self.ui.comboBoxType.setCurrentIndex(0)
        
        self.sigSetRealTimeMode = QtCore.pyqtSignal()
        self.sigUnsetRealTimeMode = QtCore.pyqtSignal()
        self.realTimeModeOn = False

        self.setMode(ModeInterface.DEFFAULT)
    def setInfinityProgress(self, mode:bool):
        self.ui.progressBarTask.setMaximum(0 if mode else 100)
        self.ui.progressBarTask.setMinimum(0)
        self.ui.progressBarTask.setValue(-1 if mode else 0)
        
    def keyPressEvent(self,event):
        keyToFunc = {
            Qt.Key.Key_Right:self.nextData,
            Qt.Key.Key_Left:self.prevData
        }
        
        try:
            keyToFunc[event.key()]()
        except KeyError as e:
            # можно также присвоить значение по умолчанию вместо бросания исключения
            print('Undefined unit: {}'.format(e.args[0]))
    
    def nextData(self):
        if self.ui.comboBoxListData.currentIndex() < self.ui.comboBoxListData.count()-1:
            self.ui.comboBoxListData.setCurrentIndex(self.ui.comboBoxListData.currentIndex() + 1)
    
    def prevData(self):
        if self.ui.comboBoxListData.currentIndex() > 0:
            self.ui.comboBoxListData.setCurrentIndex(self.ui.comboBoxListData.currentIndex() - 1)
        
    def setMode(self, mode:ModeInterface):
        self.dockAreaChart.setEnabled(mode.chartEnabled)

    def connectSignalOpenConnectionConfiguration(self, signal):
        self.ui.actionConnectionSqlDatabase.triggered.connect(signal)

    def connectSignalOpenDataFromSqlDatabase(self, signal):
        self.ui.actionFrom_sql_database.triggered.connect(signal)

    def setIndexListData(self,data):
        self.ui.comboBoxListData.addItems(data)
    
    def setData(self,dataX1,scaleTimeX1,dataY1,scaleTimeY1,dataX2,scaleTimeX2,dataY2,scaleTimeY2):
        self.profileDockX1.setData(dataX1, scaleTimeX1)
        self.profileDockY1.setData(dataY1, scaleTimeY1)
        self.profileDockX2.setData(dataX2, scaleTimeX2)
        self.profileDockY2.setData(dataY2, scaleTimeY2)
    
    def __openViewGraphics__(self):
        self.viewGraphics = ViewGraphicsDialog(self.ui.centralwidget , not self.profileDockX1.isHidden(), not self.profileDockX2.isHidden(), not self.profileDockY1.isHidden() ,not self.profileDockY2.isHidden())
        self.viewGraphics.getUI().checkBoxMCPX1.stateChanged.connect(lambda :self.__changeHiddenModeDock__(self.profileDockX1))
        self.viewGraphics.getUI().checkBoxMCPX2.stateChanged.connect(lambda :self.__changeHiddenModeDock__(self.profileDockX2))
        self.viewGraphics.getUI().checkBoxMCPY1.stateChanged.connect(lambda :self.__changeHiddenModeDock__(self.profileDockY1))
        self.viewGraphics.getUI().checkBoxMCPY2.stateChanged.connect(lambda :self.__changeHiddenModeDock__(self.profileDockY2))
        self.viewGraphics.show()
    
    def __changeHiddenModeDock__(self,dock):
        if dock.isHidden():
            dock.show()
        else:
            dock.hide()
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())
    
    
    
