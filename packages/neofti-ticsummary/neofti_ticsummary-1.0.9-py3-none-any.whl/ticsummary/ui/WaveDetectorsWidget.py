from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject
from ticsummary import dataTIC
from ticsummary.ui import PlotWidget


class WaveScintillators(PlotWidget.Ui_Plot):
    def __init__(self, title):
        super().__init__()
        self.form = QtWidgets.QWidget()
        super().setupUi(self.form)
        for item in dataTIC.MeasureWaveDetectorsEnum:
            self.addItemcomboBoxTypePlot(item.title)
        super().setMainTitle(title)
    def getWidget(self):
        return self.form