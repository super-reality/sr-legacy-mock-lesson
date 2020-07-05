from PyQt5.QtWidgets import QWidget,QApplication
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
import sys
class SomeWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.defaultWindowFlags = self.windowFlags()
        self.setAttribute(Qt.WA_TranslucentBackground)

        # ...
        self.restoreButton = QtWidgets.QPushButton('Restore state')
        # ...
        self.restoreButton.clicked.connect(self.restoreFlags)

    def mousePressEvent(self,event):
        print('checkmehere')
        self.setWindowFlags(self.defaultWindowFlags)
        pass

    def restoreFlags(self):
        # setWindowFlags calls setParent(), so you might need to show it again if
        # it was visible before; let's store the current state
        isVisible = self.isVisible()
        self.setWindowFlags(self.defaultWindowFlags)
        if isVisible:
            self.setVisible(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = SomeWidget(None)
    mw.show()
    sys.exit(app.exec_())
    pass