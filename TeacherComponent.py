import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QMessageBox,\
QAction, QTabWidget,QGridLayout,QFrame,QLabel,QSlider,QScrollArea,QCheckBox,QSizePolicy,QFileDialog,QDockWidget, QDialog,QTreeView,\
    QLineEdit, QTreeWidget, QTreeWidgetItem,QAbstractItemView,QAbstractScrollArea,QPlainTextEdit,QRadioButton,QInputDialog
from PyQt5.QtGui import QIcon,QFont,QCursor,QPixmap,QPaintDevice,QPainter,QPen
from PyQt5.QtCore import pyqtSlot, Qt, QSize,QEvent,QTimer,pyqtSignal, QPoint
from Setting import Settings
from Mybutton import *
from Container import *
from PyQt5 import QtWidgets
import os
import Globals
import MyUtil
import shutil
import logging


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


class HeaderClickable(CommonHeaderLabel):
    def __init__(self,parent,label):
        super(HeaderClickable, self).__init__(parent)
        self.lable = label
        self.maxLen = 20
        self.__initUI()
    def __initUI(self):
        if(len(self.lable)>self.maxLen):
            self.lable = self.lable[:self.maxLen] + "..."
        self.setText(self.lable)
    def enterEvent(self,e):
        self.setCursor(QCursor(Qt.PointingHandCursor))
    def mousePressEvent(self,event):
        pass


class TeacherFirstToolbar(MyFrame):

    def __init__(self,parent):
        super(TeacherFirstToolbar, self).__init__(parent)
        self.__initUI()
        
    def __initUI(self):
        hbox = MyHBoxLayout(self)
        self.bt_book  = BookButton(self)
        self.bt_search = SearchButton(self)
        hbox.addWidget(self.bt_book)
        hbox.addStretch(1)
        hbox.addWidget(self.bt_search)
        hbox.setContentsMargins(0,0,0,0)
        return hbox

class TeacherSecondToolbar(MyFrame):
    sig_NewProject = pyqtSignal()
    sig_newFolder = pyqtSignal()
    sig_EditProject = pyqtSignal()
    sig_DeleteProject = pyqtSignal()
    sig_SearchProject = pyqtSignal()
    sig_Social = pyqtSignal()
    sig_UploadToCloud = pyqtSignal()
    sig_PlayResume = pyqtSignal()

    def __init__(self,parent):
        super(TeacherSecondToolbar, self).__init__(parent)
        self.__initUI()
        
    def __initUI(self):
        hbox = MyHBoxLayout(self)
        self.bt_newfolder = NewFolderButton(self)
        self.bt_newProject = NewProjectButton(self)
        self.bt_edit  = EditButton(self)
        self.bt_delete = DeleteButton(self)
        self.bt_searchplus = SearchPlusButton(self)

        self.bt_social = SocialButton(self)
        self.bt_cloud = CloudButton(self)
        self.bt_resume = PlayResumeButton(self)

        hbox.addWidget(self.bt_newfolder)
        hbox.addWidget(self.bt_newProject)
        hbox.addWidget(self.bt_edit)
        hbox.addWidget(self.bt_delete)
        hbox.addWidget(self.bt_searchplus)
        
        hbox.addStretch(1)
        hbox.addWidget(self.bt_social)
        hbox.addWidget(self.bt_cloud)
        hbox.addWidget(self.bt_resume)
        hbox.setContentsMargins(0,0,0,0)

        #bind event
        self.bt_newfolder.clicked.connect(self.sig_newFolder)
        self.bt_newProject.clicked.connect(self.sig_NewProject)
        self.bt_edit.clicked.connect(self.sig_EditProject)
        self.bt_delete.clicked.connect(self.sig_DeleteProject)
        self.bt_searchplus.clicked.connect(self.sig_SearchProject)
        self.bt_social.clicked.connect(self.sig_Social)
        self.bt_cloud.clicked.connect(self.sig_UploadToCloud)
        self.bt_resume.clicked.connect(self.sig_PlayResume)
        return hbox

class TeacherSecondLessonToolbar(MyFrame):
    def __init__(self,parent):
        super(TeacherSecondLessonToolbar,self).__init__(parent,)
        self.__initUI()
        
    def __initUI(self):

        hbox = MyHBoxLayout(self)
        self.bt_lookstep = LookStepButton(self)
        self.bt_clickstep = ClickStepButton(self)
        self.bt_matchstep = MatchStepButton(self)
        self.bt_mousestep = MouseStepButton(self)
        self.bt_attachstep = AttachStepButton(self)
        self.bt_delete = DeleteButton(self)

        self.bt_cloudbutton = CloudButton(self)
        self.bt_playbutton = PlayButton(self)


        # hbox.addWidget(bt_edit)
        hbox.addWidget(self.bt_lookstep)
        hbox.addWidget(self.bt_clickstep)
        hbox.addWidget(self.bt_matchstep)
        hbox.addWidget(self.bt_mousestep)
        hbox.addWidget(self.bt_attachstep)
        hbox.addStretch(1)
        hbox.addWidget(self.bt_delete)
        
        hbox.addStretch(1)
        hbox.addWidget(self.bt_cloudbutton)
        hbox.addWidget(self.bt_playbutton)

        #Lookstep and mousestep seems to be not needed #checkmehere
        self.bt_lookstep.hide()
        self.bt_mousestep.hide()
        self.bt_matchstep.hide()
        self.bt_cloudbutton.hide()
        self.bt_attachstep.hide()
        return hbox

class Teacher_LookStep_SecondToolBar(MyFrame):
    # This is lesson page
    def __init__(self,parent):

        super(Teacher_LookStep_SecondToolBar,self).__init__(parent)

        self.isPixmapSelected = False
        self.currentPixmap = None

        self.__initUI()
        

    def __initUI(self):

        gbox = MyGridLayout(self)
        self.edit_lesson_title = QLineEdit(self)
        self.edit_lesson_descripiton = MyRichTextDockWidget(None)
        self.edit_lesson_tag = QLineEdit(self)
                
        # self.validlabel_tag = ValidLabel(self)
        self.bt_picture = PictureButton(self)
        self.bt_video = VideoButton(self)
        self.bt_folder = NewFolderButton(self)
        self.lbl_picture = MyDropableLable(self)
        self.anchorDialog = QAnchorDialog(self)

        #set style sheet border
        self.edit_lesson_descripiton.setStyleSheet('border:1 solid')
        self.edit_lesson_tag.setStyleSheet('border:1 solid')
        self.edit_lesson_title.setStyleSheet('border:1 solid')
        self.edit_lesson_title.setFont(QFont('Arial',12))
        self.edit_lesson_tag.setFont(QFont('Arial',12))
        self.edit_lesson_descripiton.setFont(QFont('Arial',10))
        self.edit_lesson_title.setFixedHeight(30)
        self.edit_lesson_tag.setFixedHeight(30)
                
        #add widgets to layout
        gbox.addWidget(self.edit_lesson_title,0,0,1,10)
        gbox.addWidget(self.edit_lesson_descripiton,1,0,5,10)
        gbox.addWidget(self.edit_lesson_tag,6,0,1,10)
        gbox.addWidget(self.bt_picture,7,0,1,1)
        gbox.addWidget(self.bt_video,7,1,1,1)
        gbox.addWidget(self.bt_folder,7,2,1,1)
        gbox.addWidget(self.lbl_picture,8,0,4,4)

        #set placeholder in each lineedit
        self.edit_lesson_title.setPlaceholderText(Settings.titlePlaceholder)
        self.edit_lesson_descripiton.setPlaceHolderText(Settings.descriptionPlaceholder)
        self.edit_lesson_tag.setPlaceholderText(Settings.tagsPlaceHolder)
        self.anchorDialog.setWindowTitle(Settings.anchorText)
        
        #binding event.
        self.bt_picture.clicked.connect(self.uploadPicture)
        self.anchorDialog.pixmapChanged.connect(self.pixmapChanged)
        pass

    def pixmapChanged(self):
        self.isPixmapSelected = True
        pixmap = self.anchorDialog.pixmap()
        self.lbl_picture.setPixmap(pixmap)
        pass

    def getValidation(self):

        if(self.edit_lesson_title.text() == ''):
            return Settings.noTitleError

        if(self.edit_lesson_tag.text() == ''):
            return Settings.noTag

        if(self.lbl_picture.pixmap() == None):
            return Settings.noAnchor

        return Settings.valid

    def showEvent(self,e):
        # self.anchorDialog.show()
        pass

    def hideEvent(self,e):
        self.anchorDialog.hide()
    
    def setItemInfo(self,posx,posy,poswidth,posheight,pixmap):
        
        if(pixmap is not None):
            self.lbl_picture.setPixmap(pixmap)
            self.anchorDialog.currentPixmap = pixmap
            self.anchorDialog.move(posx,posy)
            self.anchorDialog.resize(poswidth,posheight)
            self.anchorDialog.show()
            self.anchorDialog.mouseDoubleClickEvent(None)
        else:
            self.lbl_picture.initLablePixmap()
            self.anchorDialog = QAnchorDialog(self)
            self.anchorDialog.pixmapChanged.connect(self.pixmapChanged)

            
        
        self.anchorDialog.lastPosx = posx
        self.anchorDialog.lastPosy = posy
        self.anchorDialog.lastWidth = poswidth
        self.anchorDialog.lastHeight = posheight
        pass
    def uploadPicture(self):
        if(self.anchorDialog.isHidden() == True):
            self.anchorDialog.show()
            pass
        else:
            self.anchorDialog.getPixmapAtCurrentPosition()
            pass
        pass

class ClickStepItem(MyFrame):
    
    def __init__(self,parent):

        super(ClickStepItem,self).__init__(parent)
        self.isChild = False
        self.anchorDialog = QAnchorDialog(self)
        self.anchorDialog.sig_mouseClick.connect(self.sig_mouseClick)
        self.anchorDialog.setClickPoint(True)
        self.posx = None
        self.posy = None
        self.posWidth = None
        self.posHeight = None
        self.currentPixmap = None
        self.anchorchildposx = None
        self.anchorchildposy = None
        self.anchorchildwidth = None
        self.anchorchildheight = None

        self.anchorposx = None
        self.anchorposy = None
        self.anchorwidth = None
        self.anchorheight = None


        self.isFirstShow = True

        self.__initUI()

        #set style
        self.lbl_uploadImg.setStyleSheet('margin-bottom:10px;border:1px solid black')
    
    def __initUI(self):

        self.layout = MyGridLayout(self)

        self.edit_header = CommonHeaderTextEdit(self)
        self.lbl_icon = CommonHeaderIcon(self)
        self.lbl_icon.setPixmap(QPixmap('icons/clickstep.png'))
        self.edit_description = CommonDescriptionTextEdit(self)
        self.lbl_prefix = CommonHeaderLabel(self,isPrefix=True)
        self.bt_pic = PictureButton(self)
        self.bt_video = VideoButton(self)
        self.bt_newfolder = NewFolderButton(self)
        self.bt_attach = AttachStepButton(self)
        self.lbl_uploadImg = MyDropableLable(self)
        self.checkbt_clickSpot = MyCheckBox(self)
        self.lbl_clickSpot = CommonHeaderLabel(self)
        self.checkbt_imageRec = MyCheckBox(self)
        self.combo_imageRec = MyComboBox(self)
        
        self.row_clickspot = MyRow(self)
        self.row_imageRec = MyRow(self)
        self.row_clickspot.addWidget(self.checkbt_clickSpot)
        self.row_clickspot.addWidget(self.lbl_clickSpot)
        self.row_imageRec.addWidget(self.checkbt_imageRec)
        self.row_imageRec.addWidget(self.combo_imageRec)
        self.row_snapshot = MyRow(self)
        self.row_snapshot.addWidget(self.bt_pic)
        self.row_snapshot.addWidget(self.bt_video)
        self.row_snapshot.addWidget(self.bt_attach)
        self.edit_TextMatch = CommonHeaderTextEdit(self)
        
        
        # set properties for each object
        self.edit_sec_description = CommonDescriptionTextEdit(self)
        self.edit_header.setPlaceholderText(Settings.stepTitlePlaceHolder)
        self.edit_description.setPlaceholderText(Settings.stepDescriptionPlaceHolder)
        self.lbl_clickSpot.setText(Settings.clickSportText)
        self.combo_imageRec.addItem(Settings.imageMatchText)
        self.combo_imageRec.addItem(Settings.textMatchText)
        self.combo_imageRec.setCurrentIndex(0)
        self.checkbt_clickSpot.setChecked(True)
        self.edit_TextMatch.setPlaceholderText(Settings.textMatchPlaceHolderText)
        

        #set layout
        self.layout.addWidget(self.lbl_prefix,0,0,24,1)
        self.layout.addWidget(self.edit_header,0,1,1,19)
        self.layout.addWidget(self.lbl_icon,0,20,1,1)
        self.layout.addWidget(self.edit_description,1,1,1,20)
        self.layout.addWidget(self.edit_sec_description,2,1,1,20)
        self.layout.addWidget(self.row_clickspot,2,1,1,20)
        self.layout.addWidget(self.row_imageRec,3,1,1,1)
                
        # self.layout.addWidget(self.bt_pic,4,1,1,1)
        # self.layout.addWidget(self.bt_video,4,2,1,1)
        # self.layout.addWidget(self.bt_att,4,3,1,1)
        self.layout.addWidget(self.row_snapshot,4,1,1,20)
        self.layout.addWidget(self.lbl_uploadImg,5,1,20,20)
        self.layout.addWidget(self.edit_TextMatch,26,1,1,20)


        #set layout properties.
        self.layout.setContentsMargins(0,0,0,Settings.commonMargin)
        

        #current feedback field seems to be not needed #checkme here
        self.edit_sec_description.hide()
        self.bt_newfolder.hide()
        self.edit_TextMatch.hide()

        #bind event
        self.bt_pic.clicked.connect(self.process_bt_pic_clicked)
        self.anchorDialog.pixmapChanged.connect(self.updatePic)
        self.checkbt_clickSpot.stateChanged.connect(self.process_checkbt_clickSpot)
        self.checkbt_imageRec.stateChanged.connect(self.process_checkbt_imageRec)
        self.combo_imageRec.currentIndexChanged.connect(self.process_combo_imageRec)
        
        pass
    
    def process_combo_imageRec(self,curIndex):

        if(self.checkbt_imageRec.isChecked() == False):
            self.checkbt_imageRec.setChecked(True)
            self.checkbt_clickSpot.setChecked(False)
            
        if self.combo_imageRec.currentText() == Settings.imageMatchText:
            self.edit_TextMatch.hide()
            pass
        if self.combo_imageRec.currentText() == Settings.textMatchText:
            self.edit_TextMatch.show()
            pass
        pass
    
    def process_checkbt_clickSpot(self,event):

        if(event):

            self.checkbt_clickSpot.setChecked(True)
            self.checkbt_imageRec.setChecked(False)
            self.anchorDialog.setClickPoint(True)
            
            #if anchor diallog is hidden, then don't show child anchor also.
            posx = self.anchorDialog.mapToGlobal(QPoint(0,0)).x() + self.anchorDialog.width()//2
            posy = self.anchorDialog.mapToGlobal(QPoint(0,0)).y() + self.anchorDialog.height()//2
            self.anchorDialog.childAnchor.move(posx-self.anchorDialog.width()//4,posy-self.anchorDialog.height()//4)
            self.anchorDialog.childAnchor.resize(self.anchorDialog.width()//2,self.anchorDialog.height()//2)
            self.anchorDialog.childAnchor.show()
            self.anchorDialog.childAnchor.topleftgrip.showEvent(None)
            self.anchorDialog.childAnchor.toprightgrip.showEvent(None)
            self.anchorDialog.childAnchor.bottomleftgrip.showEvent(None)
            self.anchorDialog.childAnchor.bottomrightgrip.showEvent(None)
            if(self.anchorDialog.isHidden() == True):
                self.anchorDialog.childAnchor.hide()
                return
            pass
        else:
            self.anchorDialog.setClickPoint(False)
            self.anchorDialog.childAnchor.hide()
            pass
    
    def process_checkbt_imageRec(self,event):
        if(event):
            self.checkbt_clickSpot.setChecked(False)
            if(self.combo_imageRec.currentText() == Settings.textMatchText):
                self.edit_TextMatch.show()
            else:
                self.edit_TextMatch.hide()
                pass
            pass
        else:
            self.edit_TextMatch.hide()
            pass
    
    def process_bt_pic_clicked(self):

        if(self.anchorDialog.isHidden()):
            self.anchorDialog.show()
        else:
            self.anchorDialog.mouseDoubleClickEvent(1)
            self.anchorDialog.hide()
        
    def updatePic(self):

        pixmap = self.anchorDialog.currentPixmap
        self.currentPixmap = pixmap
        
        if(self.anchorDialog.ClickPointable):
            #set child anchor pos info
            self.posx = self.anchorDialog.childAnchor.x() - self.anchorDialog.x()
            self.posy = self.anchorDialog.childAnchor.y() - self.anchorDialog.y()
            self.posWidth = self.anchorDialog.childAnchor.width()
            self.posHeight = self.anchorDialog.childAnchor.height()
            self.lbl_uploadImg.setClickableArea(self.posx,self.posy,self.posWidth,self.posHeight)
        else:
            self.posx = None
            self.posy = None
            self.posWidth = None
            self.posHeight = None
            self.lbl_uploadImg.setClickableArea(None,None,None,None)
            pass
        # self.anchorDialog.setPixmap(pixmap)
        
        # project text match using tesseract
        if(self.checkbt_imageRec.isChecked() == True and self.combo_imageRec.currentText() == Settings.textMatchText):
            cv2_image = MyUtil.convertPixmapToGray(pixmap,isgray=False)
            str_Match = MyUtil.getTextFromImage(cv2_image)
            self.edit_TextMatch.setText(str_Match)
        self.lbl_uploadImg.setPixmap(pixmap)
        pass

    def mousePressEvent(self,event):

        pass

    def showEvent(self,event):

        self.edit_header.show()
        self.edit_description.show()
        self.lbl_icon.show()
        self.lbl_uploadImg.show()
        self.row_clickspot.show()
        self.row_imageRec.show()
        self.row_snapshot.show()
        
        if len(self.edit_TextMatch.toPlainText())>0:
            self.edit_TextMatch.show()
            self.checkbt_clickSpot.setChecked(False)
            self.checkbt_imageRec.setChecked(True)
            self.combo_imageRec.setCurrentText(Settings.textMatchText)
        if self.posx is None:
            self.checkbt_clickSpot.setChecked(False)
            self.checkbt_imageRec.setChecked(True)
        pass

        super().showEvent(event)

        if(self.isFirstShow == True):
            self.isFirstShow = False
            
            if self.anchorposx is not None:
                self.anchorDialog.resize(self.anchorwidth,self.anchorheight)
                self.anchorDialog.move(self.anchorposx,self.anchorposy)
            
            if self.posx is not None:
                self.anchorDialog.ClickPointable = True
                self.checkbt_clickSpot.setChecked(True)
                self.anchorDialog.childAnchor.move(self.anchorchildposx,self.anchorchildposy)
                self.anchorDialog.childAnchor.resize(self.anchorchildwidth,self.anchorchildheight)

            self.anchorDialog.show()

            if(self.anchorposx is not None):
                self.anchorDialog.mouseDoubleClickEvent(None)

    def hideEvent(self,event):
        self.edit_header.hide()
        self.lbl_icon.hide()
        self.edit_description.hide()
        self.lbl_prefix.hide()
        # self.bt_pic.hide()
        # self.bt_video.hide()
        # self.bt_newfolder.hide()
        # self.bt_attach.hide()
        self.row_snapshot.hide()
        self.lbl_uploadImg.hide()
        self.row_clickspot.hide()
        self.row_imageRec.hide()
        self.row_snapshot.hide()
        self.edit_TextMatch.hide()
        super(ClickStepItem,self).hideEvent(event)
    
    def setWidgetSpan(self, widget, rowspan=1, colspan=1):
        index = self.layout.indexOf(widget)
        row, column = self.layout.getItemPosition(index)[:2]
        self.layout.addWidget(widget, row, column, rowspan, colspan)
    
    def sig_mouseClick(self,posx,posy):
        #checkmehere don't need to show crosshair to mouse click point
        # self.posx = posx
        # self.posy = posy
        pass

    def getDatas(self):
        title = self.edit_header.toPlainText()
        description = self.edit_description.toPlainText()
        anchorPixmap = self.anchorDialog.currentPixmap
        sec_description = self.edit_sec_description.toPlainText()
        match_Text = self.edit_TextMatch.toPlainText()

        if(self.isFirstShow == True):
            print("checmehere2")
            print(self.anchorchildposx,self.anchorchildposy,self.anchorchildwidth,self.anchorchildheight)
            return Settings.clickStep,title,description,sec_description,None,anchorPixmap,self.isChild,None,match_Text,self.anchorDialog.lastPosx,\
            self.anchorDialog.lastPosy,self.anchorDialog.lastWidth,self.anchorDialog.lastHeight,self.anchorchildposx,self.anchorchildposy,self.anchorchildwidth,\
                self.anchorchildheight
        else:
            return Settings.clickStep,title,description,sec_description,None,anchorPixmap,self.isChild,None,match_Text,self.anchorDialog.lastPosx,\
            self.anchorDialog.lastPosy,self.anchorDialog.lastWidth,self.anchorDialog.lastHeight,self.anchorDialog.childAnchor.lastChildPosx,\
                self.anchorDialog.childAnchor.lastChildPosy,self.anchorDialog.childAnchor.lastChildWidth,self.anchorDialog.childAnchor.lastChildHeight

    def setItemInfos(self,title,description,sec_description,isChild,spotposx,spotposy,spotwidth,spotheight,anchorPixmap,*kwargs):
        
        self.edit_header.setText(title)
        self.edit_description.setText(description)
        self.edit_sec_description.setText(sec_description)
        self.posx = spotposx
        self.posy = spotposy
        self.posWidth = spotwidth
        self.posHeight = spotheight
        
        if(kwargs is not None):

            self.edit_TextMatch.setText(kwargs[0])

            if len(kwargs)>7:
                self.anchorposx = kwargs[1]
                self.anchorposy = kwargs[2]
                self.anchorwidth = kwargs[3]
                self.anchorheight = kwargs[4]
                self.anchorchildposx = kwargs[5]
                self.anchorchildposy = kwargs[6]
                self.anchorchildwidth = kwargs[7]
                self.anchorchildheight = kwargs[8]
            else:
                self.anchorposx = None
                self.anchorposy = None
                self.anchorwidth = None
                self.anchorheight = None
                self.anchorchildposx = None
                self.anchorchildposy = None
                self.anchorchildwidth = None
                self.anchorchildheight = None


        self.isChild = isChild
        
        if(anchorPixmap is not None):
            path = os.path.join(Globals.projectmgr.projectPath,anchorPixmap)
            self.lbl_uploadImg.setPixmap(QPixmap(path))
            self.anchorDialog.currentPixmap = QPixmap(path)
            self.anchorDialog.setPixmap(QPixmap(path))

        #init lastposx
        self.anchorDialog.lastPosx = self.anchorposx
        self.anchorDialog.lastPosy = self.anchorposy
        self.anchorDialog.lastWidth = self.anchorwidth
        self.anchorDialog.lastHeight = self.anchorheight

        self.anchorDialog.childAnchor.lastChildPosx = self.anchorchildposx
        self.anchorDialog.childAnchor.lastChildPosy = self.anchorchildposy
        self.anchorDialog.childAnchor.lastChildWidth = self.anchorchildwidth
        self.anchorDialog.childAnchor.lastChildHeight = self.anchorchildheight

        
        
    
class MyListWidget(QWidget):
    
    def __init__(self,parent):

        super(MyListWidget, self).__init__(parent)
        self.listitems = self.LoadItems()
        self.vbox = MyVBoxLayout(self)
        self.vbox.addStretch(1)
        self.__initUI()

    def LoadItems(self):
        return []

    def getItemsList(self):
        return self.listitems

    def clear(self):
        while len(self.listitems):
            self.currentItem = self.listitems[0]
            self.removeCurrentItem()
        self.currentItem = None

    def removeCurrentItem(self):
        self.vbox.removeWidget(self.currentItem)
        self.listitems.remove(self.currentItem)
        self.currentItem.close()
        self.currentItem.anchorDialog.close()
        self.currentItem = None
        self.showAllItems()

    def __initUI(self):
        self.listitems = self.LoadItems()
        if(len(self.listitems) == 0):
            self.currentItem = None
            return
        self.currentItem = self.listitems[0]
        for item in self.listitems:
            self.vbox.addWidget(item)
    
    def insertItem(self,item):
        if(item is None):
            self.showAllItems()
            return
        self.vbox.insertWidget(self.vbox.count()-1,item)
        self.listitems.append(item)
        self.currentItem = item
        self.currentItem.edit_header.installEventFilter(self)
        # self.currentItem.lbl_prefix.installEventFilter(self) #check me here no need add child item
        self.showAllItems()

    def isEmpty(self):
        return len(self.listitems) == 0

    def showAllItems(self):
        for item in self.listitems:
            if(item == self.currentItem):
                item.show()
                item.anchorDialog.show()
                pass
            else:
                item.show()
                item.anchorDialog.hide()

    def eventFilter(self,source,event):

        if event.type() == QEvent.FocusIn and source is not None:
            self.currentItem = source.parentWidget()
            self.showAllItems()
            return super(MyListWidget,self).eventFilter(source,event)

        elif event.type() == QEvent.MouseButtonPress and type(source).__name__ == 'CommonHeaderLabel':
            #change this item as child
            self.currentItem = source.parentWidget()
            # self.currentItem.isChild = not self.currentItem.isChild#check me here , removed child property
            self.showAllItems()
            return super(MyListWidget,self).eventFilter(source,event)

        else:
            return super(MyListWidget,self).eventFilter(source,event)
    
    def showEvent(self,event):
        self.showAllItems()
        super().showEvent(event)
    
    def getValidation(self):
        for item in self.listitems:
            if item.edit_header is not None:
                if(item.edit_header.toPlainText() == ''):
                    self.currentItem = item
                    return Settings.noTitleError
            else:
                # This is attach step or pistol step
                pass
        return Settings.valid
        
class TeacherLandingPage(MyContainer):

    sig_currentItemChanged = pyqtSignal(str)
    sig_DoubleClick = pyqtSignal(str)
    def __init__(self,parent):
        super(TeacherLandingPage, self).__init__(parent)
        self.parent = parent
        layout = self.createLayOut()
        self.setLayout(layout)
        

    def createLayOut(self):

        self.toolbarfirst  = TeacherFirstToolbar(self)
        self.toolbarsec = TeacherSecondToolbar(self)

        self.tree = MyTree(self,fromAws=False)
        self.toolbarfirst.bt_search.clicked.connect(self.find_item_with_name)
        

        vbox = MyVBoxLayout(self)
        #add all frame to a container.

        vbox.addWidget(self.toolbarfirst)
        vbox.addWidget(self.toolbarsec)
        vbox.addWidget(self.tree)
        vbox.addStretch(1)

        #bind event
        self.tree.currentItemChanged.connect(self.currentItemChanged)
        self.tree.sig_doubleclick.connect(self.sig_DoubleClick)

        return vbox
    

    def currentItemChanged(self,item):

        paths = []
        while(item is not None):
            paths.insert(0,item.text(0))
            item = item.parent()
        curPath = ""
        for path in paths:
            curPath = os.path.join(curPath,path)

        self.sig_currentItemChanged.emit(curPath)

    def find_item_with_name(self):

        self.tree.find_button_clicked('acer')

    def refresh(self):
        self.tree.refresh()

class TeacherNewLessionPage(MyContainer):
    procDone = pyqtSignal(str)
    
    def __init__(self,parent):

        super(TeacherNewLessionPage,self).__init__(parent)
        self.__initUI()

        self.currentProjectPath = Globals.projectmgr.projectPath
        self.data = None

    def __initUI(self):
        self.layout = MyGridLayout(self)
        self.firsttoolbar = TeacherFirstToolbar(self)

        ## grouping two widget
        
        self.Secondtoolbar = Teacher_LookStep_SecondToolBar(self)
        self.newLessonbar = TeahcerNewLookStepPage(self)
        
        self.newLessonbar.hide()
        self.Thirdtoolbar = TeacherSecondLessonToolbar(self)
        
        self.layout.addWidget(self.firsttoolbar,0,0,1,1)
        self.layout.addWidget(self.Secondtoolbar,1,0,15,1)
        self.layout.addWidget(self.newLessonbar,1,0,15,1)
        self.layout.addWidget(self.Thirdtoolbar,16,0,1,1)

        #bind events

        self.Thirdtoolbar.bt_attachstep.clicked.connect(lambda:self.addItem('attach'))
        self.Thirdtoolbar.bt_clickstep.clicked.connect(lambda:self.addItem('click'))
        self.Thirdtoolbar.bt_cloudbutton.clicked.connect(lambda:self.addItem('cloud'))
        self.Thirdtoolbar.bt_lookstep.clicked.connect(lambda:self.addItem('look'))
        self.Thirdtoolbar.bt_matchstep.clicked.connect(lambda:self.addItem('match'))
        self.Thirdtoolbar.bt_mousestep.clicked.connect(lambda:self.addItem('mouse'))
        self.Thirdtoolbar.bt_playbutton.clicked.connect(lambda:self.addItem('play'))
        self.Thirdtoolbar.bt_delete.clicked.connect(lambda:self.addItem('delete'))

        self.newLessonbar.frame.mousePressEvent = self.gotoNewLessonFromStepPage
        self.Secondtoolbar.edit_lesson_title.textChanged.connect(self.newLessonbar.setText)
        self.Secondtoolbar.anchorDialog.pixmapChanged.connect(self.pixmapChanged)

        return self.layout

    def gotoNewLessonFromStepPage(self,event):
        self.newLessonbar.hide()
        self.Secondtoolbar.show()
        #hide lessonwidget and anchordialgo
        if(self.newLessonbar.listWidget.currentItem is not None):
            self.newLessonbar.listWidget.currentItem.anchorDialog.hide()
        pass

    def pixmapChanged(self):
        self.newLessonbar.lbl_icon.setPixmap(self.Secondtoolbar.anchorDialog.pixmap())

    def processTitleChanged(self,str_title):
        pass

    def addItemInstance(self,item=None):
        logging.info("this item has been added from folder "+item.edit_header.toPlainText())
        if(item is None):
            return
        self.newLessonbar.listWidget.insertItem(item)
        pass
    
    def addItem(self,itemtype):

        if(itemtype == 'attach'):
            self.newLessonbar.listWidget.insertItem(None)
            pass
        elif(itemtype == 'click'):
            if(self.newLessonbar.isHidden()):
                if(self.newLessonbar.listWidget.isEmpty()):
                    logging.info("empty item has been added")
                    self.newLessonbar.listWidget.insertItem(ClickStepItem(self))
                    pass
                else:
                    logging.info("No item has been added but go to step page")
                    self.gotoStepPage()
                    return
            else:
                logging.info("new empty item has been added")
                self.newLessonbar.listWidget.insertItem(ClickStepItem(self))
                pass            
            pass
        elif(itemtype == 'cloud'):
            # self.newLessonbar.listWidget.insertItem(None)
            pass
        elif(itemtype == 'play'):
            self.procDone.emit("start")
            return
        elif(itemtype == 'delete'):
            if self.newLessonbar.listWidget.currentItem is not None:
                self.newLessonbar.listWidget.removeCurrentItem()
                pass
        else:
            pass

        # scroll to last item
        self.newLessonbar.scroll.verticalScrollBar().setSliderPosition(self.newLessonbar.scroll.verticalScrollBar().maximum())
        self.gotoStepPage()
    
    def getValidation(self):
        
        valid_resp_lesson = self.Secondtoolbar.getValidation()
        valid_resp_steps = self.newLessonbar.getValidation()
        
        if(valid_resp_lesson == Settings.valid):
            pass
        else:
            self.gotoNewLessonPage(None)
            return Settings.lessonError
        if(valid_resp_steps == Settings.valid):
            pass
        else:
            self.gotoStepPage()
            return Settings.stepError
        return Settings.valid
    
    def gotoNewLessonPage(self,event):
        
        # if(self.currentProjectPath != Globals.projectmgr.projectPath and Globals.projectmgr.projectPath is not None):

        self.clearAllListItems()
        if self.LoadCurrentProject():
            #emit signal
            logging.info("loading current project..")
            pass
        else:
            return False
        if(MyUtil.isLeaf(self.currentProjectPath) == False):
            return False

        logging.info("go to step page project..")
        
        self.newLessonbar.hide()
        self.Secondtoolbar.show()

        #hide lessonwidget and anchordialgo
        if(self.newLessonbar.listWidget.currentItem is not None):
            self.newLessonbar.listWidget.currentItem.anchorDialog.hide()

        return True

    def clearAllListItems(self):
        logging.info("list items has been cleared")
        self.newLessonbar.listWidget.clear()

    def LoadCurrentProject(self):

        self.currentProjectPath = Globals.projectmgr.projectPath
        
        print("project is createend here",self.currentProjectPath)


        if(MyUtil.isLeaf(self.currentProjectPath)):
            pass
        else:
            logging.info("Current item is not project folder.")
            return False

        self.data = MyUtil.loadData(os.path.join(self.currentProjectPath,Settings.projectFileName))
        if(self.data is None):
            logging.info("Data is not found in here " + self.currentProjectPath)
            return False

        self.imageBaseUrl = self.data.metaInfo.baseImgUrl
        self.Secondtoolbar.edit_lesson_title.setText(self.data.header.title)
        self.Secondtoolbar.edit_lesson_descripiton.setText(self.data.header.description)
        self.Secondtoolbar.edit_lesson_tag.setText(self.data.header.tags)
        
        if(self.data.header.anchorImageName is not None):
            pixmap = QPixmap(os.path.join(Globals.projectmgr.projectPath,self.data.header.anchorImageName))
        else:
            pixmap = None
        try:
            param = self.data.header.anchorposx,self.data.header.anchorposy,self.data.header.anchorwidth,self.data.header.anchorheight,pixmap
            self.Secondtoolbar.setItemInfo(*param)
            pass
        except:
            param = None,None,None,None,pixmap
            self.Secondtoolbar.setItemInfo(*param)
            pass
        
        self.itemList = []
        for idx in range(len(self.data.lessons)):
            if(self.data.lessons[idx].type == Settings.lookStep):
                pass
            elif(self.data.lessons[idx].type == Settings.clickStep):

                curInfo = self.data.lessons[idx]
                item = ClickStepItem(self)
                try:
                    anchorposx = curInfo.anchorposx
                    anchorposy = curInfo.anchorposy
                    anchorwidth = curInfo.anchorwidth
                    anchorheight = curInfo.anchorheight
                    anchorchildposx = curInfo.anchorchildposx
                    anchorchildposy = curInfo.anchorchildposy
                    anchorchildwidth = curInfo.anchorchildwidth
                    anchorchildheight = curInfo.anchorchildheight
                except:
                    anchorposx = None
                    anchorposy = None
                    anchorwidth = None
                    anchorheight = None
                    anchorchildposx = None
                    anchorchildposy = None
                    anchorchildwidth = None
                    anchorchildheight = None
                    pass

                item.setItemInfos(curInfo.title,curInfo.description,curInfo.sec_description,curInfo.isChild,curInfo.spotposx,\
                curInfo.spotposy,curInfo.spotwidth,curInfo.spotheight,\
                    curInfo.anchorPixmap,curInfo.matchText,anchorposx,anchorposy,anchorwidth,anchorheight,anchorchildposx,\
                        anchorchildposy,anchorchildwidth,anchorchildheight)

                self.addItemInstance(item)
                item.hide()
                pass
            
            else:
                pass
        
        return True
    
    def gotoStepPage(self):
        
        self.Secondtoolbar.hide()
        self.newLessonbar.show()
    
    def hideEvent(self,event):
        if self.newLessonbar.listWidget.currentItem is not None:
            self.newLessonbar.listWidget.currentItem.anchorDialog.hide()
        pass

class TeahcerNewLookStepPage(MyContainer):
    #This is step page
    def __init__(self,parent):

        super(TeahcerNewLookStepPage,self).__init__(parent)
        self.__initUI()

    def __initUI(self):

        self.layout = MyGridLayout(self)
        self.lbl_lessonTitle = CommonHeaderLabel(self)
        self.frame = MyFrame(self)
        self.lbl_icon = CommonHeaderIcon(self)
        self.listWidget = MyListWidget(self)
        self.lbl_lessonTitle.setContentsMargins(10,1,10,1)
        self.lbl_icon.setContentsMargins(1,1,1,1)
        
        hbox = MyHBoxLayout(None)
        hbox.addWidget(self.lbl_lessonTitle)
        hbox.addStretch(1)
        hbox.addWidget(self.lbl_icon)
        self.frame.setLayout(hbox)
        
        self.scroll = QScrollArea(self)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.listWidget)

        self.layout.addWidget(self.frame,1,0,1,20)
        
        self.layout.addWidget(self.scroll,2,0,20,20)

        #event binding
        self.frame.mousePressEvent = self.gotoTeacherNewLessonPage
    
    def getValidation(self):
        return self.listWidget.getValidation()
    
    def gotoTeacherNewLessonPage(self,event):
        # for future use
        pass
    
    def showEvent(self,event):
        self.listWidget.showAllItems()

    def setText(self,str_text):
        self.lbl_lessonTitle.setText(str_text)
        pass

    def setLabelIcon(self, label = "Title",iconPath='icons/smile.png'):
        # self.lbl_lessonTitle.setText(label)
        # self.lbl_icon.setPixmap(QPixmap(iconPath))
        pass

class TeacherTabWidget(MyContainer):
    gotoStudentTab = pyqtSignal(str)
    sig_saveCurrentProject = pyqtSignal(str)
    sig_upLoadFolder = pyqtSignal(str)

    def __init__(self,parent):
        super(TeacherTabWidget,self).__init__(parent)
        self.currentWidget = None
        self.currentProjectPath = None
        self.__initUI()

    def __initUI(self):

        self.landing_page = TeacherLandingPage(self)
        self.currentWidget = self.landing_page

        self.lookstep_page = TeacherNewLessionPage(self)
        self.layout = MyVBoxLayout(self)
        self.layout.addWidget(self.landing_page)
        self.layout.addWidget(self.lookstep_page)
        self.setLayout(self.layout)

        # viewing only current page and hide all others
        self.hideAllButCurrent()
        
        #event binding
        self.landing_page.toolbarsec.sig_EditProject.connect(self.editProject)
        self.landing_page.toolbarsec.sig_NewProject.connect(self.createNewProject)
        self.landing_page.toolbarsec.sig_newFolder.connect(self.createNewFolder)
        self.landing_page.toolbarsec.sig_DeleteProject.connect(self.deleteProject)
        self.landing_page.toolbarsec.sig_SearchProject.connect(self.searchProject)
        self.landing_page.toolbarsec.sig_Social.connect(self.gotoSocial)
        self.landing_page.toolbarsec.sig_UploadToCloud.connect(self.upLoadProjectToCloud)
        self.landing_page.toolbarsec.sig_PlayResume.connect(self.playLesson)
        self.landing_page.sig_currentItemChanged.connect(self.currentItemChanged)
        self.landing_page.sig_DoubleClick.connect(self.editProject)

        self.lookstep_page.firsttoolbar.bt_book.clicked.connect(self.gotoLandingpage)
        self.lookstep_page.procDone.connect(self.gotoStudentTab)

    def currentItemChanged(self,leafPath):
        
        Globals.projectmgr.currentProjectPath = leafPath
        Globals.projectmgr.changeProjectPath()
        
    def createNewFolder(self):

        pmgr = Globals.projectmgr
        path = ""
        if(pmgr.projectPath is None):
            path = pmgr.getTeacherProjectsLocalPath()
        else:
            path = pmgr.projectPath
        
        name, done = QInputDialog.getText(self, 'Input Dialog', 'ENTER YOUR PROGRAM NAME:')
        if(done):
            pass
        else:
            return

        #if leaf. select parent directory  
        if(MyUtil.isLeaf(path)):
            path = os.path.dirname(path)

        #if this same name dir exist, replace with new one
        path = os.path.join(path,name)
        if os.path.exists(path):
            shutil.rmtree(path,ignore_errors=True)
        try:
            os.mkdir(path)
        except:
            logging.info("can't create program folder in path: " + path)

        #refresh tree object
        self.landing_page.refresh()
        pass
    def editProject(self,path=None):
        # this is for edit project
        
        self.gotoLooksteppage(param=Settings.gotoLessson)
        pass
    
    def createNewProject(self):

        name, done1 =  Settings.templateFolder, True #QInputDialog.getText(self, 'Input Dialog', 'Enter your project name:')#check me here this is uneccessary

        if(done1):
            path = None
            if(MyUtil.isLeaf(Globals.projectmgr.getAbsCurrentProjectPath())):
                path = os.path.dirname(Globals.projectmgr.getAbsCurrentProjectPath())
            else:
                path = Globals.projectmgr.getAbsCurrentProjectPath()
            try:
                path = os.path.join(path,name)
                Globals.projectmgr.createTemplateProject(path)
                Globals.projectmgr.projectPath = path
                logging.info(path + " creating project...")
                #create project directory and projecty main file
                self.gotoLooksteppage()
            except:
                pass
        else:
            pass
        pass

    def deleteProject(self):
        if Globals.projectmgr.deleteCurrentProject():
            self.landing_page.tree.refresh()
        pass

    def searchProject(self):
        pass
    def gotoSocial(self):
        pass
    def upLoadProjectToCloud(self):
        self.sig_upLoadFolder.emit(Globals.projectmgr.projectPath)
        pass
    def playLesson(self):
        pass

    
    def getValidation(self):
        return self.lookstep_page.getValidation()
    def hideAllButCurrent(self):
        self.landing_page.hide()
        self.lookstep_page.hide()
        self.currentWidget.show()

    def gotoLooksteppage(self,param = 1):
        if(param == Settings.gotoLessson):
            logging.info("go to newlessonPage")
            if self.lookstep_page.gotoNewLessonPage(None):
                pass
            else:
                return
            pass
        elif(param == Settings.gotoStep):
            logging.info("go to lessonstepPage")
            self.lookstep_page.gotoStepPage()
            pass
        self.currentWidget = self.lookstep_page
        self.hideAllButCurrent()


    def showConfirmDlg(self):
        if(CustomDialog.showStandardMsgbox(self.window(),"Will you save This project?")):
            return True
        else:
            return False
        pass
    
    def gotoLandingpage(self):
        
        if self.showConfirmDlg():
            #save current project
            self.sig_saveCurrentProject.emit("")
            pass
        else:
            #delete template project
            if Settings.templateFolder in Globals.projectmgr.projectPath:
                shutil.rmtree(Globals.projectmgr.projectPath)
            else:
                pass

        self.currentWidget = self.landing_page
        self.hideAllButCurrent()
        self.landing_page.tree.refresh()

    # def hideEvent(self,event):
    #     self.gotoLandingpage()









