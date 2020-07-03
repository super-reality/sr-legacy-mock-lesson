import sys

from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget,QSpinBox
from PyQt5.QtCore import pyqtSlot, Qt, QSize,QEvent,pyqtSignal,pyqtSlot
from Setting import Settings
from PyQt5.QtGui import QIcon,QFont,QCursor,QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, \
QAction, QTabWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QFrame,QLabel,QSlider,\
    QScrollArea,QCheckBox,QSizePolicy,QFileDialog,QDockWidget, QDialog,QListWidget,QProgressBar
from Component import MyTableWidget
import webbrowser
from Container import MyBar
from Mybutton import CommonButton
from QtWaitingSpinner.pyqtspinner.spinner import WaitingSpinner

from StudentComponent import CommonLessonItem

import threading
import time

from threading import Thread
from Setting import Settings
from PyQt5.QtCore import pyqtSignal,pyqtSlot


class MyCommonThread(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self,parent=None,**kwargs):
        """
        """
        Thread.__init__(self,daemon=True)
        self.parent = parent
        


    def run(self):
        for i in range(100):
            time.sleep(0.1)
            self.parent.sig_Increase.emit(i+1)
        pass

class MyProgressDlg(QDialog):
    
    def __init__(self,parent):
        super(MyProgressDlg,self).__init__(parent)
        self.progress = QProgressBar(self)
        self.setModal(True)
        
        self.__initUI()
        self.hide()

    def __initUI(self):
        self.progress.valueChanged.connect(self.processValuechanged)
        self.progress.setMaximum(100)
        self.label = QLabel(self)
        self.label.setText("Please wait for loading")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.progress)
        self.resize(200,100)
        self.setWindowTitle("Loading...")
        pass

    def processValuechanged(self,value):
        if(value == self.progress.maximum()):
            self.hide()
        else:
            pass

    
    
class MainWindow(QWidget):
    sig_Increase = pyqtSignal(int)
    def __init__(self):
        super(MainWindow, self).__init__()
        self.sig_Increase.connect(self.process)
        test_thread = MyCommonThread(self)
        test_thread.start()
        self.progressDlg = MyProgressDlg(self)
        
        self.resize(400,400)
    
    def process(self,val):
        self.progressDlg.show()
        self.progressDlg.progress.setValue(val)



class SomeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.defaultWindowFlags = self.windowFlags()
        print(self.windowFlags())
        exit(0)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # ...
        self.restoreButton = QPushButton('Restore state')
        # ...
        self.restoreButton.clicked.connect(self.restoreFlags)

    def restoreFlags(self):
        # setWindowFlags calls setParent(), so you might need to show it again if
        # it was visible before; let's store the current state
        isVisible = self.isVisible()
        self.setWindowFlags(self.defaultWindowFlags)
        if isVisible:
            self.setVisible(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = SomeWidget()
    mw.show()
    sys.exit(app.exec_())
