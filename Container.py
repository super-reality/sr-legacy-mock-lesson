import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QDialogButtonBox,QMessageBox,\
QAction, QTabWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QFrame,QLabel,QSlider,QScrollArea,QCheckBox,QSizePolicy,QFileDialog,QDockWidget,\
     QDialog,QTextEdit,QSizeGrip,QToolButton,QGraphicsOpacityEffect,QProgressBar,QTreeWidget,QTreeWidgetItem,QAbstractItemView,QAbstractScrollArea,QMenu
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon,QFont,QCursor,QPixmap,QPaintDevice,QPainter,QPen,QColor,QMouseEvent,QKeySequence
from PyQt5.QtCore import pyqtSlot, Qt, QSize,QEvent,QTimer,QPoint,pyqtSignal,QRect
from Setting import Settings
from Mybutton import TitleButton,CloseButton
from wordprocessor.wordprocessor import MyTextEditDialog
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import Qt,QUrl
from MyUtil import getPixmapFromScreen, isImageUrl,getScreenSize
from threading import Thread
import time
import MyUtil
import Globals
import os
import keyboard

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
    def __init__(self,parent,isPrefix=False):
        super(CommonHeaderLabel,self).__init__(parent)
        # self.setMaximumSize(200,100)
        self.isPrefix = isPrefix
        if(isPrefix):
            self.setMaximumSize(Settings.prefixWidth,400)
            self.setFixedWidth(Settings.prefixWidth)
        self.setWordWrap(True)
        self.setFont(QFont('Arial',14))

    def paintEvent(self,event):
        if(self.isPrefix == False):
            super(CommonHeaderLabel,self).paintEvent(event)
            return
        # painter = QPainter(self)
        # painter.setPen(QPen(Qt.black))
        # painter.drawLine(QPoint(self.width()//3,10),QPoint(self.width()//3,self.height()-10))
        # painter.drawLine(QPoint(self.width()*2//3,10),QPoint(self.width()*2//3,self.height()-10))

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
        # self.setScaledContents(True)

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
        self.setStyleSheet('border:1px solid black;margin-bottom:5px')
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
        self.textChanged.connect(self.processTextChanged)
        self.setStyleSheet('border:1px solid black')
        self.__initUI()

    def __initUI(self):
        self.setFont(QFont('Arial',16))

    def processTextChanged(self):
        size = self.document().size().toSize()
        self.setFixedHeight(max(Settings.commonRowHeightChild,size.height()+3))

class CommonFramelessWidget(QFrame):
    def __init__(self,parent):
        super(CommonFramelessWidget,self).__init__(parent)
        self.setWindowFlags(Qt.Window|Qt.FramelessWindowHint)
        self.isMousePressed = False

    def mousePressEvent(self, event):
        self.isMousePressed = True
        self.oldPos = event.globalPos()
    def mouseReleaseEvent(self,event):
        self.isMousePressed = False
    def mouseMoveEvent(self,e):
        delta = QPoint (e.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = e.globalPos()

class MySizeGrip(CommonFramelessWidget):
    
    def __init__(self,parent,position=Settings.topleft):

        super(MySizeGrip,self).__init__(parent)
        self.oldpos = None
        self.newpos = None
        self.position = position
        self.gripsize = Settings.gripSize
        self.setStyleSheet('border: 2px solid black;')
        self.limitParent = None
        self.__initUI()

    def __initUI(self):
        self.resize(Settings.gripSize,Settings.gripSize)
        
        pass
    def setLimitParent(self,parent):
        self.limitParent = parent
        pass
    
    def isLimited(self):

        if(self.limitParent is None):
            return True

        parentPosx,parentPosy = self.limitParent.mapToGlobal(QPoint(0,0)).x(),self.limitParent.mapToGlobal(QPoint(0,0)).y()
        parentWidth = self.limitParent.width()
        parentHeight = self.limitParent.height()
        self.currentPosx = self.mapToGlobal(QPoint(0,0)).x() + Settings.gripSize//2
        self.currentPosy = self.mapToGlobal(QPoint(0,0)).y() + Settings.gripSize//2
        
        if(self.currentPosx < parentPosx):
            return False
        if(self.currentPosx >= parentPosx + parentWidth):
            return False
        if(self.currentPosy < parentPosy):
            return False
        if(self.currentPosy >= parentPosy + parentHeight):
            return False
        return True


    def changeGripSize(self):
        Settings.gripSize = max(min(self.parentWidget().width(),self.parentWidget().height(),100)//5,10)
        self.resize(Settings.gripSize,Settings.gripSize)
        pass

    def processParentPositionChangeEvent(self,deltax,deltay):
        if(self.isMousePressed == False):
            self.showEvent(None)
        pass
    def showEvent(self,event):
        
        self.changeGripSize()
        # move this widget to parent's corner
        parentpos = self.parentWidget().mapToGlobal(QPoint(0,0)).x(),self.parentWidget().mapToGlobal(QPoint(0,0)).y()
        parentWidgetSize = self.parentWidget().width(),self.parentWidget().height()
        
        if(self.position == Settings.topleft):
            self.move(parentpos[0]-Settings.gripSize//2,parentpos[1]-Settings.gripSize//2)
        if(self.position == Settings.topright):
            self.move(parentpos[0]+ parentWidgetSize[0] - Settings.gripSize//2,parentpos[1]-Settings.gripSize//2)
        if(self.position == Settings.bottomleft):
            self.move(parentpos[0]-Settings.gripSize//2,parentpos[1] - Settings.gripSize//2 + parentWidgetSize[1])
        if(self.position == Settings.bottomright):
            self.move(parentpos[0] + parentWidgetSize[0] - Settings.gripSize//2,parentpos[1] - Settings.gripSize//2 + parentWidgetSize[1])
        
        self.oldpos = self.mapToGlobal(QPoint(0,0)).x(),self.mapToGlobal(QPoint(0,0)).y()

    def moveEvent(self,event):
        if(self.oldpos is None or self.isMousePressed == False):
            return
        self.changeGripSize()
        if self.isLimited() == False:
            self.move(self.oldpos[0]-Settings.gripSize//2,self.oldpos[1]-Settings.gripSize//2)
            return
        else:
            self.newpos = self.mapToGlobal(QPoint(0,0)).x()+Settings.gripSize//2,self.mapToGlobal(QPoint(0,0)).y()+Settings.gripSize//2
        #process here
        if(self.position == Settings.topleft):
            diffx = self.newpos[0] - self.oldpos[0]
            diffy = self.newpos[1] - self.oldpos[1]
            width = self.parentWidget().width()
            height = self.parentWidget().height()
            self.parentWidget().resize(width-diffx,height-diffy)
            self.parentWidget().move(*self.newpos)
            pass
        elif(self.position == Settings.topright):
            diffx = self.newpos[0] - self.oldpos[0]
            diffy = self.newpos[1] - self.oldpos[1]
            width = self.parentWidget().width()
            height = self.parentWidget().height()
            self.parentWidget().resize(width+diffx,height-diffy)
            self.parentWidget().move(self.newpos[0]-width,self.newpos[1]+diffy)
            pass
        elif(self.position == Settings.bottomleft):
            diffx = self.newpos[0] - self.oldpos[0]
            diffy = self.newpos[1] - self.oldpos[1]
            width = self.parentWidget().width()
            height = self.parentWidget().height()
            self.parentWidget().resize(width-diffx,height+diffy)
            self.parentWidget().move(self.newpos[0],self.newpos[1]-height)
            pass
        elif(self.position == Settings.bottomright):
            diffx = self.newpos[0] - self.oldpos[0]
            diffy = self.newpos[1] - self.oldpos[1]
            width = self.parentWidget().width()
            height = self.parentWidget().height()
            self.parentWidget().resize(width+diffx,height+diffy)
            self.parentWidget().move(self.newpos[0] - width,self.newpos[1] - height)
            pass
        else:
            pass

        self.oldpos = self.newpos

class MyChildAnchorWidget(CommonFramelessWidget):
    sig_moveResizeEvent = pyqtSignal(int,int)
    def __init__(self,parent):
        super(MyChildAnchorWidget,self).__init__(parent)
        #set corner's sizeGrip Objects
        if(self.parentWidget() == None):
            return
        
        #create objects
        self.topleftgrip =MySizeGrip(self,position=Settings.topleft)
        self.toprightgrip =MySizeGrip(self,position=Settings.topright)
        self.bottomrightgrip =MySizeGrip(self,position=Settings.bottomleft)
        self.bottomleftgrip =MySizeGrip(self,position=Settings.bottomright)
        self.resize(self.parentWidget().width()//2,self.parentWidget().height()//2)

        #set styles , attributes and properties
        self.setWindowOpacity(Settings.commonOpacity)
        self.setStyleSheet('border:1px solid black; border-style:dashed;background-color: #ff0074')
        self.setStyleSheet('border:1px solid red')
        self.topleftgrip.setStyleSheet('border:1px solid red')
        self.toprightgrip.setStyleSheet('border:1px solid red')
        self.bottomrightgrip.setStyleSheet('border:1px solid red')
        self.bottomleftgrip.setStyleSheet('border:1px solid red')
        
        self.topleftgrip.setLimitParent(self.parentWidget())
        self.toprightgrip.setLimitParent(self.parentWidget())
        self.bottomleftgrip.setLimitParent(self.parentWidget())
        self.bottomrightgrip.setLimitParent(self.parentWidget())


        #bind events
        self.sig_moveResizeEvent.connect(self.topleftgrip.processParentPositionChangeEvent)
        self.sig_moveResizeEvent.connect(self.toprightgrip.processParentPositionChangeEvent)
        self.sig_moveResizeEvent.connect(self.bottomleftgrip.processParentPositionChangeEvent)
        self.sig_moveResizeEvent.connect(self.bottomrightgrip.processParentPositionChangeEvent)

        self.lastChildPosx = None
        self.lastChildPosy = None
        self.lastChildWidth = None
        self.lastChildHeight = None


    def processParentMoveEvent(self,deltax,deltay):

        if(deltax is None or deltax > 10000 or deltax < 0 or deltay < 0 or deltay >10000):
            self.moveEvent(None)
        else:
            self.move(self.mapToGlobal(QPoint(0,0)).x() + deltax,self.mapToGlobal(QPoint(0,0)).y() + deltay)
        pass        
    
    def showEvent(self,event):

        self.topleftgrip.show()
        self.toprightgrip.show()
        self.bottomleftgrip.show()
        self.bottomrightgrip.show()


    def hideEvent(self,event):

        self.topleftgrip.hide()
        self.toprightgrip.hide()
        self.bottomleftgrip.hide()
        self.bottomrightgrip.hide()
        self.lastChildPosx = self.mapToGlobal(QPoint(0,0)).x()
        self.lastChildPosy = self.mapToGlobal(QPoint(0,0)).y()
        self.lastChildWidth = self.width()
        self.lastChildHeight = self.height()

    def moveEvent(self,event):
        
        parentPosx = self.parentWidget().mapToGlobal(QPoint(0,0)).x()
        parentPosy = self.parentWidget().mapToGlobal(QPoint(0,0)).y()
        parentWidth = self.parentWidget().width()
        parentHeight = self.parentWidget().height()
        
        currentPosx = self.mapToGlobal(QPoint(0,0)).x()
        currentPosy = self.mapToGlobal(QPoint(0,0)).y()
        currentWidth = self.width()
        currentHeight = self.height()
        
        newPosx = currentPosx
        newPosy = currentPosy
        newWidth = currentWidth
        newHeight = currentHeight

        
        b_isIn = False
        if parentPosx > currentPosx:
            newPosx = parentPosx
            b_isIn = True
            pass
        if parentPosx + parentWidth < currentPosx + currentWidth:
            newPosx = parentPosx + parentWidth - currentWidth
            b_isIn = True
            pass
        if parentPosy > currentPosy:
            newPosy = parentPosy
            b_isIn = True
            pass
        if parentPosy + parentHeight < currentPosy + currentHeight:
            newPosy = parentPosy + parentHeight - currentHeight
            
            b_isIn = True
        
        if(b_isIn == False):
            #if this child widget is in parent widget completely, then no action
            self.sig_moveResizeEvent.emit(None,None)
            return
        self.move(newPosx,newPosy)
        self.resize(newWidth,newHeight)
        self.sig_moveResizeEvent.emit(None,None)
        pass



class QAnchorDialog(QLabel):
    
    pixmapChanged = pyqtSignal()
    sig_mouseClick = pyqtSignal(int,int)
    sig_moveResizeEvent = pyqtSignal(int,int)

    def __init__(self,parent):
        super(QAnchorDialog,self).__init__(parent)
        #set corner's sizeGrip Objects
        self.topleftgrip =MySizeGrip(self,position=Settings.topleft)
        self.toprightgrip =MySizeGrip(self,position=Settings.topright)
        self.bottomrightgrip =MySizeGrip(self,position=Settings.bottomleft)
        self.bottomleftgrip =MySizeGrip(self,position=Settings.bottomright)
        self.childAnchor = MyChildAnchorWidget(self)
        self.resize(Settings.anchorDefaultWidth,Settings.anchorDefaultHeight)
        
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.Window)

        #set opacity
        self.ClickPointable = False
        self.isFirstShowing = True
        self.rects = []

        self.posxToEmit = None
        self.posyToEmit = None
        self.posWidthToEmit = None
        self.posHeightToEmit = None
        self.currentPixmap = None
        self.lastPosx = None
        self.lastPosy = None
        self.lastWidth = None
        self.lastHeight = None
        self.isMovable = True
        

        #set object name for style
        self.setObjectName("AnchorDlg")
        self.setStyleSheet('#AnchorDlg{border:2px solid black; border-style:dashed;background-color:#00deff}')

        self.setWindowOpacity(Settings.commonOpacity)
        # self.__initUI()
        self.childAnchor.hide()

        #event binding
        self.sig_moveResizeEvent.connect(self.topleftgrip.processParentPositionChangeEvent)
        self.sig_moveResizeEvent.connect(self.toprightgrip.processParentPositionChangeEvent)
        self.sig_moveResizeEvent.connect(self.bottomleftgrip.processParentPositionChangeEvent)
        self.sig_moveResizeEvent.connect(self.bottomrightgrip.processParentPositionChangeEvent)
        self.sig_moveResizeEvent.connect(self.childAnchor.processParentMoveEvent)
        
        
    def setMovable(self,b_movable):
        self.isMovable = b_movable
        pass
    
    def keyPressEvent(self,event):
        if(keyboard.is_pressed('ctrl+enter')):
            self.captureWindwoAtCurrentPosition()
            pass
        
    def contextMenuEvent(self,event):
        contextmenu = QMenu(self)
        contextmenu.addAction("Capture",self.captureWindwoAtCurrentPosition,'Ctrl+Enter')
        action = contextmenu.exec_(self.mapToGlobal(event.pos()))
        

    def captureWindwoAtCurrentPosition(self):
        self.mouseDoubleClickEvent(1)
        self.hide()

    def hideAllChild(self,ishide=True):
        if(ishide):
            # self.label_header.hide()
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
        self.setAttribute(Qt.WA_TranslucentBackground|Qt.WA_NoSystemBackground)
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
        self.currentPixmap = pix

        #move again to original pos
        self.pixmapChanged.emit()
        self.captureLastPos()

    def reLocating(self):
        self.hide()
        self.show()
        pass

    def mouseDoubleClickEvent(self,event):

        posx = self.mapToGlobal(QPoint(0,0)).x()
        posy = self.mapToGlobal(QPoint(0,0)).y()
        W = self.width()
        H = self.height()
        
        #hide temporarily to get image behind of this dialog
        self.hide()
        if event is not None:
            pix = getPixmapFromScreen(posx,posy,W,H)
            self.setPixmap(pix)
            self.currentPixmap = pix
        
        #move again to original pos
        self.show()
        self.move(posx + Settings.bias,posy + Settings.bias)
        self.sig_mouseClick.emit(self.posxToEmit,self.posyToEmit)
        
        if(event is not None):
            self.pixmapChanged.emit()
            self.captureLastPos()
        pass
    
    def enterEvent(self,e):
        pass

    def mouseMoveEvent(self,e):
        if(self.isMovable):
            delta = QPoint (e.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = e.globalPos()
            self.sig_moveResizeEvent.emit(delta.x(),delta.y())

    def resizeEvent(self,event):
        #if this step is mouseclickstep , calculate child width and let this parent to not be small than child anchor
        if self.ClickPointable == True:
            newWidth,newHeight = self.width(),self.height()
            if(self.width() < self.childAnchor.width()):
                newWidth = self.childAnchor.width()
            if(self.height() < self.childAnchor.height()):
                newHeight = self.childAnchor.height()
            self.resize(newWidth,newHeight)
        self.sig_moveResizeEvent.emit(None,None)

    def showEvent(self,e):
        # self.move(self.parentWidget().mapToGlobal(QPoint(220,220))+QPoint(100,0))
        self.topleftgrip.show()
        self.bottomleftgrip.show()
        self.bottomrightgrip.show()
        self.toprightgrip.show()
        if self.ClickPointable == True:
            self.childAnchor.show()
            if(self.isFirstShowing == True):
                #move to center of parent anchor
                self.isFirstShowing = False
                curposx,curposy = self.mapToGlobal(QPoint(0,0)).x(),self.mapToGlobal(QPoint(0,0)).y()
                centerx,centery = curposx + self.width()//2, curposy + self.height()//2
                self.childAnchor.move(centerx - self.width()//4,centery - self.height()//4)
                self.childAnchor.resize(self.width()//2,self.height()//2)
                self.childAnchor.processParentMoveEvent(None,None)
                pass
        pass

    def hideEvent(self,e):

        self.topleftgrip.hide()
        self.toprightgrip.hide()
        self.bottomrightgrip.hide()
        self.bottomleftgrip.hide()
        if self.ClickPointable == True:
            self.childAnchor.hide()
       

    def captureLastPos(self):
        # save last click point
        self.lastPosx = self.mapToGlobal(QPoint(0,0)).x()
        self.lastPosy = self.mapToGlobal(QPoint(0,0)).y()
        self.lastWidth = self.width()
        self.lastHeight = self.height()

    def mouseReleaseEvent(self,event):
        #if anchor is out of screen, then let it go into inside of screen
        posx = self.mapToGlobal(QPoint(0,0)).x()
        posy = self.mapToGlobal(QPoint(0,0)).y()
        screenH,screenW = getScreenSize()

        isOut = False
        if(posx<0):
            posx = 0
            isOut = True
        if((posx + self.width())>screenW):
            posx = screenW - self.width()
            isOut = True
        if(posy<0):
            posy = 0
            isOut = True
        if(posy + self.height()>screenH):
            posy = screenH - self.height()
            isOut = True
        self.move(posx,posy)
        if(isOut == True):
            self.hide()
            self.show()
        
    def drawRect(self,posx,posy,poswidth,posheight):
        
        self.posxToEmit = posx
        self.posyToEmit = posy
        self.posWidthToEmit = poswidth
        self.posHeightToEmit = posheight
        self.update()
        pass

    def paintEvent(self,event):
        #just keep pixmap but don't show it but background
        painter = QPainter(self)
        pen = QPen(QColor(*Settings.childAnchorMarkLineColor))
        pen.setWidth(Settings.childAnchorMarkLineWidth)
        painter.setPen(pen)
        if(self.posxToEmit is not None):
            painter.drawRect(self.posxToEmit,self.posyToEmit,self.posWidthToEmit,self.posHeightToEmit)

        for rect in self.rects:
            painter.drawRect(rect.x(),rect.y(),rect.width(),rect.height())
            pass
        
        # painter = QPainter(self)
        # painter.setPen(Qt.red)
        
        # if self.posxToEmit is not None and self.posyToEmit is not None:
        #     painter.drawLine(self.posxToEmit-20,self.posyToEmit,self.posxToEmit+20,self.posyToEmit)
        #     painter.drawLine(self.posxToEmit,self.posyToEmit-20,self.posxToEmit,self.posyToEmit+20)
        #     painter.drawEllipse(self.posxToEmit-20,self.posyToEmit-20,40,40)
        # else:
        #     pass


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
    def setText(self, str_In = ""):
        self.wordprocessor.editor.setText(str_In)

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
        self.setMaximumSize(400,400)
        self.resize(200,200)
        self.setAlignment(Qt.AlignCenter)
        
        self.posx = None
        self.posy = None
        self.poswidth = None
        self.posheight = None

        # self.setScaledContents(True)
        self.__initUI()
    def __initUI(self):
        self.setPixmap(QPixmap('icons/placeholder.png'))
        self.setAcceptDrops(True)
        pass
    def initLablePixmap(self):
        self.setPixmap(QPixmap('icons/placeholder.png'))
        pass
    def dragEnterEvent(self,e):
        m = e.mimeData()
        if m.hasUrls():
            e.accept()
        else:
            e.ignore()
    def setClickableArea(self,posx,posy,poswidth,posheight):

        self.posx = posx
        self.posy = posy
        self.poswidth = poswidth
        self.posheight = posheight
        self.update()

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

    def paintEvent(self,event):
        
        if(self.posx is None):
            super().paintEvent(event)
            return
        painter = QPainter(self.pixmap())
        pen = QPen(QColor(*Settings.childAnchorMarkLineColor))
        pen.setWidth(Settings.childAnchorMarkLineWidth)
        painter.setPen(pen)
        painter.drawRect(QRect(self.posx,self.posy,self.poswidth,self.posheight))
        super().paintEvent(event)
        pass

class MyDropableLableForStudent(MyDropableLable):
    sig_mousePress = pyqtSignal()
    def __init__(self,parent):
        super(MyDropableLableForStudent,self).__init__(parent)
    def mousePressEvent(self,event):
        self.sig_mousePress.emit()
        pass
    def enterEvent(self,event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        

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

class NextArrowWidget(QToolButton):

    def __init__(self,parent):

        super(NextArrowWidget,self).__init__(parent)
        self.__initUI()

    def __initUI(self):
        self.setStyleSheet('border:1 solid')
        self.resize(20,150)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.Window)
        self.setArrowType(Qt.RightArrow)
        
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

class MyRow(QWidget):

    def __init__(self, parent):
    
        super(MyRow,self).__init__(parent)
        self.__initUI()

    def __initUI(self):

        self.setStyleSheet('margin:1px;')
        self.layout = QHBoxLayout(self)
        self.layout.addStretch(1)
        pass

    def addWidget(self,item):

        self.layout.insertWidget(self.layout.count()-1,item)

        pass




class MyTree(QTreeWidget):
    sig_doubleclick = pyqtSignal(str)
    def __init__(self,parent,fromAws=False):
        # remove default arrow icon
        super(MyTree, self).__init__(parent)
        self.setHeaderHidden(True)
        self.TreeRoot = self.invisibleRootItem()
        self.setStyleSheet("""    QTreeView::branch:open:has-children:!has-siblings{image:url(icons/stack.png)}
                                  QTreeView::branch:!has-children:!has-siblings:adjoins-item{image:url(icons/stack.png)}
                                  QTreeView::branch:has-siblings:adjoins-item{image:url(icons/stack.png)}
                                  QTreeView::branch:open:has-children:has-siblings{image:url(icons/stack.png)}
                                  QTreeView::branch:closed:has-children:has-siblings{image:url(icons/stack.png)}
                                  QTreeView::branch:closed:has-children:!has-siblings{image:url(icons/stack.png)}
                                  QTreeView::branch:open:has-children{image:url(icons/stack.png)}
                                  QTreeView::branch:closed:has-children{image:url(icons/stack.png)}
                                  QTreeView::branch:open:{image:url(icons/stack.png)}
                                  QTreeView::branch:closed:{image:url(icons/stack.png)}
                                  QTreeView::branch:end:{image:url(icons/stack.png)}
                                  ;""")
        self.iconPath = Settings.getSetting()['treeiconpath']
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        
        #load initial data for treeview
        self.text_to_titem = TextToTreeItem()
        self.find_str = ""
        self.found_titem_list = []
        self.found_idx = 0
        self.fromAws = fromAws
        
        
        self.recurse_jdata(self.loadData(), self.TreeRoot)
        self.addTopLevelItem(self.TreeRoot)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        pass
    
    def recurse_jdata(self, jdata, tree_widget):
        
        text_list = []

        if isinstance(jdata, dict):
            for key, val in jdata.items():
                text_list.append(str(key))
                row_item = MyTreeItem(str(key),isParent=True)
                self.text_to_titem.append(text_list, row_item)
                tree_widget.addChild(row_item)
                self.recurse_jdata(val,row_item)
                pass
        elif isinstance(jdata, list):
            for i, val in enumerate(jdata):
                if isinstance(val,dict):
                    (key, val) = list(val.items())[0]
                    text_list.append(str(key))
                    row_item = MyTreeItem(str(key),isParent=True)
                    self.text_to_titem.append(text_list, row_item)
                    tree_widget.addChild(row_item)
                    self.recurse_jdata(val,row_item)
                    pass
                elif isinstance(val,str):
                    text_list.append(str(val))
                    row_item = MyTreeItem(str(val))
                    self.text_to_titem.append(text_list, row_item)
                    text_list.remove(str(val))
                    tree_widget.addChild(row_item)
                else:
                    pass
        elif isinstance(jdata,str):
            text_list.append(str(jdata))
            row_item = MyTreeItem(str(jdata))
            self.text_to_titem.append(text_list, row_item)
            tree_widget.addChild(row_item)
        else:
            print("This should never be reached!")

    def find_button_clicked(self,find_str):

        # find_str = self.find_box.text()

        # Very common for use to click Find on empty string
        if find_str == "":
            return

        # New search string
        if find_str != self.find_str:
            self.find_str = find_str
            self.found_titem_list = self.text_to_titem.find(self.find_str)
            self.found_idx = 0
        else:
            item_num = len(self.found_titem_list)
            self.found_idx = (self.found_idx + 1) % item_num
        try:
            self.tree_widget.setCurrentItem(self.found_titem_list[self.found_idx])
        except:
            print('Not founded node')

    def loadData(self,isAws=False):
        """ 
        Load data from api or any other data source and return json object
        """
        # return data for test
        if(self.fromAws):
            return MyUtil.getDataFromBucket()
        else:
            return MyUtil.getDataFromCurrentTeacherFolder()

    def insertItem(self,label,path,isParent):

        # newItem = MyTreeItem(text = label,isParent = isParent, iconPath = self.iconPath)
        try:
            pass
        except:
            pass

    def refresh(self,data=None):
        self.clear()
        #load initial data for treeview
        self.text_to_titem = TextToTreeItem()
        self.find_str = ""
        self.found_titem_list = []
        self.found_idx = 0
        if(data is None):
            self.recurse_jdata(self.loadData(), self.TreeRoot)
        else:
            self.recurse_jdata(data,self.TreeRoot)
        pass
    
    def dropEvent(self,event):
        
        item=self.itemAt(event.pos())
        pathSource = os.path.join(Globals.projectmgr.getTeacherProjectsLocalPath(), self.currentItem().getPath())
        
        if(item is None):
            try:
                shutil.move(pathSource,Globals.projectmgr.getTeacherProjectsLocalPath())
                super(MyTree,self).dropEvent(event)
                self.refresh()
            except:
                event.ignore()
                pass
            return
        if(item.isParent):
            pathDist = os.path.join(Globals.projectmgr.getTeacherProjectsLocalPath(), item.getPath())
            try:
                shutil.move(pathSource,pathDist)
                super(MyTree,self).dropEvent(event)
                self.refresh()
            except:
                event.ignore()
                pass
            
        else:
            event.ignore()

    def mouseDoubleClickEvent(self,event):
        
        if(self.currentItem() is not None):
            self.sig_doubleclick.emit(self.currentItem().getPath())
            pass
        
        super(MyTree,self).mouseDoubleClickEvent(event)
        
        pass




class MyTreeItem(QTreeWidgetItem):

    def __init__(self,text = 'None',iconPath='icons/directory.png',isParent = False):

        super(MyTreeItem, self).__init__()

        self.isParent = isParent
        self.setText(0,text)
        
        if(isParent):
            font = QFont('Arial',10)
            font.setBold(True)
            self.setFont(0,font)
            self.setIcon(0,QIcon(iconPath))
        else:
            font = QFont('Arial',12)
            self.setFont(0,font)

    def getPath(self):
        item = self
        paths = []
        while(item is not None):
            paths.insert(0,item.text(0))
            item = item.parent()
        curPath = ""
        for path in paths:
            curPath = os.path.join(curPath,path)
        return curPath


class TextToTreeItem:

    def __init__(self):
        self.text_list = []
        self.titem_list = []

    def append(self, text_list, titem):
        for text in text_list:
            self.text_list.append(text)
            self.titem_list.append(titem)

    # Return model indices that match string
    def find(self, find_str):

        titem_list = []
        for i, s in enumerate(self.text_list):
            if find_str in s:
                titem_list.append(self.titem_list[i])

        return titem_list


    