from PyQt6.QtCore import QObject, QThread, pyqtSignal
'''
class __PyQTBackWorkingWithProgress__(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.thread = QThread()
        self.thread.started.connect(self.__taskRun__)
        self.finished.connect(self.thread.quit)
        self.finished.connect(self.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.progress.connect(self.reportProgress)
    
    def setTaskFunc(self,func):
        self.func = func
    def __taskRun__(self):
        self.reportProgress(self.func())
        self.finished.emit()
    def run (self):
        self.moveToThread(self.thread)
        self.thread.start()
    def reportProgress(i):
        print(i)

class __PyQTBackWorking__(QObject):
    finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.thread = QThread()
        self.thread.started.connect(self.__taskRun__)
        self.finished.connect(self.thread.quit)
        self.finished.connect(self.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
    
    def setTaskFunc(self,func):
        self.func = func
    def taskRun(self):
        self.reportProgress(self.func())
        self.finished.emit()
    def run (self):
        self.moveToThread(self.thread)
        self.thread.start()
'''
class HandlerTask(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    
    #private constructor
    def __init__(self, func):
        super().__init__()
        self.func = func
    def run(self):
        self.func()
        self.finished.emit()
    
def runTask(taskFunc, endFunc=None, progressReportFunc=None):
    handler = HandlerTask(taskFunc)
    thread = QThread()
    handler.moveToThread(thread)
    #thread.started.connect(self.__taskRun__)
    handler.finished.connect(thread.quit)
    handler.finished.connect(handler.deleteLater)
    handler.finished.connect(thread.deleteLater)
    if endFunc != None: handler.finished.connect(endFunc)
    if progressReportFunc != None: handler.progress.connect(progressReportFunc)
    thread.started.connect(handler.run)
                           
    thread.start()
    return (handler, thread)
    #handler.progress.connect(self.reportProgress)
