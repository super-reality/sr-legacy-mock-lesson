from PyQt5.QtWidgets import QWidget,QApplication,QTextEdit
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
import sys


class MyContainer(QWidget):
    def __init__(self,parent):
        super(MyContainer,self).__init__(parent)
        # self.setContentsMargins(0,0,0,0)
        # self.setStyleSheet('border:0')
        
    def __initUI(self):
        pass
    def setWidgetSpan(self, widget, rowspan=1, colspan=1):
        index = self.layout.indexOf(widget)
        row, column = self.layout.getItemPosition(index)[:2]
        self.layout.addWidget(widget, row, column, rowspan, colspan)

class SomeWidget(MyContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def mousePressEvent(self,event):
        pass

    def restoreFlags(self):
        # setWindowFlags calls setParent(), so you might need to show it again if
        # it was visible before; let's store the current state
        pass
class mainWidget(QWidget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        styles = """
        MyContainer{
            border:3px solid green
        }
        """
        widget = SomeWidget(self)
        widget.setWindowFlags(Qt.FramelessWindowHint|Qt.Window)
        widget.resize(self.width()//2,self.height()//2)
        widget.setStyleSheet('background-color:red')
        widget.show()
        self.setStyleSheet(styles)
        pass

def test1():
    return 0,1

if __name__ == "__main__":

    # app = QApplication(sys.argv)
    # mw = mainWidget()
    # mw.show()
    # sys.exit(app.exec_())
    
    pass