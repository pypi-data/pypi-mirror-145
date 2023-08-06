from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_CountScintillatorsWidget(object):
    def setupUi(self, CountScintillatorsWidget):
        CountScintillatorsWidget.setObjectName("CountScintillators")
        CountScintillatorsWidget.resize(400, 300)
        CountScintillatorsWidget.setWindowTitle("")
        self.gridLayout = QtWidgets.QGridLayout(CountScintillatorsWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.spinBoxCountLeftUp = QtWidgets.QSpinBox(CountScintillatorsWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.spinBoxCountLeftUp.setFont(font)
        self.spinBoxCountLeftUp.setReadOnly(True)
        self.spinBoxCountLeftUp.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBoxCountLeftUp.setObjectName("spinBoxCountLeftUp")
        self.gridLayout.addWidget(self.spinBoxCountLeftUp, 0, 0, 1, 1)
        self.spinBoxCountRightUp = QtWidgets.QSpinBox(CountScintillatorsWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.spinBoxCountRightUp.setFont(font)
        self.spinBoxCountRightUp.setReadOnly(True)
        self.spinBoxCountRightUp.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBoxCountRightUp.setObjectName("spinBoxCountRightUp")
        self.gridLayout.addWidget(self.spinBoxCountRightUp, 0, 2, 1, 1)
        self.spinBoxCountCenter = QtWidgets.QSpinBox(CountScintillatorsWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.spinBoxCountCenter.setFont(font)
        self.spinBoxCountCenter.setReadOnly(True)
        self.spinBoxCountCenter.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBoxCountCenter.setObjectName("spinBoxCountCenter")
        self.gridLayout.addWidget(self.spinBoxCountCenter, 1, 1, 1, 1)
        self.spinBoxCountLeftBottom = QtWidgets.QSpinBox(CountScintillatorsWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.spinBoxCountLeftBottom.setFont(font)
        self.spinBoxCountLeftBottom.setReadOnly(True)
        self.spinBoxCountLeftBottom.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBoxCountLeftBottom.setObjectName("spinBoxCountLeftBottom")
        self.gridLayout.addWidget(self.spinBoxCountLeftBottom, 2, 0, 1, 1)
        self.spinBoxRightBottom = QtWidgets.QSpinBox(CountScintillatorsWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.spinBoxRightBottom.setFont(font)
        self.spinBoxRightBottom.setReadOnly(True)
        self.spinBoxRightBottom.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBoxRightBottom.setObjectName("spinBoxRightBottom")
        self.gridLayout.addWidget(self.spinBoxRightBottom, 2, 2, 1, 1)

        self.retranslateUi(CountScintillatorsWidget)
        QtCore.QMetaObject.connectSlotsByName(CountScintillatorsWidget)

    def retranslateUi(self, CountScintillatorsWidget):
        pass

class CountScintillators():
    def __init__(self):
        self.widget = QtWidgets.QWidget()
        self.ui = Ui_CountScintillatorsWidget()
        self.ui.setupUi(self.widget)
    def show(self):
        self.widget.show()
    def getWidget(self):
        return self.widget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    countScintillatorsWidget = CountScintillators()
    countScintillatorsWidget.show()
    sys.exit(app.exec())
