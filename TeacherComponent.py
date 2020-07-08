import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QMessageBox,\
QAction, QTabWidget,QGridLayout,QFrame,QLabel,QSlider,QScrollArea,QCheckBox,QSizePolicy,QFileDialog,QDockWidget, QDialog,QTreeView,\
    QLineEdit, QTreeWidget, QTreeWidgetItem,QAbstractItemView,QAbstractScrollArea,QPlainTextEdit,QRadioButton
from PyQt5.QtGui import QIcon,QFont,QCursor,QPixmap,QPaintDevice,QPainter,QPen
from PyQt5.QtCore import pyqtSlot, Qt, QSize,QEvent,QTimer,pyqtSignal, QPoint
from Setting import Settings
from Mybutton import *
from Container import *
from PyQt5 import QtWidgets


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


class MyTree(QTreeWidget):
    def __init__(self,parent):
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

    def loadData(self):
        """ 
        Load data from api or any other data source and return json object
        """
        # return data for test
        return ['Drawing Sunsets',{'Pixel Art Track':['How To DRAW A SMILEY FACE']},'Color Theory',{'Art Theroy':{'Drawing Lessions':['Select Palette','acer'],'Drawing Lessions1':['Select Palette','acer']}},\
            'Drawing Sunsets1',{'Pixel Art Track1':['How To DRAW A SMILEY FACE1']},'Color Theory1',{'Art Theroy1':{'Drawing Lessions1':['Select Palette1','acer1'],'Drawing Lessions':['Select Palette','acer']}},\
                'Drawing Sunsets2',{'Pixel Art Track':['How To DRAW A SMILEY FACE']},'Color Theory',{'Art Theroy':{'Drawing Lessions':['Select Palette','acer'],'Drawing Lessions1':['Select Palette','acer']}},
                'Drawing Sunsets3',{'Pixel Art Track':['How To DRAW A SMILEY FACE']},'Color Theory',{'Art Theroy':{'Drawing Lessions':['Select Palette','acer'],'Drawing Lessions1':['Select Palette','acer']}}]

    def insertItem(self,label,path,isParent):

        # newItem = MyTreeItem(text = label,isParent = isParent, iconPath = self.iconPath)
        try:
            pass
        except:
            pass

    def dropEvent(self,event):
        item=self.itemAt(event.pos())

        if(item is None):
            super(MyTree,self).dropEvent(event)
            return
        if(item.isParent):
            super(MyTree,self).dropEvent(event)
        else:
            event.ignore()


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

    def __init__(self,parent):
        super(TeacherSecondToolbar, self).__init__(parent)
        self.__initUI()
        
    def __initUI(self):
        hbox = MyHBoxLayout(self)
        self.bt_edit  = EditButton(self)
        self.bt_newfolder = NewFolderButton(self)
        self.bt_searchplus = SearchPlusButton(self)

        self.bt_social = SocialButton(self)
        self.bt_cloud = CloudButton(self)
        self.bt_resume = PlayResumeButton(self)

        hbox.addWidget(self.bt_edit)
        hbox.addWidget(self.bt_newfolder)
        hbox.addWidget(self.bt_searchplus)
        
        hbox.addStretch(1)
        hbox.addWidget(self.bt_social)
        hbox.addWidget(self.bt_cloud)
        hbox.addWidget(self.bt_resume)
        hbox.setContentsMargins(0,0,0,0)
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
    def uploadPicture(self):
        if(self.anchorDialog.isHidden() == True):
            self.anchorDialog.show()
            pass
        else:
            self.anchorDialog.getPixmapAtCurrentPosition()
            pass
        pass

class LookStepItem(MyFrame):

    def __init__(self,parent):

        super(LookStepItem,self).__init__(parent)

        self.isChild = False
        self.anchorDialog = QAnchorDialog(self)
        self.__initUI()
        self.setStyleSheet('padding:2px')
        
    def mousePressEvent(self,event):
        
        pass

    def __initUI(self):

        self.layout = MyGridLayout(self)
        self.edit_header = CommonHeaderTextEdit(self)

        self.lbl_icon = CommonHeaderIcon(self)
        self.lbl_icon.setPixmap(QPixmap('icons/lookstep.png'))
        self.edit_description = CommonDescriptionTextEdit(self)
        self.lbl_prefix = CommonHeaderLabel(self,isPrefix=True)
        self.edit_header.setPlaceholderText(Settings.stepTitlePlaceHolder)
        self.edit_description.setPlaceholderText(Settings.stepDescriptionPlaceHolder)

        self.layout.addWidget(self.lbl_prefix,0,0,2,1)
        self.layout.addWidget(self.edit_header,0,1,1,19)
        self.layout.addWidget(self.lbl_icon,0,20,1,1)
        self.layout.addWidget(self.edit_description,1,1,1,20)

        
    
    def getDatas(self):
        title = self.edit_header.toPlainText()
        description = self.edit_description.toPlainText()
        anchorPixmap = self.anchorDialog.pixmap()
        return Settings.lookStep,title,description,None,None,anchorPixmap,self.isChild,None


    def display(self,isminum=False):
        if(self.isChild):
            self.setContentsMargins(30,0,0,0)
            isminum = True
        else:
            self.setContentsMargins(0,0,0,0)
        if(isminum == True):

            self.setWidgetSpan(self.lbl_prefix,1,1)
            self.edit_description.hide()

            pass
        else:

            self.setWidgetSpan(self.lbl_prefix,2,1)
            self.edit_description.show()
            pass

    def setWidgetSpan(self, widget, rowspan=1, colspan=1):
        index = self.layout.indexOf(widget)
        row, column = self.layout.getItemPosition(index)[:2]
        self.layout.addWidget(widget, row, column, rowspan, colspan)
    # def hideEvent(self,event):
    #     super().hide()
    #     self.anchorDialog.hide()
    def getValidation(self):
        # self.edit_header.textBackgroundColor
        
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
        
        
        # set properties for each object
        self.edit_sec_description = CommonDescriptionTextEdit(self)
        self.edit_header.setPlaceholderText(Settings.stepTitlePlaceHolder)
        self.edit_description.setPlaceholderText(Settings.stepDescriptionPlaceHolder)
        self.lbl_clickSpot.setText(Settings.clickSportText)
        self.combo_imageRec.addItem(Settings.imageMatchText)
        self.combo_imageRec.addItem(Settings.textMatchText)
        self.combo_imageRec.setCurrentIndex(0)
        self.checkbt_clickSpot.setChecked(True)

        #set layout
        self.layout.addWidget(self.lbl_prefix,0,0,23,1)
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

        #current feedback field seems to be not needed #checkme here
        self.edit_sec_description.hide()
        self.bt_newfolder.hide()

        #bind event
        self.bt_pic.clicked.connect(self.process_bt_pic_clicked)
        self.anchorDialog.pixmapChanged.connect(self.updatePic)
        self.checkbt_clickSpot.stateChanged.connect(self.process_checkbt_clickSpot)
        self.checkbt_imageRec.stateChanged.connect(self.process_checkbt_imageRec)
        pass

    def process_checkbt_clickSpot(self,event):
        if(event):
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
            pass
        else:
            pass
    def process_bt_pic_clicked(self):
        if(self.anchorDialog.isHidden()):
            self.anchorDialog.show()
        else:
            self.anchorDialog.getPixmapAtCurrentPosition()
            self.anchorDialog.hide()
        
    def updatePic(self):
        pixmap = self.anchorDialog.pixmap()
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
        self.lbl_uploadImg.setPixmap(pixmap)
        pass

    def mousePressEvent(self,event):

        pass

    def display(self,isminum=False):
        if(self.isChild):
            self.setContentsMargins(30,0,0,0)
            isminum = True
        else:
            self.setContentsMargins(0,0,0,0)
        if(isminum == True):
            self.setWidgetSpan(self.lbl_prefix,1,1)
            self.show()
            self.edit_description.hide()
            self.bt_pic.hide()
            self.bt_video.hide()
            self.bt_newfolder.hide()
            self.lbl_uploadImg.hide()
            self.checkbt_clickSpot.hide()
            self.checkbt_imageRec.hide()
            self.combo_imageRec.hide()
            
            # self.edit_sec_description.hide()
        else:
            self.setWidgetSpan(self.lbl_prefix,23,1)
            self.edit_description.show()
            self.bt_pic.show()
            self.bt_video.show()
            # self.bt_newfolder.show()
            self.lbl_uploadImg.show()
            self.checkbt_clickSpot.show()
            self.checkbt_imageRec.show()
            self.combo_imageRec.show()
            
            # self.edit_sec_description.show()
    
    def setWidgetSpan(self, widget, rowspan=1, colspan=1):
        index = self.layout.indexOf(widget)
        row, column = self.layout.getItemPosition(index)[:2]
        self.layout.addWidget(widget, row, column, rowspan, colspan)
    # def hideEvent(self,event):
    #     super().hide()
    #     self.anchorDialog.hide()
    def sig_mouseClick(self,posx,posy):
        #checkmehere don't need to show crosshair to mouse click point
        # self.posx = posx
        # self.posy = posy
        pass
    def getDatas(self):
        title = self.edit_header.toPlainText()
        description = self.edit_description.toPlainText()
        anchorPixmap = self.anchorDialog.pixmap()
        sec_description = self.edit_sec_description.toPlainText()
        return Settings.clickStep,title,description,sec_description,None,anchorPixmap,self.isChild,None

class MatchStepItem(MyFrame):

    def __init__(self,parent):

        super(MatchStepItem,self).__init__(parent)
        self.isChild = False
        self.anchorDialog = QAnchorDialog(self)
        self.__initUI()
        self.lbl_uploadImg.setStyleSheet('margin-bottom:10px;border:1px solid black')
        

    def __initUI(self):
        
        self.layout = MyGridLayout(self)
        self.edit_header = CommonHeaderTextEdit(self)
        self.lbl_icon = CommonHeaderIcon(self)
        self.lbl_icon.setPixmap(QPixmap('icons/matchstep.png'))
        self.edit_description = CommonDescriptionTextEdit(self)
        self.lbl_prefix = CommonHeaderLabel(self,isPrefix=True)
        # self.lbl_prefix.setPixmap(QPixmap('icons/stack-step-big.png'))
        self.edit_header.setPlaceholderText(Settings.stepTitlePlaceHolder)
        self.edit_description.setPlaceholderText(Settings.stepDescriptionPlaceHolder)
        

        self.bt_pic = PictureButton(self)
        self.bt_video = VideoButton(self)
        self.bt_newfolder = NewFolderButton(self)
        self.lbl_uploadImg = MyDropableLable(self)
        self.checkbt_showscrolll = QCheckBox(self)
        self.bt_upscroll = QPushButton(self)
        self.bt_downscroll = QPushButton(self)
        

        self.bt_upscroll.setMinimumHeight(20)
        self.bt_downscroll.setMinimumHeight(20)
        self.bt_upscroll.setIcon(QIcon('icons/uparrow.png'))
        self.bt_downscroll.setIcon(QIcon('icons/downarrow.png'))
        self.checkbt_showscrolll.setText('Show Scroll iocns')

        #set fixed height for some widget


        
        self.layout.addWidget(self.lbl_prefix,0,0,23,1)
        self.layout.addWidget(self.edit_header,0,1,1,19)
        self.layout.addWidget(self.lbl_icon,0,20,1,1)
        self.layout.addWidget(self.edit_description,1,1,1,20)
        
        self.layout.addWidget(self.bt_pic,2,1,1,1)
        self.layout.addWidget(self.bt_video,2,2,1,1)
        self.layout.addWidget(self.bt_newfolder,2,3,1,1)
        self.layout.addWidget(self.lbl_uploadImg,3,1,20,20)
        

        #this seems to be useless at the moment.
        self.checkbt_showscrolll.hide()
        self.bt_upscroll.hide()
        self.bt_downscroll.hide()

        #bind events
        self.anchorDialog.pixmapChanged.connect(self.updatePic)
        self.bt_pic.clicked.connect(self.process_bt_pic_clicked)
        # self.edit_header.focusOutEvent = self.processFocusout

        pass

    def processFocusout(self,event):
        
        self.anchorDialog.hide()

    def process_bt_pic_clicked(self):
        if(self.anchorDialog.isHidden()):
            self.anchorDialog.show()
        else:
            self.anchorDialog.getPixmapAtCurrentPosition()
            self.anchorDialog.hide()
        
    def updatePic(self):
        pixmap = self.anchorDialog.pixmap()
        self.lbl_uploadImg.setPixmap(pixmap)
        
        pass

    def getDatas(self):

        title = self.edit_header.toPlainText()
        description = self.edit_description.toPlainText()
        sec_description =""
        uploadPixmap = self.lbl_uploadImg.pixmap()
        anchorPixmap = self.anchorDialog.pixmap()
        
        return Settings.matchStep,title,description,sec_description,uploadPixmap,anchorPixmap,self.isChild,None
  
    def display(self,isminum = False):
        if(self.isChild):
            self.setContentsMargins(30,0,0,0)
            isminum = True
        else:
            self.setContentsMargins(0,0,0,0)
        if(isminum == True):
            #set prefix label height to header label
            self.setWidgetSpan(self.lbl_prefix,1,1)
            self.setWidgetSpan(self.lbl_uploadImg,0,0)
            self.layout.setRowStretch(2,0)
            self.edit_description.hide()
            
            self.bt_pic.hide()
            self.bt_video.hide()
            self.bt_newfolder.hide()
            self.lbl_uploadImg.hide()
            
        else:

            self.setWidgetSpan(self.lbl_prefix,23,1)
            self.setWidgetSpan(self.lbl_uploadImg,20,20)
            self.layout.setRowStretch(2,1)

            self.edit_description.show()
            self.bt_pic.show()
            self.bt_video.show()
            self.bt_newfolder.show()
            self.lbl_uploadImg.show()
    
    def setWidgetSpan(self, widget, rowspan=1, colspan=1):

        index = self.layout.indexOf(widget)
        row, column = self.layout.getItemPosition(index)[:2]
        self.layout.addWidget(widget, row, column, rowspan, colspan)

class MouseStepItem(MyFrame):

    def __init__(self,parent):

        super(MouseStepItem,self).__init__(parent)

        self.isChild = False
        self.upScroll = None
        self.anchorDialog = QAnchorDialog(self)
        self.__initUI()
        self.setStyleSheet('padding:2px')


    def __initUI(self):
        
        self.layout = MyGridLayout(self)
        self.edit_header = CommonHeaderTextEdit(self)
        self.lbl_icon = CommonHeaderIcon(self)
        self.lbl_icon.setPixmap(QPixmap('icons/mousestep.png'))
        self.edit_description = CommonDescriptionTextEdit(self)
        self.edit_header.setPlaceholderText(Settings.stepTitlePlaceHolder)
        self.edit_description.setPlaceholderText(Settings.stepDescriptionPlaceHolder)
        self.lbl_prefix = CommonHeaderLabel(self,isPrefix=True)
        # self.lbl_prefix.setPixmap(QPixmap('icons/stack-step-big.png'))
        self.optionRight = QRadioButton("Right Click")
        self.optionScroll = QRadioButton("Scroll")
        self.lbl_uploadImg = MyDropableLable(self)

        self.bt_pic = PictureButton(self)
        self.bt_upscroll = QPushButton(self)
        self.bt_downscroll = QPushButton(self)

        # self.bt_upscroll.setFixedSize(20,20)
        # self.bt_downscroll.setFixedSize(20,20)
        self.bt_upscroll.setIcon(QIcon('icons/uparrow.png'))
        self.bt_downscroll.setIcon(QIcon('icons/downarrow.png'))
        
        self.layout.addWidget(self.lbl_prefix,0,0,19,1)
        self.layout.addWidget(self.edit_header,0,1,2,18)
        self.layout.addWidget(self.lbl_icon,0,19,2,1)
        self.layout.addWidget(self.edit_description,2,1,2,19)
        self.layout.addWidget(self.optionRight,4,1,2,3)
        self.layout.addWidget(self.optionScroll,6,1,2,3)
        self.layout.addWidget(self.bt_upscroll,6,5,2,1)
        self.layout.addWidget(self.bt_downscroll,6,6,2,1)
        self.layout.addWidget(self.lbl_uploadImg,8,1,10,10)
        self.layout.addWidget(self.bt_pic,8,1,1,1)
       
        #init UI
        self.bt_upscroll.setEnabled(False)
        self.bt_downscroll.setEnabled(False)
        #bind event

        self.bt_upscroll.clicked.connect(self.processButton)
        self.bt_downscroll.clicked.connect(self.processButton)
        self.optionScroll.clicked.connect(self.processOption)

        pass

    def processOption(self):
        
        if(self.optionScroll.isChecked()):
            self.bt_upscroll.setEnabled(True)
            self.upScroll = True
            self.bt_upscroll.show()
            self.bt_downscroll.setEnabled(False)
            self.bt_downscroll.show()
        else:
            pass
        pass

    def processButton(self):
        
        if(self.bt_upscroll.isEnabled()):
            self.bt_upscroll.setEnabled(False)
            self.bt_downscroll.setEnabled(True)
            pass
        else:
            self.bt_upscroll.setEnabled(True)
            self.bt_downscroll.setEnabled(False)
        
        if(self.bt_upscroll.isEnabled()):
            self.upScroll = True
        else:
            self.upScroll = False
        print(self.upScroll)
        pass

    def display(self, isminum = False):

        if(self.isChild == True):
            self.setContentsMargins(30,0,0,0)
            isminum = True
        else:
            self.setContentsMargins(0,0,0,0)
        
        if(isminum == True):

            self.setWidgetSpan(self.lbl_prefix,2,1)
            self.setWidgetSpan(self.lbl_uploadImg,0,0)
            self.setWidgetSpan(self.bt_pic,0,0)
            self.setWidgetSpan(self.edit_description,0,0)
            self.setWidgetSpan(self.optionRight,0,0)
            self.setWidgetSpan(self.optionScroll,0,0)
            self.setWidgetSpan(self.bt_upscroll,0,0)
            self.setWidgetSpan(self.bt_downscroll,0,0)

            self.edit_description.hide()
            self.optionRight.hide()
            self.optionScroll.hide()
            self.bt_upscroll.hide()
            self.bt_downscroll.hide()
            self.lbl_uploadImg.hide()
            self.bt_pic.hide()

        else:

            self.setWidgetSpan(self.lbl_prefix,19,1)
            self.setWidgetSpan(self.lbl_uploadImg,10,10)
            # self.lbl_prefix.setMaximumHeight(300)
            self.setWidgetSpan(self.bt_pic,1,1)
            self.setWidgetSpan(self.edit_description,2,19)
            self.setWidgetSpan(self.optionRight,2,3)
            self.setWidgetSpan(self.optionScroll,2,3)
            self.setWidgetSpan(self.bt_upscroll,2,1)
            self.setWidgetSpan(self.bt_downscroll,2,1)

            self.edit_description.show()
            self.optionRight.show()
            self.optionScroll.show()
            self.bt_upscroll.show()
            self.bt_downscroll.show()
            self.lbl_uploadImg.show()
            self.bt_pic.show()

        pass

    def setWidgetSpan(self, widget, rowspan=1, colspan=1):
        index = self.layout.indexOf(widget)
        row, column = self.layout.getItemPosition(index)[:2]
        self.layout.addWidget(widget, row, column, rowspan, colspan)

    # def hideEvent(self,event):
    #     super().hide()
    #     self.anchorDialog.hide()

    def getValidation(self):
        pass
    def getDatas(self):
        title = self.edit_header.toPlainText()
        description = self.edit_description.toPlainText()
        sec_description = None
        uploadPixmap = self.lbl_uploadImg.pixmap()
        anchorPixmap = self.anchorDialog.pixmap()
        isRightClick = self.optionRight.isChecked()
        mouseState = None
        if(isRightClick == True):
            mouseState = Settings.rightClick
        elif(self.upScroll == True):
            mouseState = Settings.scrollUp
        elif(self.upScroll == False):
            mouseState = Settings.scrollDown
        else:
            mouseState = Settings.leftClick
        return Settings.mouseStep,title,description,sec_description,uploadPixmap,anchorPixmap,self.isChild,mouseState

class AttachStepItem(MyFrame):

    def __init__(self,parent):

        super(AttachStepItem,self).__init__(parent)
        self.isChild = False
        self.__initUI()
        self.setStyleSheet('padding:2px')

    def __initUI(self):
        
        pass

    # def hideEvent(self,event):
    #     super().hide()
    #     self.anchorDialog.hide()

    def getValidation(self):
        title = None
        description = None
        sec_description = None
        uploadPixmap = None
        anchorPixmap = None
        mouseState = None
        return Settings.attachStep,title,description,sec_description,uploadPixmap,anchorPixmap,self.isChild,mouseState
        

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
        self.showAllItems()
    
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

    def showAllItems(self):

        for item in self.listitems:
            if(item == self.currentItem):
                item.display(isminum=False)
                item.anchorDialog.show()
                pass
            else:
                # item.display(isminum=True)
                # item.display(isminum=False)#checkmehere
                item.anchorDialog.hide()

    def eventFilter(self,source,event):

        if event.type() == QEvent.FocusIn and source is not None:
            self.currentItem = source.parentWidget()
            self.showAllItems()
            return super(MyListWidget,self).eventFilter(source,event)

        elif event.type() == QEvent.MouseButtonPress and type(source).__name__ == 'CommonHeaderLabel':
            #change this item as child
            self.currentItem = source.parentWidget()
            self.currentItem.isChild = not self.currentItem.isChild
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

    def __init__(self,parent):
        super(TeacherLandingPage, self).__init__(parent)
        self.parent = parent
        layout = self.createLayOut()
        self.setLayout(layout)
        

    def createLayOut(self):

        self.toolbarfirst  = TeacherFirstToolbar(self)
        self.toolbarsec = TeacherSecondToolbar(self)
        self.tree = MyTree(self)
        self.toolbarfirst.bt_search.clicked.connect(self.find_item_with_name)

        vbox = MyVBoxLayout(self)

        #add all frame to a container.

        vbox.addWidget(self.toolbarfirst)
        vbox.addWidget(self.toolbarsec)
        vbox.addWidget(self.tree)
        vbox.addStretch(1)

        return vbox

    def find_item_with_name(self):

        self.tree.find_button_clicked('acer')

class TeacherNewLessionPage(MyContainer):
    procDone = pyqtSignal(str)
    def __init__(self,parent):

        super(TeacherNewLessionPage,self).__init__(parent)
        self.__initUI()

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

        self.newLessonbar.frame.mousePressEvent = self.gotoNewLessonPage
        self.Secondtoolbar.edit_lesson_title.textChanged.connect(self.newLessonbar.setText)
        self.Secondtoolbar.anchorDialog.pixmapChanged.connect(self.pixmapChanged)


        
        return self.layout
    
    def pixmapChanged(self):
        self.newLessonbar.lbl_icon.setPixmap(self.Secondtoolbar.anchorDialog.pixmap())

    def processTitleChanged(self,str_title):
        pass
    
    def addItem(self,itemtype):
        
        if(itemtype == 'attach'):
            self.newLessonbar.listWidget.insertItem(None)
            pass
        elif(itemtype == 'click'):
            if(self.newLessonbar.isHidden()):
                if(len(self.newLessonbar.listWidget.listitems) == 0):
                    pass
                else:
                    self.gotoStepPage()
                    return
            self.newLessonbar.listWidget.insertItem(ClickStepItem(self))
            pass
        elif(itemtype == 'cloud'):
            self.newLessonbar.listWidget.insertItem(None)
            pass
        elif(itemtype == 'look'):
            self.newLessonbar.listWidget.insertItem(LookStepItem(self))
            pass
        elif(itemtype == 'match'):
            self.newLessonbar.listWidget.insertItem(MatchStepItem(self))
            pass
        elif(itemtype == 'mouse'):
            self.newLessonbar.listWidget.insertItem(MouseStepItem(self))
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
        
        self.newLessonbar.hide()
        self.Secondtoolbar.show()
        
        #hide lessonwidget and anchordialgo
        if(self.newLessonbar.listWidget.currentItem is not None):
            self.newLessonbar.listWidget.currentItem.anchorDialog.hide()
    
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
    
    def setText(self,str_text):
        self.lbl_lessonTitle.setText(str_text)
        pass

    def setLabelIcon(self, label = "Title",iconPath='icons/smile.png'):
        # self.lbl_lessonTitle.setText(label)
        # self.lbl_icon.setPixmap(QPixmap(iconPath))
        pass

class TeacherTabWidget(MyContainer):
    gotoStudentTab = pyqtSignal(str)
    def __init__(self,parent):
        super(TeacherTabWidget,self).__init__(parent)
        self.currentWidget = None
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
        #event process to go to landing page
        self.landing_page.toolbarsec.bt_edit.clicked.connect(self.gotoLooksteppage)
        self.lookstep_page.firsttoolbar.bt_book.clicked.connect(self.gotoLandingpage)
        
        #event binding
        self.lookstep_page.procDone.connect(self.gotoStudentTab)

    def getValidation(self):
        return self.lookstep_page.getValidation()
    def hideAllButCurrent(self):
        self.landing_page.hide()
        self.lookstep_page.hide()
        self.currentWidget.show()

    def gotoLooksteppage(self,param = 0):
        self.currentWidget = self.lookstep_page
        self.hideAllButCurrent()
        if(param == Settings.gotoLessson):
            self.lookstep_page.gotoNewLessonPage(None)
            pass
        elif(param == Settings.gotoStep):
            self.lookstep_page.gotoStepPage()
            pass


    def showConfirmDlg(self):
        if(CustomDialog.showStandardMsgbox(self.window(),"Will you exit creation of project?")):
            return True
        else:
            return False
        pass
    
    def gotoLandingpage(self):
        
        if self.showConfirmDlg():
            self.currentWidget = self.landing_page
            self.hideAllButCurrent()
        else:
            pass

    # def hideEvent(self,event):
    #     self.gotoLandingpage()









