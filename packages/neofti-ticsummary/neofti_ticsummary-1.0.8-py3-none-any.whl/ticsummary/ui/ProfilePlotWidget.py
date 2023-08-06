from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject
from ticsummary import dataTIC
from ticsummary.ui import PlotWidget


class ProfilePlot(PlotWidget.Ui_Plot):
    def __init__(self, title):
        super().__init__()
        self.form = QtWidgets.QWidget()
        super().setupUi(self.form)
        for item in dataTIC.MeasureProfileTypeEnum:
            self.addItemcomboBoxTypePlot(item.title)
        super().setMainTitle(title)
            
    def onComboBoxTypePlotIndexChanged(self, index):
        if not self.flagDataSet: return
        match index:
            case 0:
                self.plotLineByXY(
                    self.getBlockData().countPerSlice, 
                    self.getBlockData().timePerSlice, 
                    dataTIC.MeasureProfileTypeEnum[0].title, 
                    dataTIC.MeasureProfileTypeEnum[0].nameX, 
                    dataTIC.MeasureProfileTypeEnum[0].unitX, 
                    dataTIC.MeasureProfileTypeEnum[0].nameY, 
                    dataTIC.MeasureProfileTypeEnum[0].unitY)
            case 1:
                self.plotLineByXY(
                    self.getBlockData().meanPerSlice, 
                    self.getBlockData().timePerSlice, 
                    dataTIC.MeasureProfileTypeEnum[1].title, 
                    dataTIC.MeasureProfileTypeEnum[1].nameX, 
                    dataTIC.MeasureProfileTypeEnum[1].unitX, 
                    dataTIC.MeasureProfileTypeEnum[1].nameY, 
                    dataTIC.MeasureProfileTypeEnum[1].unitY)
            case 2:
                self.plotLineByXY(
                    self.getBlockData().sigmaPerSlice, 
                    self.getBlockData().timePerSlice, 
                    dataTIC.MeasureProfileTypeEnum[2].title, 
                    dataTIC.MeasureProfileTypeEnum[2].nameX, 
                    dataTIC.MeasureProfileTypeEnum[2].unitX, 
                    dataTIC.MeasureProfileTypeEnum[2].nameY, 
                    dataTIC.MeasureProfileTypeEnum[2].unitY)
            case 3:
                self.plotLineByXY(
                    self.getBlockData().countPerChannel, 
                    self.getBlockData().numberPerChannel, 
                    dataTIC.MeasureProfileTypeEnum[3].title, 
                    dataTIC.MeasureProfileTypeEnum[3].nameX, 
                    dataTIC.MeasureProfileTypeEnum[3].unitX, 
                    dataTIC.MeasureProfileTypeEnum[3].nameY, 
                    dataTIC.MeasureProfileTypeEnum[3].unitY)
            case 4:
                self.plotColorMap(
                    self.getBlockData().matrix,
                    dataTIC.MeasureProfileTypeEnum[3].title, 
                    dataTIC.MeasureProfileTypeEnum[3].nameX, 
                    dataTIC.MeasureProfileTypeEnum[3].unitX, 
                    dataTIC.MeasureProfileTypeEnum[3].nameY, 
                    dataTIC.MeasureProfileTypeEnum[3].unitY,
                    dataTIC.MeasureProfileTypeEnum[3].nameColor,
                    dataTIC.MeasureProfileTypeEnum[3].unitColor)
        print(index)
        
    def getWidget(self):
        return self.form
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = ProfilePlot()
    Form.show()
    sys.exit(app.exec())  

'''
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot 
import numpy as np
import pyqtgraph as pg
from numpy import ndarray
from TICSummary import DataTIC
from datetime import datetime as dt
from re import match

class Ui_Plot(QObject):
    
    def __init__(self):
        QObject.__init__(self)
    
    deleteWidgetIsCall = pyqtSignal()
    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBoxTypePlot = QtWidgets.QComboBox(Form)
        self.comboBoxTypePlot.setObjectName("comboBoxTypePlot")
        self.comboBoxTypePlot.currentIndexChanged.connect(self.onComboBoxTypePlotIndexChanged)
        
        for item in DataTIC.MeasureProfileTypeEnum:
            self.comboBoxTypePlot.addItem(item.title)
        
        self.horizontalLayout.addWidget(self.comboBoxTypePlot)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonDelete = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(25)
        sizePolicy.setVerticalStretch(25)
        sizePolicy.setHeightForWidth(self.pushButtonDelete.sizePolicy().hasHeightForWidth())
        self.pushButtonDelete.setSizePolicy(sizePolicy)
        self.pushButtonDelete.setMinimumSize(QtCore.QSize(25, 25))
        self.pushButtonDelete.setMaximumSize(QtCore.QSize(25, 25))
        self.pushButtonDelete.setSizeIncrement(QtCore.QSize(0, 0))
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.pushButtonDelete.clicked.connect(self.deletePlot)
        self.horizontalLayout.addWidget(self.pushButtonDelete)
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        self.layoutPlot = pg.GraphicsLayoutWidget()
        self.linePlot = self.layoutPlot.addPlot()
        self.colorMapPlot = self.layoutPlot.addPlot()
        self.linePlot.hide()
        self.colorMapPlot.hide()
        self.cmap = pg.colormap.get('CET-L9')
        self.bar = pg.ColorBarItem(
            interactive=True, colorMap=self.cmap)
        font=QtGui.QFont()
        font.setPixelSize(20)
        self.linePlot.getAxis("bottom").setTickFont(font)
        self.linePlot.getAxis("left").setTickFont(font)
        self.colorMapPlot.getAxis("bottom").setTickFont(font)
        self.colorMapPlot.getAxis("left").setTickFont(font)
        self.bar.getAxis("right").setTickFont(font)

        #data = np.fromfunction(lambda i, j: i*j, (100, 100))
        self.image = pg.ImageItem()
        self.colorMapPlot.addItem(self.image)
        self.bar.setImageItem(self.image, insert_in=self.colorMapPlot)
        
        self.verticalLayout.addWidget(self.layoutPlot)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
        self.labelAxisStyle = {'color': '#FFF', 'font-size': '14pt'}
        self.titlePlotStyle = {'color': '#FFF', 'font-size': '20pt'}

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButtonDelete.setText(_translate("Form", "X"))
        
    def plotLineBy2darray(self, data, titlePlot, titleX, unitX, titleY, unitY):
        splittedData = np.hsplit(data, 2)
        self.plotLineByXY(
            splittedData[0].flatten(), 
            splittedData[1].flatten(), 
            titlePlot, 
            titleX, unitX, 
            titleY, unitY)
    def plotLineByXY(self, x, y, titlePlot, titleX, unitX, titleY, unitY):
        self.colorMapPlot.hide()
        self.linePlot.show()
        self.linePlot.clear()
        self.linePlot.plot(x=x, y=y)
        self.linePlot.setTitle(titlePlot, **self.titlePlotStyle)
        self.linePlot.setLabel('left', titleY, units=unitY, **self.labelAxisStyle)
        self.linePlot.setLabel('bottom', titleX, units=unitX, **self.labelAxisStyle)
        
    def plotColorMap(self, data, titlePlot, titleX, unitX, titleY, unitY, titleColorBar, unitColor):
        self.colorMapPlot.show()
        self.linePlot.hide()
        self.image.setImage(image=data)
        self.bar._update_items()
        self.colorMapPlot.setTitle(titlePlot, **self.titlePlotStyle)
        self.colorMapPlot.setLabel('left', titleY, units=unitY, **self.labelAxisStyle)
        self.colorMapPlot.setLabel('bottom', titleX, units=unitX, **self.labelAxisStyle)
        self.bar.setLabel('left', titleColorBar, units=unitColor, **self.labelAxisStyle)
        
    def setBlockData(self, data):
        self.blockData = data
        
    def deletePlot(self):
        self.deleteWidgetIsCall.emit()
    def onComboBoxTypePlotIndexChanged(self, index):
        match index:
            case 0:
                self.plotLineByXY(
                    self.blockData.countPerSlice, 
                    self.blockData.timePerSlice, 
                    DataTIC.MeasureProfileTypeEnum[0].title, 
                    DataTIC.MeasureProfileTypeEnum[0].nameX, 
                    DataTIC.MeasureProfileTypeEnum[0].unitX, 
                    DataTIC.MeasureProfileTypeEnum[0].nameY, 
                    DataTIC.MeasureProfileTypeEnum[0].unitY)
            case 1:
                self.plotLineByXY(
                    self.blockData.meanPerSlice, 
                    self.blockData.timePerSlice, 
                    DataTIC.MeasureProfileTypeEnum[1].title, 
                    DataTIC.MeasureProfileTypeEnum[1].nameX, 
                    DataTIC.MeasureProfileTypeEnum[1].unitX, 
                    DataTIC.MeasureProfileTypeEnum[1].nameY, 
                    DataTIC.MeasureProfileTypeEnum[1].unitY)
            case 2:
                self.plotLineByXY(
                    self.blockData.sigmaPerSlice, 
                    self.blockData.timePerSlice, 
                    DataTIC.MeasureProfileTypeEnum[2].title, 
                    DataTIC.MeasureProfileTypeEnum[2].nameX, 
                    DataTIC.MeasureProfileTypeEnum[2].unitX, 
                    DataTIC.MeasureProfileTypeEnum[2].nameY, 
                    DataTIC.MeasureProfileTypeEnum[2].unitY)
            case 3:
                self.plotLineByXY(
                    self.blockData.countPerChannel, 
                    self.blockData.numberPerChannel, 
                    DataTIC.MeasureProfileTypeEnum[3].title, 
                    DataTIC.MeasureProfileTypeEnum[3].nameX, 
                    DataTIC.MeasureProfileTypeEnum[3].unitX, 
                    DataTIC.MeasureProfileTypeEnum[3].nameY, 
                    DataTIC.MeasureProfileTypeEnum[3].unitY)
            case 4:
                self.plotColorMap(
                    self.blockData.matrix,
                    DataTIC.MeasureProfileTypeEnum[3].title, 
                    DataTIC.MeasureProfileTypeEnum[3].nameX, 
                    DataTIC.MeasureProfileTypeEnum[3].unitX, 
                    DataTIC.MeasureProfileTypeEnum[3].nameY, 
                    DataTIC.MeasureProfileTypeEnum[3].unitY,
                    DataTIC.MeasureProfileTypeEnum[3].nameColor,
                    DataTIC.MeasureProfileTypeEnum[3].unitColor)
        print(index)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Plot()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
'''