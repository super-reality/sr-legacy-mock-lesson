import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, 
QAction, QTabWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QFrame,QLabel,QSlider,QScrollArea,QCheckBox,QSizePolicy,QFileDialog,QDockWidget, QDialog,\
    QListWidget)
from PyQt5.QtGui import QIcon,QFont,QCursor,QPixmap,QPaintDevice,QPainter,QPen
from PyQt5.QtCore import pyqtSlot, Qt, QSize,QEvent,QTimer
from Setting import Settings
from Mybutton import *
from Container import *
import os
from MyUtil import match_image,drawRectToPixmap,convertPixmapToGray,get_marked_image,convertCV2ImageToPixmap,loadData
import logging
import win32com.client as wincl
import threading

class StudentHeaderToolBar(MyFrame):

    sig_bt_resumeplay = pyqtSignal()
    sig_bt_carmin = pyqtSignal()
    
    sig_bt_signal = pyqtSignal()
    sig_bt_question = pyqtSignal()
    sig_bt_social = pyqtSignal()
    sig_bt_speaker = pyqtSignal()
    sig_bt_search = pyqtSignal()
    
    def __init__(self,parent):

        super(StudentHeaderToolBar,self).__init__(parent)
        self.setMaximumHeight(40)
        self.__initUI()
    
    def __initUI(self):
        
        hbox = MyHBoxLayout(self)

        self.bt_resumeplay = PlayResumeButton(self)
        self.bt_carmin = CarmineButton(self)
        
        self.bt_signal = SignalButton(self)
        self.bt_question = QuestionButton(self)
        self.bt_social = SocialButton(self)
        self.bt_speaker = SpeakerButton(self)
        self.bt_search = SearchButton(self)
        
        hbox.addWidget(self.bt_resumeplay)
        hbox.addWidget(self.bt_carmin)
        hbox.addStretch(1)
        hbox.addWidget(self.bt_signal)
        hbox.addWidget(self.bt_question)
        hbox.addWidget(self.bt_social)
        hbox.addWidget(self.bt_speaker)
        hbox.addWidget(self.bt_search)

        #bind event
        self.bt_signal.clicked.connect(self.sig_bt_signal)
        self.bt_resumeplay.clicked.connect(self.sig_bt_resumeplay)
        self.bt_carmin.clicked.connect(self.sig_bt_carmin)
        self.bt_question.clicked.connect(self.sig_bt_question)
        self.bt_social.clicked.connect(self.sig_bt_social)
        self.bt_speaker.clicked.connect(self.sig_bt_speaker)
        self.bt_search.clicked.connect(self.sig_bt_search)

class CommonLessonItem(MyFrame):
    sig_ItemHeaderIcon = pyqtSignal(str,int,int,int,int)
    sig_check_bt_showTestBoxStateChanged = pyqtSignal(int)
    def __init__(self,parent,isHeader=False):

        super(CommonLessonItem,self).__init__(parent)
        self.lbl_title = CommonHeaderLabel(self)
        self.lbl_description = CommonDescriptionLabel(self)
        self.lbl_icon = CommonHeaderIcon(self)
        self.isHeader = isHeader
        if(self.isHeader):
            pass
        else:
            self.lbl_uploadImg = MyDropableLableForStudent(self)
            self.check_bt_showTestBox = MyCheckBox(self)
            self.check_bt_showTestBox.setChecked(True)
            self.check_bt_showTestBox.setText(Settings.showTextBox)
            #bind evnet
            self.check_bt_showTestBox.stateChanged.connect(self.sig_check_bt_showTestBoxStateChanged)

        self.__initUI()
        self.isChild = False
        self.anchorPixmapUrl = None
        self.posx = None
        self.posy = None
        self.posWidth = None
        self.posHeight = None



    def __initUI(self):
        
        #set layout
        self.layout = MyGridLayout(self)
        self.layout.addWidget(self.lbl_title,0,0,1,19)
        self.layout.addWidget(self.lbl_icon,0,19,1,1)
        self.layout.addWidget(self.lbl_description,1,0,1,20)
        if(self.isHeader):
            pass
        else:
            self.layout.addWidget(self.check_bt_showTestBox,2,0,1,20)
            self.layout.addWidget(self.lbl_uploadImg,3,0,20,20)
            self.check_bt_showTestBox.hide()
            self.lbl_description.setStyleSheet("border-bottom:2px solid black")

            
        #initialize properties and stylesheet
        self.setInfo("Title","Description",None)
        self.setLayout(self.layout)

        #event binding
        self.lbl_icon.mousePressEvent = self.processMatchEvent

        
    
    def processMatchEvent(self,event):
        self.sig_ItemHeaderIcon.emit(self.anchorPixmapUrl,self.posx,self.posy,self.posWidth,self.posHeight)
        th_audio = threading.Thread(target=self.playAudioFromText,daemon=True)
        th_audio.start()

    def playAudioFromText(self):
        if (self.lbl_description is not None and self.lbl_description.text() != ''):
            MyUtil.playAudioFromText(Text=self.lbl_description.text())
        pass
        
    def showEvent(self,event):
        #if clickstep show child anchor
        if(self.posx is not None):
            self.lbl_uploadImg.setClickableArea(self.posx,self.posy,self.posWidth,self.posHeight)
        else:
            pass

    def display(self,isminimized=False):

        if(isminimized):
            self.lbl_icon.hide()
            self.lbl_description.hide()
            if(self.isHeader):
                pass
            else:
                self.lbl_uploadImg.hide()
        else:
            self.lbl_icon.show()
            self.lbl_description.show()
            if(self.isHeader):
                pass
            else:
                self.lbl_uploadImg.hide()
    
    def setInfo(self,title,description,iconPath,anchorUrl=None):
        self.lbl_title.setText(title)
        self.lbl_description.setText(description)
        if(iconPath is not None):
            self.lbl_icon.setPixmap(QPixmap(iconPath))
        if(anchorUrl is not None):
            self.lbl_uploadImg.setPixmap(QPixmap(anchorUrl))

class CommonLessonOverview(CommonLessonItem):
    
    def __init__(self,parent):

        super(CommonLessonOverview,self).__init__(parent,isHeader=True)
        self.isMinimized = False
        self.__initUI()
    
    def __initUI(self):
        self.layout.removeWidget(self.lbl_icon)
        self.layout.addWidget(self.lbl_icon,0,19,2,1)
        # self.lbl_icon.setPixmap(QPixmap('icons/lookstep.png'))
    
    def mousePressEvent(self,event):
        if(self.isMinimized):
            self.lbl_icon.hide()
            self.lbl_description.hide()
        else:
            self.lbl_icon.show()
            self.lbl_description.show()
        self.isMinimized = not self.isMinimized

class CommonLessonLookStepItem(CommonLessonItem):
    
    def __init__(self,parent):

        super(CommonLessonLookStepItem,self).__init__(parent)
        self.__initUI()
    
    def __initUI(self):

        self.lbl_icon.setPixmap(QPixmap('icons/lookstep.png'))    

class CommonLessonClickStepItem(CommonLessonItem):

    sig_ImageClicked = pyqtSignal()
    sig_showed = pyqtSignal()

    def __init__(self,parent):
        super(CommonLessonClickStepItem,self).__init__(parent)
        #change image component with new one

        self.isFirstShow = True
        self.matchText = None
        self.anchorDiaglog = QAnchorDialog(self)
        self.anchorDiaglog.isTextMatch = True
        self.isCheckedTestbox = True
        self.__initUI()    

        #bind event
        self.lbl_uploadImg.sig_mousePress.connect(self.sig_ImageClicked)
        self.lbl_uploadImg.sig_mousePress.connect(self.processTextMatch)
        self.sig_check_bt_showTestBoxStateChanged.connect(self.check_bt_showTestBoxChanged)
        self.anchorDiaglog.pixmapChanged.connect(self.processchangedPixmap)
        if(self.lbl_uploadImg is not None):
            self.lbl_uploadImg.mousePressEvent = self.processMatchEvent

    def hideEvent(self,event):
        self.anchorDiaglog.hide()
        super(CommonLessonClickStepItem,self).hideEvent(event)

    def processchangedPixmap(self):

        if(self.anchorDiaglog.currentPixmap is None or self.matchText is None):
            return
        
        pixmap = self.anchorDiaglog.currentPixmap
        cv2_image = convertPixmapToGray(pixmap.copy(),isgray=False)
        rects = get_marked_image(self.matchText,cv2_image)
        self.anchorDiaglog.rects = rects.copy()
        self.anchorDiaglog.update()
        
    def check_bt_showTestBoxChanged(self,event):
        
        if(event):
            self.isCheckedTestbox = True
        else:
            self.isCheckedTestbox = False
            self.anchorDiaglog.hide()  
    
    def processTextMatch(self):
        
        if(self.isCheckedTestbox == True):
            self.anchorDiaglog.setClickPoint(False)
            self.anchorDiaglog.show()
        else:
            self.anchorDiaglog.hide()
            pass

    def __initUI(self):

        self.lbl_icon.setPixmap(QPixmap('icons/clickstep.png'))

    def showEvent(self,event):

        if(self.matchText is not None):

            self.check_bt_showTestBox.show()
        else:
            self.check_bt_showTestBox.hide()

        super(CommonLessonClickStepItem,self).showEvent(event)
        self.sig_showed.emit()
        pass

    def display(self,isminimized=False):

        super(CommonLessonClickStepItem,self).display(isminimized)

class CommonLessonMatchStepItem(CommonLessonItem):
    
    def __init__(self,parent):
        super(CommonLessonMatchStepItem,self).__init__(parent)
        self.__initUI()
        self.lbl_icon.setPixmap(QPixmap('icons/matchstep.png'))
        
    def __initUI(self):
        
        self.lbl_uploadImg = MyDropableLable(self)
        self.layout.addWidget(self.lbl_uploadImg,2,0,1,20)

class CommonLessonMouseStepItem(CommonLessonItem):
    
    def __init__(self,parent):
    
        super(CommonLessonMouseStepItem,self).__init__(parent)
        
        self.__initUI()
        self.lbl_icon.setPixmap(QPixmap('icons/mousestep.png'))
        
    def __initUI(self):
        self.lbl_uploadImg = MyDropableLable(self)
        self.lbl_uploadImg.setAlignment(Qt.AlignCenter)
        self.lbl_uploadImg.setWindowFlags(Qt.FramelessWindowHint|Qt.Window)
        self.lbl_uploadImg.setAttribute(Qt.WA_TranslucentBackground)
        self.lbl_uploadImg.setScaledContents(True)
        self.lbl_uploadImg.move(400,400)
        
    def setInfo(self,title,description,iconPath):
        super(CommonLessonMouseStepItem,self).setInfo(title,description,iconPath)
        self.setMouseStepImage()
        pass
    def setMouseStepImage(self,isCurrentItem=False):
        if(self.lbl_title.text() == Settings.scrollDown):
            #set image as scroll down
            self.lbl_uploadImg.setPixmap(QPixmap('icons/scrolldown.png'))
        elif(self.lbl_title.text() == Settings.scrollUp):
            #set image as scroll up
            self.lbl_uploadImg.setPixmap(QPixmap('icons/scrollup.png'))
        else:
            pass
    
    def hideEvent(self,event):
        self.lbl_uploadImg.hide()
        super(CommonLessonMouseStepItem,self).hide()
    def showEvent(self,event):
        # self.lbl_uploadImg.show()
        super(CommonLessonMouseStepItem,self).show()
    
class CommonLessonAttachStepItem(CommonLessonItem):
    def __init__(self,parent):

        super(CommonLessonAttachStepItem,self).__init__(parent)
        self.__initUI()

    def __initUI(self):
        self.lbl_webview = MyWebView(self)
        # self.lbl_webview.setFixedSize(200,200)
        self.lbl_icon.setPixmap(QPixmap('icons/attachstep.png'))
        self.layout.addWidget(self.lbl_webview,2,0,1,20)

class CommonLessonPiskelStepItem(CommonLessonItem):

    def __init__(self,parent):
    
        super(CommonLessonPiskelStepItem,self).__init__(parent)
        self.lbl_referUrl = CommonDescriptionLabel('wwww.piskelapp.com')
        self.__initUI()
        self.lbl_icon.setPixmap(QPixmap('icons/lookstep.png'))

    
    def __initUI(self):

        pass
    
class StudentBodyWidget(MyContainer):
    resetEvent = pyqtSignal(str)
    sig_imageconverted = pyqtSignal(QPixmap)
    def __init__(self,parent):
    
        super(StudentBodyWidget,self).__init__(parent)
        self.prevItem = PrevArrowWidget(self)
        self.nextArrowWidget = NextArrowWidget(self)
        self.itemHeader = None
        self.currentItem = None
        self.layout = None
        self.itemList = None
        self.nextItem = None
        self.nestedItems = []
        self.currentAnchorPixmapUrl = None
        
        #set timer
        # self.timer = QTimer(self)
        # self.timer.setInterval(1000)
        # self.timer.timeout.connect(self.processAnchorAnimation)
        # self.timer.start()
        self.step = 0

        self.anchorDlg = QLabel(self)
        self.anchorDlg.setWindowFlags(Qt.FramelessWindowHint|Qt.Dialog)
        self.anchorDlg.setAttribute(Qt.WA_TranslucentBackground)
        self.anchorDlg.setScaledContents(True)
        self.anchorDlg.enterEvent = self.processAnchorWindowEnterEvent
        self.sig_imageconverted.connect(self.sig_imageconvertedProcess)

        #event binding
        self.window().moveEvent = self.processMoveEvent

    def processAnchorWindowEnterEvent(self,event):
        self.anchorDlg.hide()
        pass
    def sig_imageconvertedProcess(self,pix):
        print(type(pix).__name__,"chekcmkmerhe1")
        self.anchorDlg.setPixmap(pix)
        pass
    def processMatchByAnchor(self,anchorUrl,posx=None,posy=None,posWidth=None,posHeight=None):
        logging.info("anchor url is :" + anchorUrl)
        if(anchorUrl is not None):
            self.currentAnchorPixmapUrl = (anchorUrl)
        else:
            return 
        if(self.currentAnchorPixmapUrl is not None):
            found = 0
            try:
                (found,X,Y,W,H,R) = match_image(self.currentAnchorPixmapUrl,self.window().x(),self.window().y(),self.window().width(),self.window().height())
            except:
                logging.error("cv template matching issue")

            if(found == 0):
                logging.info('can \'t find the matching image')
                return
            else:
                logging.info('Oh cool find the matching image')
                pass
            logging.info("click point pos  is : %s, %s",posx,posy)
            if posx <1000  and posy <1000 and posx >0 and posy >0:
                cv_image = Globals.effectEngine.drawRect(posWidth,posHeight)
                if(cv_image is None):
                    return
                h,w,_ = cv_image.shape
                self.anchorDlg.resize(w,h)
                X = X + posx
                Y = Y + posy
                self.anchorDlg.move(X-(w-posWidth)//2,Y-(h-posHeight)//2)
                cv_image = MyUtil.makeTransparentFromMask(cv_image)
                image = MyUtil.convertCV2ImageToPixmap(cv_image.copy(),self)
                self.anchorDlg.clear()
                self.anchorDlg.setPixmap(QPixmap(image))
            else:
                #set opacity
                cv_image = Globals.effectEngine.drawRect(H,W)

                if(cv_image is None):
                    return
                
                h,w,_ = cv_image.shape
                self.anchorDlg.resize(w,h)
                X = X-(w-H)//2
                Y = Y-(h-W)//2
                self.anchorDlg.move(X,Y)
                cv_image = MyUtil.makeTransparentFromMask(cv_image)
                image = MyUtil.convertCV2ImageToPixmap(cv_image.copy(),self)
                self.anchorDlg.clear()
                self.anchorDlg.setPixmap(QPixmap(image))
                pass
            
            self.step = 1
            self.anchorDlg.show()
            #############check me here this is for test
            pass
        else:
            pass

    def processTextMatch(self):
        #popup window.
        
        pass

    def processAnchorAnimation(self):

        if((self.step > 7 and self.step < 9) or self.step ==0):
            if(self.anchorDlg is not None):
                self.anchorDlg.hide()
            return
        if(self.step%2):
            logging.info("anchor dialgo is showing now")
            self.anchorDlg.show()
        else:
            logging.info("anchor dialgo is hiding now")
            self.anchorDlg.hide()
        self.step = self.step + 1

        pass

    def currentProjectChanged(self,name):
        self.projectPath = os.path.join(os.getcwd(),Settings.projectStudentPath)
        self.projectPath = os.path.join(self.projectPath,name)
        if(MyUtil.isLeaf(self.projectPath)):
            self.initializeObject(self.projectPath)
        else:
            #alert pls select a valid project file
            pass
        pass

    def initializeObject(self,projectPath):
        self.prevItem.hide()
        self.nextArrowWidget.hide()
        self.resetEvent.emit("")
        if(projectPath is None):
            return
        self.currentItem = None
        self.nextItem = None
        self.nestedItems = []
        self.clearLayout()
        projectfilePath = os.path.join(projectPath,Settings.projectFileName)
        self.loadData(projectfilePath)
        if(self.data is None):
            return
        self.__initUI()
        pass

    def clearLayout(self):
        if self.layout is not None:
            while self.layout.count():
                child = self.layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

    def loadData(self,projectfilePath):

        self.data = loadData(projectfilePath)

    def __initUI(self):
        
        self.imageBaseUrl = self.data.metaInfo.baseImgUrl
        
        #initializeHeader
        self.itemHeader = CommonLessonOverview(self)
        if self.data.header.anchorImageName is None:
            self.itemHeader.setInfo(self.data.header.title,self.data.header.description,None)
            pass
        else:
            self.itemHeader.setInfo(self.data.header.title,self.data.header.description,os.path.join(self.projectPath, self.data.header.anchorImageName))
            self.itemHeader.anchorPixmapUrl = os.path.join(self.projectPath,self.data.header.anchorImageName)
            self.itemHeader.sig_ItemHeaderIcon.connect(self.processMatchByAnchor)
        
        #adds listwidgets to layout
        if(self.layout is None):
            self.layout = MyVBoxLayout(self)
        self.layout.addWidget(self.itemHeader)


        self.itemList = []
        for idx in range(len(self.data.lessons)):
            if(self.data.lessons[idx].type == Settings.lookStep):
                curInfo = self.data.lessons[idx]
                item = CommonLessonLookStepItem(self)
                item.setInfo(curInfo.title,curInfo.description,None)
                if(curInfo.anchorPixmap is None):
                    item.anchorPixmapUrl = None
                    pass
                else:
                    item.anchorPixmapUrl = os.path.join(self.projectPath,curInfo.anchorPixmap)
                item.hide()
                self.layout.addWidget(item)
                self.itemList.append(item)
                item.installEventFilter(self)
                item.isChild = (curInfo.isChild == "true")
                item.sig_ItemHeaderIcon.connect(self.processMatchByAnchor)
                pass
            elif(self.data.lessons[idx].type == Settings.clickStep):

                curInfo = self.data.lessons[idx]
                item = CommonLessonClickStepItem(self)
                item.sig_showed.connect(self.currentItemshowed)
                if(curInfo.anchorPixmap is None):
                    item.anchorPixmapUrl = None
                    pass
                else:
                    item.anchorPixmapUrl = os.path.join(self.projectPath,curInfo.anchorPixmap)
                item.setInfo(curInfo.title,curInfo.description,None,anchorUrl=item.anchorPixmapUrl)
                try:
                    if(curInfo.matchText is not None and curInfo.matchText != ""):
                        item.matchText = curInfo.matchText
                    else:
                        item.matchText = None
                except:
                    pass
                item.hide()

                self.layout.addWidget(item)
                self.itemList.append(item)
                item.installEventFilter(self)
                # item.isChild = (curInfo.isChild == "true")
                try:
                    item.posx = curInfo.spotposx
                    item.posy = curInfo.spotposy
                    item.posWidth = curInfo.spotwidth
                    item.posHeight = curInfo.spotheight
                except:
                    pass
                item.sig_ItemHeaderIcon.connect(self.processMatchByAnchor)
                item.sig_ImageClicked.connect(self.processTextMatch)

                pass
            elif(self.data.lessons[idx].type == Settings.matchStep):
                curInfo = self.data.lessons[idx]
                item = CommonLessonMatchStepItem(self)
                item.setInfo(curInfo.title,curInfo.description,None)
                if(curInfo.anchorPixmap is None):
                    item.anchorPixmapUrl = None
                    pass
                else:
                    item.anchorPixmapUrl = os.path.join(self.projectPath,curInfo.anchorPixmap)
                    item.lbl_uploadImg.setPixmap(QPixmap(os.path.join(self.projectPath,curInfo.anchorPixmap)))
                item.hide()
                self.layout.addWidget(item)
                self.itemList.append(item)
                item.installEventFilter(self)
                item.isChild = (curInfo.isChild == "true")
                item.sig_ItemHeaderIcon.connect(self.processMatchByAnchor)
                pass
            elif(self.data.lessons[idx].type == Settings.mouseStep):
                curInfo = self.data.lessons[idx]
                item = CommonLessonMouseStepItem(self)
                item.setInfo(curInfo.title,curInfo.description,None)
                if(curInfo.anchorPixmap is None):
                    item.anchorPixmapUrl = None
                    pass
                else:
                    item.anchorPixmapUrl = os.path.join(self.projectPath,curInfo.anchorPixmap)
                item.hide()
                self.layout.addWidget(item)
                self.itemList.append(item)
                item.installEventFilter(self)
                item.isChild = (curInfo.isChild == "true")
                item.sig_ItemHeaderIcon.connect(self.processMatchByAnchor)
                pass
            elif(self.data.lessons[idx].type == Settings.attachStep):
                curInfo = self.data.lessons[idx]
                item = CommonLessonAttachStepItem(self)
                item.lbl_webview.setUrl(curInfo.referUrl)
                item.hide()
                self.layout.addWidget(item)
                self.itemList.append(item)
                item.installEventFilter(self)
                item.isChild = (curInfo.isChild == "true")
                item.sig_ItemHeaderIcon.connect(self.processMatchByAnchor)
                pass
            elif(self.data.lessons[idx].type == Settings.piskelStep):
                curInfo = self.data.lessons[idx]
                item = CommonLessonPiskelStepItem(self)
                item.setInfo(title=curInfo.title,description=curInfo.description,iconPath=None)
                item.lbl_referUrl.setText(curInfo.referUrl)
                item.hide()
                self.layout.addWidget(item)
                self.itemList.append(item)
                item.installEventFilter(self)
                item.isChild = (curInfo.isChild == "true")
                item.sig_ItemHeaderIcon.connect(self.processMatchByAnchor)
                pass
            else:
                pass
        
        self.layout.addStretch(1)

        #event binding
        self.itemHeader.mousePressEvent = self.processMoveEvent
        self.prevItem.clicked.connect(self.gotoPrev)
        self.nextArrowWidget.installEventFilter(self)
    
    def currentItemshowed(self):
        #pls code here after current item showed but it has no width and height
        pass

    def showEvent(self,event):
        if(self.itemHeader is not None):
            self.itemHeader.show()
        pass

    def hideAllNextAndNestedItems(self,isHide=True):
        
        if(isHide == True and self.nextItem is not None):
            self.nextItem.hide()
            self.nextArrowWidget.hide()
            if(self.nestedItems is not None):
                for item in self.nestedItems:
                    item.hide()
            pass
        elif(isHide == False and self.nextItem is not None):
            # self.nextItem.show()
            self.nextArrowWidget.show()
            if(self.nestedItems is not None):
                for item in self.nestedItems:
                    item.show()
            pass

    def eventFilter(self,source,event):
        
        if((event.type() == QEvent.Enter and source == self.currentItem and self.currentItem is not None) or (event.type() == QEvent.MouseButtonPress and source == self.currentItem and self.currentItem is not None)):
            #view prev and next
            self.setNextItemFloating(True)
            self.hideAllNextAndNestedItems(False)
            pass
        # elif(event.type() == QEvent.MouseButtonPress and source == self.nextItem):
        #     #process press event in next item
        #     self.currentItem.hide()
        #     self.setNextItemFloating(False)
        #     self.currentItem = self.nextItem
        #     self.currentItemChanged()
        elif(event.type() == QEvent.MouseButtonPress and source == self.nextArrowWidget):
            if(self.nextItem is None):
                return super(StudentBodyWidget,self).eventFilter(source,event)
            self.currentItem.hide()
            self.currentItem = self.nextItem
            self.currentItemChanged()
        elif(event.type() == QEvent.MouseButtonPress and self.nestedItems is not None):
            #process press event in nested item
            if(source in self.nestedItems):
                source.display(False)
                pass
            else:
                pass
        elif(event.type() == QEvent.Show and source == self.currentItem):
            self.movePrevItem()
            self.moveNextItem()
            pass
        else:
            pass
        return super(StudentBodyWidget,self).eventFilter(source,event)

    def movePrevItem(self):
        self.prevItem.setSize(self.prevItem.width(),self.currentItem.lbl_icon.height()+self.currentItem.lbl_description.height() + Settings.arrowwidgetCalibrate)
        # self.prevItem.setSize(self.prevItem.width(),self.currentItem.lbl_icon.sizeHint().height()+Settings.commonRowHeightChild)
        self.prevItem.move(self.mapToGlobal(QPoint(0,0))-QPoint(self.prevItem.width(),-Settings.delta))
        self.prevItem.show()
      
    def moveNextItem(self):
        self.nextArrowWidget.setSize(self.nextArrowWidget.width(),self.currentItem.lbl_icon.height()+self.currentItem.lbl_description.height() + Settings.arrowwidgetCalibrate)
        # self.nextArrowWidget.setSize(self.nextArrowWidget.width(),self.currentItem.lbl_icon.sizeHint().height()+Settings.commonRowHeightChild)
        self.nextArrowWidget.move(self.mapToGlobal(QPoint(0,0)) + QPoint(self.window().width() - self.nextArrowWidget.width()//2,Settings.delta))
        self.nextArrowWidget.show()

    def play(self,event):
        if(self.itemHeader is not None):
            self.itemHeader.display(isminimized=True)
        if(self.currentItem is not None):
            self.currentItem.hide()
        if(self.itemList is not None):
            if(len(self.itemList) > 0):
                self.currentItem = self.itemList[0]
                self.currentItemChanged()

        #event binding
    
    def hideEvent(self,event):
        self.hideAll()

    def hideAll(self):

        self.hideAllNextAndNestedItems(False)
        if(self.currentItem is not None):
            self.currentItem.hide()
        if(self.prevItem is not None):
            self.prevItem.hide()
        if(self.itemHeader is not None):
            self.itemHeader.hide()
        if(self.nextItem is not None):
            self.nextItem.hide()
        if(self.nextArrowWidget is not None):
            self.nextArrowWidget.hide()
        for item in self.nestedItems:
            item.hide()

    def currentItemChanged(self):
        
        #hide all nested items and next item
        self.hideAllNextAndNestedItems(True)
        self.currentItem.hide()
        self.currentItem.show()
        self.currentAnchorPixmapUrl = self.currentItem.anchorPixmapUrl
        self.movePrevItem()
        
        #change nested items and next item in itemList
        length = self.itemList.__len__()
        idx = self.itemList.index(self.currentItem)
        sign_next = False
        sign_nested = False

        for index in range(idx+1, length):
            if(self.itemList[index].isChild == True):
                sign_nested = True
                print("here nested item")
                self.nestedItems.append(self.itemList[index])
            else:
                sign_next = True
                self.nextItem = self.itemList[index]
                break

        if(sign_next == False):
            self.nextItem = None
        if(sign_nested == False):
            self.nestedItems = []

        if(self.nextItem == None):
            self.nextArrowWidget.hide()
        else:
            self.moveNextItem()
        #if current item is mousestepitem, then show mouse image
        if type(self.currentItem).__name__ == "CommonLessonMouseStepItem":
            if(self.currentItem.lbl_title.text() == Settings.scrollUp or self.currentItem.lbl_title.text() == Settings.scrollDown):
                self.currentItem.lbl_uploadImg.show()
            else:
                self.currentItem.lbl_uploadImg.hide()
            pass

    def setNextItemFloating(self,isFloat=False):
        
        if(isFloat == True and self.nextItem is not None):
            # self.nextItem.setWindowFlags(Qt.FramelessWindowHint|Qt.Window)
            self.nextItem.resize(self.currentItem.width(),self.nextItem.sizeHint().height())
            self.processMoveEvent(None)
            # self.nextItem.show()
        else:
            if(self.nextItem is not None):
                self.nextItem.setWindowFlags(Qt.Widget)
                # self.nextItem.show()

    def processMoveEvent(self,event):

        if(self.prevItem is not None and self.currentItem is not None):
            self.prevItem.move(self.currentItem.mapToGlobal(QPoint(0,0))-QPoint(self.prevItem.width(),4))
            
            if( self.currentItem.isHidden() == False):
                ######################  float next item to next current item #####################
                # self.nextItem.move(self.currentItem.mapToGlobal(QPoint(0,0))+QPoint(self.currentItem.width()+4,-4))
                self.moveNextItem()
                #########################
        pass

    def gotoPrev(self,event):
        idx = self.itemList.index(self.currentItem)
        if(idx == 0):
            #go to main page.
            if(self.prevItem is not None):
                self.prevItem.hide()
            if(self.nextItem is not None):
                self.nextItem.hide()
            if(self.nextArrowWidget is not None):
                self.nextArrowWidget.hide()

            if(self.nestedItems is not None):
                for item in self.nestedItems:
                    item.hide()
            self.currentItem.hide()
            self.itemHeader.display(isminimized=False)
            # emit reset event.
            self.resetEvent.emit("")
        else:
            self.currentItem.hide()

            while(idx >= 0):
                if(self.itemList[idx-1].isChild == True):
                    idx = idx -1
                    continue
                else:
                    self.currentItem = self.itemList[idx-1]
                    break
            self.currentItemChanged()
            pass

class MyProjectListWidget(QListWidget):
    def __init__(self,parent):
        super(MyProjectListWidget,self).__init__(parent)
        self.__initUI()    
        self.setFont(QFont('Arial',14))
    def __initUI(self):
        pass

class StudentProjectList(MyContainer):

    sig_CurrentProjectChanged = pyqtSignal(str)

    def __init__(self,parent):

        super(StudentProjectList,self).__init__(parent)
        self.__initUI()

        pass               
    def __initUI(self):

        self.projectList = MyTree(self,fromAws=True)
        self.vbox = MyVBoxLayout(self)
        self.vbox.addWidget(self.projectList)
        
        #event binding
        self.projectList.currentItemChanged.connect(self.currentItemChanged)
        #set style sheet
        self.setContentsMargins(10,0,10,0)
        
        
        pass
    def currentItemChanged(self,cur,prev):
        
        pass


    def display(self,projectNameList=[]):
        # self.projectList.refresh()
        pass
        
    def getCurrentPath(self):
        if(self.projectList.currentItem() is None):
            return None
        return self.projectList.currentItem().getPath()

class StudentTabWidget(MyContainer):

    sig_bt_resumeplay = pyqtSignal()
    sig_bt_carmin = pyqtSignal()
    
    sig_bt_signal = pyqtSignal()
    sig_bt_question = pyqtSignal()
    sig_bt_social = pyqtSignal()
    sig_bt_speaker = pyqtSignal()
    sig_bt_search = pyqtSignal()
    sig_bt_resumeplay_with_Path = pyqtSignal(str)
    sig_doublClickedItem = pyqtSignal(str)
    

    def __init__(self,parent):
        super(StudentTabWidget,self).__init__(parent)
        self.__initUI()

    def __initUI(self):

        vbox = MyVBoxLayout(self)
        self.studentToolBar = StudentHeaderToolBar(self)
        self.studentBody  =  StudentBodyWidget(self)
        self.studentList = StudentProjectList(self)
        
        vbox.addWidget(self.studentToolBar)
        vbox.addWidget(self.studentBody)
        vbox.addWidget(self.studentList)
        vbox.addStretch(1)

        # hide some items at start.
        self.studentList.hide()
        #bind event.
        self.studentList.sig_CurrentProjectChanged.connect(self.studentBody.currentProjectChanged)
        # self.sig_bt_resumeplay.connect(self.showSelectedLesson)

        self.studentToolBar.sig_bt_resumeplay.connect(self.processPlayResume)
        self.studentBody.resetEvent.connect(self.processResetEvent)
        self.studentToolBar.sig_bt_signal.connect(self.sig_bt_signal)
        self.studentToolBar.sig_bt_resumeplay.connect(self.sig_bt_resumeplay)
        self.studentToolBar.sig_bt_carmin.connect(self.sig_bt_carmin)
        self.studentToolBar.sig_bt_question.connect(self.sig_bt_question)
        self.studentToolBar.sig_bt_social.connect(self.sig_bt_social)
        self.studentToolBar.sig_bt_speaker.connect(self.sig_bt_speaker)
        self.studentToolBar.sig_bt_search.connect(self.sig_bt_search)
        self.studentList.projectList.sig_doubleclick.connect(self.sig_doublClickedItem)
        
        pass
    
    def changeStatePlayButton(self):
        self.studentToolBar.bt_resumeplay.changeState()
        pass
    
    def changeProjectPathForLesson(self,pathToProject=None):
        if(pathToProject is None):
            return 
        self.studentBody.currentProjectChanged(pathToProject)
        self.studentBody.play(None)
        self.showSelectedLesson()

    def getCurrentPath(self):
        return self.studentList.getCurrentPath()
        pass
    
    def refresh(self,data=None):
        self.studentList.projectList.refresh(data)
        pass

    def setupProjectList(self,projectNameList):
        self.studentList.display(projectNameList)
        self.showProjectList()

    def showSelectedLesson(self):
        self.studentBody.show()
        self.studentList.hide()

    def getNameSelectedProject(self):
        self.studentList.getSelectedItemName()

    def showProjectList(self):
        self.studentList.show()
        self.studentBody.hide()

    def processPlayResume(self):
        if self.studentToolBar.bt_resumeplay.isPlaying == True:
            self.sig_bt_resumeplay_with_Path.emit(self.studentList.getCurrentPath())
            # self.studentBody.play(None)
        else:
            if(self.studentBody.currentItem is not None):
                self.studentBody.currentItem.hide()
            if(self.studentBody.prevItem is not None):
                self.studentBody.prevItem.hide()
            self.studentBody.hideAllNextAndNestedItems()
    
    def processResetEvent(self):
        self.studentToolBar.bt_resumeplay.reset()
        # self.studentToolBar.bt_resumeplay.changeState()

    def hideEvent(self,event):
        self.studentList.hide()
        self.studentBody.hide()
        
