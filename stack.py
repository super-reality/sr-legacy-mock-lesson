from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import sys 
  
  
class Window(QWidget): 
    def __init__(self): 
        super().__init__() 
  
  
        # set the title 
        self.setWindowTitle("Python") 
  
        # setting geometry 
        self.setGeometry(100, 100, 600, 400) 
  
        # setting up the style of border 
        self.setStyleSheet("border : 3px dashed blue;") 
  
        # creating a label widget 
        self.label_1 = QLabel("new border ", self) 
  
        # moving position 
        self.label_1.move(100, 100) 
  
        # setting up the border 
        self.label_1.setStyleSheet("border :3px solid black;") 
  
        # show all the widgets 
        self.show() 
  
  
# create pyqt5 app 
App = QApplication(sys.argv) 
  
# create the instance of our Window 
window = Window() 
  
# start the app 
sys.exit(App.exec()) 