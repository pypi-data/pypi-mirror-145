'''
Created on Dec 28, 2021

@author: Dmitry
'''

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot 
from PyQt6.QtWidgets import QSizePolicy, QLabel
from ticsummary import dataTIC
from datetime import datetime as dt
from numpy import ndarray
import numpy as np
import pyqtgraph as pg
from re import match


class Ui_Plot(QObject):
    
    deleteWidgetIsCall = pyqtSignal()
    title:str
    flagDataSet:bool
    
    def __init__(self):
        QObject.__init__(self)
        self.flagDataSet = False
        
    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        Form.setWindowOpacity(0)
        Form.setContentsMargins(0, 0, 0, 0)
        #self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.comboBoxTypePlot = QtWidgets.QComboBox(Form)
        self.comboBoxTypePlot.setObjectName("comboBoxTypePlot")
        self.comboBoxTypePlot.currentIndexChanged.connect(self.onComboBoxTypePlotIndexChanged)
        
        '''for item in DataTIC.MeasureProfileTypeEnum:
            self.comboBoxTypePlot.addItem(item.title)'''
        
        self.horizontalLayout.addWidget(self.comboBoxTypePlot)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.titleLabel = QLabel(Form)
        self.horizontalLayout.addWidget(self.titleLabel)
        self.horizontalLayout.addItem(spacerItem)
        #self.pushButtonDelete = QtWidgets.QPushButton(Form)
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        #sizePolicy.setHorizontalStretch(25)
        #sizePolicy.setVerticalStretch(25)
        #sizePolicy.setHeightForWidth(self.pushButtonDelete.sizePolicy().hasHeightForWidth())
        #self.pushButtonDelete.setSizePolicy(sizePolicy)
        #self.pushButtonDelete.setMinimumSize(QtCore.QSize(25, 25))
        #self.pushButtonDelete.setMaximumSize(QtCore.QSize(25, 25))
        #self.pushButtonDelete.setSizeIncrement(QtCore.QSize(0, 0))
        #self.pushButtonDelete.setObjectName("pushButtonDelete")
        #self.pushButtonDelete.clicked.connect(self.deletePlot)
        #self.horizontalLayout.addWidget(self.pushButtonDelete)
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
        #self.pushButtonDelete.setText(_translate("Form", "X"))
    def setMainTitle(self, text):
        self.titleLabel.setText(text)
        
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
        self.flagDataSet = True
    def getBlockData(self):
        return self.blockData
    
    def deletePlot(self):
        #self.deleteWidgetIsCall.emit()
        
        print("widgethide")
        
    def onComboBoxTypePlotIndexChanged(self, index): 0
    
    def addItemcomboBoxTypePlot(self, item):
        self.comboBoxTypePlot.addItem(item)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    #Form.setSizePolicy(QSizePolicy.PolicyFlag.ExpandFlag,QSizePolicy.PolicyFlag.ExpandFlag)
    ui = Ui_Plot()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
