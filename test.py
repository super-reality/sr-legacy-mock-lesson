from PyQt5.QtWidgets import QMainWindow, QApplication,QFrame,QWidget,QVBoxLayout
from PyQt5.QtCore import Qt
import sys


class MainWindowExample(QWidget):
    def __init__(self, parent=None):
        try:
            QMainWindow.__init__(self, parent)
            # self.setStyleSheet("border: 11px solid ;")
            # self.setWindowOpacity(0.3)
            self.test = QWidget(self)
            self.layout = QVBoxLayout(self)
            self.layout.addWidget(self.test)
            self.test.setWindowOpacity(0.5)
            self.test.setStyleSheet('background-color:red')
            self.test.resize(300,300)
            self.setAttribute(Qt.WA_NoSystemBackground, True)
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
            
        except Exception as e:
            print(e)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_widow = MainWindowExample()
    main_widow.show()
    sys.exit(app.exec_())