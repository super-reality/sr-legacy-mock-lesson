import sys

from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot, Qt, QSize,QEvent,QRect
from Setting import Settings
from PyQt5.QtGui import QIcon,QFont,QCursor,QPixmap,QPainter,QPen
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, \
QAction, QTabWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QFrame,QLabel,QSlider,QScrollArea,QCheckBox,QSizePolicy,QFileDialog,QDockWidget, QDialog
from Component import MyTableWidget
import webbrowser
from Container import MyBar,QAnchorDialog
from Mybutton import CommonButton
import logging
import keyboard

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.anchorDlg = QAnchorDialog(self)
        

    def __initStyleSheet(self):
        pass
    

        

if __name__ == "__main__":

    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.INFO)
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
