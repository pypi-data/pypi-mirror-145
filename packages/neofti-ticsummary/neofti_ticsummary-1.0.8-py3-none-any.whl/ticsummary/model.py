from tracemalloc import start
from ticsummary import dataTIC, databaseMYSQL, inputDataHandler
from ticsummary.ui.MainWindow import MainWindow, ModeInterface as MWModeInterface
from ticsummary.ui.ConnectionConfigurationDialog import ConnectionConfiguration
from ticsummary.ui.OpenSqlDataDialog import OpenSQLData
from ticsummary import databaseMYSQL
from ticsummary.backWorking import *
from PyQt6 import QtWidgets, QtCore
import threading, queue
from PyQt6.QtWidgets import QMessageBox

class Model():
    def __init__(self):
        self.__initView__()
        self.__initSignal__()
        self.sqlParameters = None
        self.mainWindow.show()
        callback_queue = queue.Queue()
        
        self.profileXDescriptionDevice = dataTIC.DescriptionDevice("profileX",0,31)
        self.profileYDescriptionDevice = dataTIC.DescriptionDevice("profileY",32,63)
    def __initView__(self):
        self.mainWindow = MainWindow()
        self.mainWindow.ui.comboBoxType.currentIndexChanged.connect(self.__typeChanged)
        
    def __initSignal__(self):
        self.mainWindow.connectSignalOpenConnectionConfiguration(self.openConnectionConfiguration)
        self.mainWindow.connectSignalOpenDataFromSqlDatabase(self.startOpenSQLData)
        self.mainWindow.ui.comboBoxListData.currentTextChanged.connect(self.loadDataByIdAndPlot)
    
    def __del__(self):
        self.connector.close()
    
    def openConnectionConfiguration(self):
        connectionConfigurationDialog = ConnectionConfiguration(self.sqlParameters)
        connectionConfigurationDialog.setModal(True)
        connectionConfigurationDialog.exec()
        if connectionConfigurationDialog.result() == QtWidgets.QDialog.DialogCode.Accepted:
            self.sqlParameters = connectionConfigurationDialog.getNewParameters()
            try:
                self.listData = databaseMYSQL.getListId(self.sqlParameters)
                self.mainWindow.setMode(MWModeInterface.DBISCONNECTED)
                self.connector = databaseMYSQL.openConnection(self.sqlParameters)
                self.mainWindow.setIndexListData(map(str,self.listData['id_RUN']))
            except Exception as e:
                print("Error sql:", e) 
                
    def loadDataByIdAndPlot(self,id, connector=None):
        thread = threading.Thread(target=self.__backThreadLoadDataByIdAndPlot__,args=(id,connector))
        thread.start()
        
    def __backThreadLoadData__(self,id,connector):
        if connector == None:
            dataB1 = databaseMYSQL.getRecordByIdFirstbank(self.sqlParameters.table, self.connector, int(id))
            dataB2 = databaseMYSQL.getRecordByIdSecondBank(self.sqlParameters.table, self.connector, int(id))
        else:
            dataB1 = databaseMYSQL.getRecordByIdFirstbank(self.sqlParameters.table, connector, int(id))
            dataB2 = databaseMYSQL.getRecordByIdSecondBank(self.sqlParameters.table, connector, int(id))
        
    def __plotData__(self,dataB1,dataB2):
        profileX1Data = inputDataHandler.getMatrixByFromToFilter(dataB1.matrix, self.profileXDescriptionDevice.channelFrom, self.profileXDescriptionDevice.channelTo)
        profileY1Data = inputDataHandler.getMatrixByFromToFilter(dataB1.matrix, self.profileYDescriptionDevice.channelFrom, self.profileYDescriptionDevice.channelTo)
        profileX2Data = inputDataHandler.getMatrixByFromToFilter(dataB2.matrix, self.profileXDescriptionDevice.channelFrom, self.profileXDescriptionDevice.channelTo)
        profileY2Data = inputDataHandler.getMatrixByFromToFilter(dataB2.matrix, self.profileYDescriptionDevice.channelFrom, self.profileYDescriptionDevice.channelTo)
        self.mainWindow.setData(profileX1Data,
            float(dataB1.timeslice/(10**6)),
            profileY1Data,
            float(dataB1.timeslice/(10**6)),
            profileX2Data,
            float(dataB2.timeslice/(10**6)),
            profileY2Data,
            float(dataB2.timeslice/(10**6)))
    def __typeChanged(self,id):
        if id == 0:
            self.mainWindow.ui.comboBoxListData.setEnabled(True)
            if self.realTimeModeOn :
                self.realTimeModeOn = False
                self.offRealTimeMode()    
        if id == 1:
            self.mainWindow.ui.comboBoxListData.setEnabled(False)
            self.realTimeModeOn = True
            self.setRealTimeMode() 
    
    def setRealTimeMode(self):
        self.realTimeModeTimer = QtCore.QTimer()
        self.realTimeModeTimer.timeout.connect(self.__doTimerRealTimeMode__)
        self.realTimeModeTimer.start(1000)
        self.lastCount = 0
    def offRealTimeMode(self):
        self.realTimeModeTimer.stop()
    def __doTimerRealTimeMode__(self):
        tempconnector = databaseMYSQL.openConnection(self.sqlParameters)
        count = databaseMYSQL.getCountRecords(self.sqlParameters.table,tempconnector)
        if count > self.lastCount:
            self.lastCount = count
            self.loadDataByIdAndPlot(count-1,tempconnector)
        tempconnector.commit()
    
    def startOpenSQLData(self):
        self.mainWindow.setInfinityProgress()
        self.handlerTaskOpenData = runTask(self.taskOpenData,self.endOpenSqlData)
        
    def taskOpenData(self):
        self.openSQLData = OpenSQLData(self.sqlParameters, lambda result: self.setNewListData(result))
        
    def endOpenSqlData(self):
        self.mainWindow.unsetInfinityProgress()
        self.openSQLData.show()

    def setNewConnectionParameters(self, parameters):
        self.sqlParameters = parameters
        
    def setNewListData(self, list):
        self.listData = list