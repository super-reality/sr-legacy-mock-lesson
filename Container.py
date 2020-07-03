import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QDialogButtonBox,QMessageBox,\
QAction, QTabWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QFrame,QLabel,QSlider,QScrollArea,QCheckBox,QSizePolicy,QFileDialog,QDockWidget,\
     QDialog,QTextEdit,QSizeGrip,QToolButton,QGraphicsOpacityEffect
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon,QFont,QCursor,QPixmap,QPaintDevice,QPainter,QPen
from PyQt5.QtCore import pyqtSlot, Qt, QSize,QEvent,QTimer,QPoint,pyqtSignal
from Setting import Settings
from Mybutton import TitleButton,CloseButton
from wordprocessor.wordprocessor import MyTextEditDialog
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import Qt,QUrl
from MyUtil import getPixmapFromScreen, isImageUrl,getScreenSize
from threading import Thread
import time

class MyFrame(QtWidgets.QWidget):

    def __init__(self,parent):

        super(MyFrame, self).__init__(parent)
        self.setContentsMargins(10,10,10,10)

    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        pen = QPen(Qt.black, 5)
        qp.setPen(pen)
        self.drawLine(event, qp)
        qp.end()

    def drawLine(self, event, qp):

        qp.drawLine(0, self.height(), self.width(), self.height())
    
    def setWidgetSpan(self, widget, rowspan=1, colspan=1):
        index = self.layout.indexOf(widget)
        row, column = self.layout.getItemPosition(index)[:2]
        self.layout.addWidget(widget, row, column, rowspan, colspan)

class MyVBoxLayout(QtWidgets.QVBoxLayout):
    def __init__(self,parent):
        super(MyVBoxLayout,self).__init__(parent)
        self.setContentsMargins(0,0,0,0)

class MyHBoxLayout(QtWidgets.QHBoxLayout):
    def __init__(self,parent):
        super(MyHBoxLayout,self).__init__(parent)
        self.setContentsMargins(0,0,0,0)

class MyGridLayout(QtWidgets.QGridLayout):
    def __init__(self,parent):
        super(MyGridLayout,self).__init__(parent)
        self.setContentsMargins(0,0,0,0)

class MyContainer(QWidget):
    def __init__(self,parent):
        super(MyContainer,self).__init__(parent)
        self.setContentsMargins(0,0,0,0)
        self.setStyleSheet('border:0')
    def __initUI(self):
        pass
    def setWidgetSpan(self, widget, rowspan=1, colspan=1):
        index = self.layout.indexOf(widget)
        row, column = self.layout.getItemPosition(index)[:2]
        self.layout.addWidget(widget, row, column, rowspan, colspan)

class CommonHeaderLabel(QLabel):
    def __init__(self,parent):
        super(CommonHeaderLabel,self).__init__(parent)
        self.setWordWrap(True)
        self.setFont(QFont('Arial',14))

class CommonHeaderLabelForAnchor(CommonHeaderLabel):
    def __init__(self,parent):
        super(CommonHeaderLabelForAnchor,self).__init__(parent)
        self.setWordWrap(True)
        self.setFont(QFont('Arial',14))
    def enterEvent(self,event):
        self.setCursor(Qt.SizeAllCursor)

class CommonHeaderIcon(QLabel):

    clicked = pyqtSignal(str)

    def __init__(self,parent):
        super(CommonHeaderIcon,self).__init__(parent)
        # self.setFixedSize(30,30)
        self.setStyleSheet('border:0')
        self.setWordWrap(True)
        self.setScaledContents(True)

    def enterEvent(self,event):
        self.setCursor(Qt.PointingHandCursor)
    def mousePressEvent(self,event):
        self.clicked.emit("start")

class CommonDescriptionLabel(QLabel):
    def __init__(self,parent):
        super(CommonDescriptionLabel,self).__init__(parent)
        self.setFont(QFont('Arial',12))
        self.setWordWrap(True)

class CommonDescriptionTextEdit(QTextEdit):
    def __init__(self,parent):
        super(CommonDescriptionTextEdit,self).__init__(parent)
        self.setFixedHeight(50)
        self.textChanged.connect(self.processTextChanged)
        self.__initUI()
    def __initUI(self):
        self.setFont(QFont('Arial',12))
    def processTextChanged(self):
        size = self.document().size().toSize()
        if(size.height()<50):
            return
        self.setFixedHeight(size.height()+3)

class CommonHeaderTextEdit(QTextEdit):
    def __init__(self,parent):
        super(CommonHeaderTextEdit,self).__init__(parent)
        self.setFixedHeight(50)
        self.setStyleSheet('height:50px')
        self.textChanged.connect(self.processTextChanged)
        self.__initUI()
    def __initUI(self):
        self.setFont(QFont('Arial',16))

    def processTextChanged(self):
        size = self.document().size().toSize()
        self.setFixedHeight(size.height()+3)

class QAnchorDialog(QLabel):
    pixmapChanged = pyqtSignal()
    sig_mouseClick = pyqtSignal(int,int)
    def __init__(self,parent):

        super(QAnchorDialog,self).__init__(parent)

        #set corner's sizeGrip Objects
        self.topleftgrip =QSizeGrip(self)
        self.toprightgrip =QSizeGrip(self)
        self.bottomrightgrip =QSizeGrip(self)
        self.bottomleftgrip =QSizeGrip(self)
        self.topleftgrip.setStyleSheet('background-color:lightgreen')
        self.toprightgrip.setStyleSheet('background-color:lightgreen')
        self.bottomrightgrip.setStyleSheet('background-color:lightgreen')
        self.bottomleftgrip.setStyleSheet('background-color:lightgreen')
        self.resize(300,200)
        
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.Window)
        self.__initUI()

        #set opacity
        self.setWindowOpacity(0.7) # this is should be called after InitUI() to take effect
        self.ClickPointable = False
        self.posxToEmit = None
        self.posyToEmit = None

        #set object name for style
        self.setObjectName("AnchorDlg")
        self.setStyleSheet('#AnchorDlg{border:3px solid black; border-style:dashed}')
        
    def hideAllChild(self,ishide=True):
        if(ishide):
            self.label_header.hide()
            self.topleftgrip.hide()
            self.toprightgrip.hide()
            self.bottomleftgrip.hide()
            self.bottomrightgrip.hide()
            pass
        else:
            pass
    def setClickPoint(self,b_clickable=False):
        self.ClickPointable = b_clickable

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()


    def __initUI(self):

        gbox = MyGridLayout(self)
        self.label_header = CommonHeaderLabelForAnchor(self)
        self.label_header.setText("ANCHOR\n \nDrag and Double Click To Capture Image")
        self.label_header.setWordWrap(True)
        self.label_header.setAlignment(Qt.AlignCenter)
        
        
        gbox.addWidget(self.topleftgrip,0,0,1,1)
        gbox.addWidget(self.toprightgrip,0,19,1,1)
        gbox.addWidget(self.bottomrightgrip,19,19,1,1)
        gbox.addWidget(self.bottomleftgrip,19,0,1,1)
        
        
        gbox.addWidget(self.label_header,1,1,18,18)

        #bind event
        self.label_header.installEventFilter(self)
        pass
    
    def getPixmapAtCurrentPosition(self):
        
        if(self.isHidden()):
            return
        posx = self.mapToGlobal(QPoint(0,0)).x()
        posy = self.mapToGlobal(QPoint(0,0)).y()
        W = self.width()
        H = self.height()

        
        #hide temporarily to get image behind of this dialog
        self.hide()
        pix = getPixmapFromScreen(posx,posy,W,H)
        self.setPixmap(pix)
        
        
        #hide all text after double click.
        self.label_header.setText("")
        
        #move again to original pos
        self.pixmapChanged.emit()

    def mouseDoubleClickEvent(self,event):

        posx = self.mapToGlobal(QPoint(0,0)).x()
        posy = self.mapToGlobal(QPoint(0,0)).y()
        W = self.width()
        H = self.height()
        
        #hide temporarily to get image behind of this dialog
        self.hide()
        pix = getPixmapFromScreen(posx,posy,W,H)
        self.setPixmap(pix)
        
        
        #hide all text after double click.
        self.label_header.setText("")
        
        #move again to original pos
        self.show()
        self.move(posx + Settings.bias,posy + Settings.bias)
        self.pixmapChanged.emit()

        self.posxToEmit = event.globalX() - posx
        self.posyToEmit = event.globalY() - posy

        self.sig_mouseClick.emit(self.posxToEmit,self.posyToEmit)

        pass
    
    def enterEvent(self,e):
        pass

    def mouseMoveEvent(self,e):
        delta = QPoint (e.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = e.globalPos()
 
    def showEvent(self,e):
        # self.move(self.parentWidget().mapToGlobal(QPoint(220,220))+QPoint(100,0))
        pass

    def mouseReleaseEvent(self,event):
        #if anchor is out of screen, then let it go into inside of screen
        posx = self.mapToGlobal(QPoint(0,0)).x()
        posy = self.mapToGlobal(QPoint(0,0)).y()
        screenH,screenW = getScreenSize()
        if(posx<0):
            posx = 0
        if((posx + self.width())>screenW):
            posx = screenW - self.width()
        if(posy<0):
            posy = 0
        if(posy + self.height()>screenH):
            posy = screenH - self.height()
        self.move(posx,posy)
        
    def paintEvent(self,event):
        
        if(self.ClickPointable):
            pass
        else:
            super().paintEvent(event)
            return
        
        painter = QPainter(self)
        painter.setPen(Qt.red)
        
        if self.posxToEmit is not None and self.posyToEmit is not None:
            painter.drawLine(self.posxToEmit-20,self.posyToEmit,self.posxToEmit+20,self.posyToEmit)
            painter.drawLine(self.posxToEmit,self.posyToEmit-20,self.posxToEmit,self.posyToEmit+20)
            painter.drawEllipse(self.posxToEmit-20,self.posyToEmit-20,40,40)
        else:
            pass

class MyRichTextDockWidget(QMainWindow):
    def __init__(self, *args):

        super(MyRichTextDockWidget,self).__init__(*args)
        self.__initUI()

    def __initUI(self):

        self.wordprocessor = MyTextEditDialog(self)
        self.dockWidget = MyDock(self)
        self.dockWidget.setWidget(self.wordprocessor)
        self.dockWidget.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea,self.dockWidget)
        
        #event binidng
        self.dockWidget.topLevelChanged.connect(self.floatingChanged)
        pass
    def setPlaceHolderText(self,placeHStr):
        self.wordprocessor.editor.setPlaceholderText(placeHStr)
    def floatingChanged(self):
        if(self.dockWidget.isFloating()):
            self.wordprocessor.hideAllButTextEdit(True)
            
        else:
            self.wordprocessor.hideAllButTextEdit(False)
    def getText(self):
        return self.wordprocessor.editor.toPlainText()

class MyDock(QDockWidget):
    def __init__(self,parent = None):
        super(MyDock,self).__init__(parent=parent)
        self.hideTitleWidget()
        self.topLevelChanged.connect(self.floatingChanged)
    
    def hideTitleWidget(self):
        # title = QWidget()
        # self.setTitleBarWidget(title)
        # self.titleBarWidget().hide()
        pass
    def setFrame(self,frame):
        self.setWidget(frame)
        pass
    def closeEvent(self,event):
        self.setFloating(False)
        self.hideTitleWidget()
        event.ignore()
    def floatingChanged(self,bfloat):
        if(bfloat == False):
            self.hideTitleWidget()

class MyBar(QWidget):

    def __init__(self, parent):

        super(MyBar, self).__init__()
        self.parent = parent
        self.setFixedHeight(30)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.title = TitleButton(self)
        self.title.setFixedWidth(100)
        self.title.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.title.move(0,0)
        

        self.btn_close = CloseButton(self)
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.btn_close.setFixedWidth(30)
        self.btn_close.move(0,200)

        
        self.layout.addWidget(self.title)
        self.layout.addStretch(1)
        self.layout.addWidget(self.btn_close)

        
        self.start = QPoint(0, 0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(MyBar, self).resizeEvent(QResizeEvent)

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False


    def btn_close_clicked(self):
        self.parent.close()

    def btn_max_clicked(self):
        self.parent.showMaximized()

    def btn_min_clicked(self):
        self.parent.showMinimized()

class MyDropableLable(QLabel):
    def __init__(self,parent):
        super(MyDropableLable,self).__init__(parent)
        self.setStyleSheet('border:1 solid')
        # self.setFixedSize(200,200)
        self.resize(200,200)
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(True)
        self.__initUI()
    def __initUI(self):
        self.setPixmap(QPixmap('icons/placeholder.png'))
        self.setAcceptDrops(True)
        pass
    def dragEnterEvent(self,e):
        m = e.mimeData()
        if m.hasUrls():
            e.accept()
        else:
            e.ignore()
    def dropEvent(self,e):
        
        m = e.mimeData()
        try:
            if(isImageUrl(m.urls()[0].path()) == True):
                pass
            else:
                return
        except:
            return
        
        self.setPixmap(QPixmap(m.urls()[0].toLocalFile()))

class MyWebView(MyFrame):
    def __init__(self,parent):
        super(MyWebView,self).__init__(parent)
        self.__initUI()
    def __initUI(self):
        # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled,True)
        self.layout = MyVBoxLayout(self)
        # self.webview=QWebEngineView()
        # self.webview.setUrl(QUrl("https://www.youtube.com/watch?v=Mq4AbdNsFVw"))
        # self.layout.addWidget(self.webview)
        self.show()
    def setUrl(self,url):
        # self.webview.setUrl(QUrl(url))
        self.show()

class PrevArrowWidget(QToolButton):

    def __init__(self,parent):

        super(PrevArrowWidget,self).__init__(parent)
        self.__initUI()

    def __initUI(self):
        self.setStyleSheet('border:1 solid')
        self.resize(20,150)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.Window)
        self.setArrowType(Qt.LeftArrow)
        
    def setSize(self,width,height):
        self.resize(width,height)
        pass

class MyFloatItem(MyContainer):
    
    def __init__(self,parent):

        super(MyFloatItem,self).__init__(parent)
        self.__initUI()
    
    def __initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.Window)
        pass

class CustomDialog(QDialog):

    def __init__(self, *args, **kwargs):

        super(CustomDialog, self).__init__(*args, **kwargs)
        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.bt_ok = QPushButton(self)
        self.bt_cancel = QPushButton(self)
    @staticmethod
    def showStandardMsgbox(parent,strWindowText=""):
        msg = QMessageBox(parent)
        msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.setWindowTitle("Alert")
        msg.setText(strWindowText)
        reply = msg.exec()
        if(reply == QMessageBox.Ok):
            return True
        else:
            return False

class ValidLabel(QLabel):
    
    def __init__(self,parent):

        super(ValidLabel,self).__init__(parent)
        self.__initUI()
    
    def __initUI(self):
        self.setScaledContents(True)
        self.setText("This is required")
        self.setStyleSheet('color:red')
        pass

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

    
