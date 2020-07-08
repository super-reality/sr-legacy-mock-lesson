import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, \
QAction, QTabWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QFrame,QLabel,QSlider,QScrollArea,QCheckBox,QSizePolicy,QFileDialog,QDockWidget, QDialog
from PyQt5.QtGui import QIcon,QFont,QCursor,QPixmap,QPaintDevice,QPainter,QPen
from PyQt5.QtCore import pyqtSlot, Qt, QSize,QEvent,QMargins
from Setting import Settings
from Mybutton import *
from TeacherComponent import *
from StudentComponent import *
from Container import CustomDialog
from ProjectMgr.LocalMgr import LocalProjectMgr
from QtWaitingSpinner.pyqtspinner.spinner import WaitingSpinner
from Thread import UpDownLoadThread
import logging



class MyTableWidget(QWidget):
    sig_startUpDown = pyqtSignal(int)
    def __init__(self, parent):
        super(MyTableWidget, self).__init__(parent)

        self.parent = parent

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(3,4,4,4)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab_student = StudentTabWidget(self)
        self.tab_teacher = TeacherTabWidget(self)
        self.tab_explore = QWidget(self)
        self.tab_xrclassroom = QWidget(self)
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab_student,"Student")
        self.tabs.addTab(self.tab_teacher,"Teacher")
        self.tabs.addTab(self.tab_explore,"Explore")
        self.tabs.addTab(self.tab_xrclassroom,"Social")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        #binding event
        self.tab_teacher.gotoStudentTab.connect(self.gotoStudentTab)

        #projectmgr setup
        self.projectmgr = LocalProjectMgr()
        self.waitForLoading = WaitingSpinner(self)
        self.threadForUpDown = UpDownLoadThread(self)

        #event bind
        self.tab_student.sig_bt_signal.connect(self.sig_bt_signal)
        self.tab_student.sig_bt_carmin.connect(self.sig_bt_carmin)
        self.sig_startUpDown.connect(self.startUpDown)
    
    def startUpDown(self,state = -1):
        if(state == 0):
            self.waitForLoading.start()
        else:
            self.waitForLoading.stop()
            

    def sig_bt_carmin(self):
        projectList = self.projectmgr.getProjectNameList()
        self.tab_student.setupProjectList(projectList)
        pass
    def sig_bt_signal(self):
        if(self.threadForUpDown.isAlive() == False):
            self.threadForUpDown = UpDownLoadThread(self)
            self.threadForUpDown.isUpLoad = False
            self.threadForUpDown.start()
        pass

    def gotoStudentTab(self):

        if(CustomDialog.showStandardMsgbox(self.window(),"Will you finish project setup?") == True):
            
            if self.tab_teacher.getValidation() == Settings.valid:
                """
                #prepare for creating new lesson by removing old items and widgets that are hidden
                do something here for that
                """
                #goto student tab to test.
                self.waitForLoading.start()
                if self.saveProjectToLocal() == False:
                    pass
                else:
                    self.tabs.setCurrentWidget(self.tab_student)
                self.waitForLoading.stop()
            else:
                pass
        
        else:
            pass

    def saveProjectToLocal(self):

        #first Create Project
        projectName = self.tab_teacher.lookstep_page.Secondtoolbar.edit_lesson_title.text()
        title = projectName
        description = self.tab_teacher.lookstep_page.Secondtoolbar.edit_lesson_descripiton.getText()
        tags = self.tab_teacher.lookstep_page.Secondtoolbar.edit_lesson_tag.text()
        pixmapRefer = self.tab_teacher.lookstep_page.Secondtoolbar.lbl_picture.pixmap()
        pixmapAnchor = self.tab_teacher.lookstep_page.Secondtoolbar.anchorDialog.pixmap()
        if(self.tab_teacher.lookstep_page.Secondtoolbar.isPixmapSelected):
            pass
        else:
            pixmapRefer = None
            pixmapAnchor = None        
        
        try:
            resp = self.projectmgr.createProject(projectName,title,description,tags,pixmapRefer,pixmapAnchor)
            if(resp == Settings.projectAlreadyExist):
                dlg_resp = CustomDialog.showStandardMsgbox(self.window(),"Project Folder Already Exist, Will you replace it with new one?")
                if(dlg_resp):
                    
                    self.projectmgr.deleteCurrentProject()
                    
                    self.projectmgr.createProject(projectName,title,description,tags,pixmapRefer,pixmapAnchor)
                else:
                    return False
            elif(resp == Settings.projectNameNotSpecified):
                return False
            else:
                pass
        except:
            logging.exception(Settings.projectFileManagementError)
            return False
            pass

        
        #create step
        try:
            for item in self.tab_teacher.lookstep_page.newLessonbar.listWidget.getItemsList():
                
                if( Settings.lookStep in  type(item).__name__):
                    #create lookstep
                    params = item.getDatas()
                    if(item.anchorDialog is not None):
                        item.anchorDialog.hide()
                    self.projectmgr.createStep(*params)
                    pass
                elif(Settings.clickStep in type(item).__name__):
                    params = item.getDatas()
                    if(item.anchorDialog is not None):
                        item.anchorDialog.hide()
                    self.projectmgr.setClickArea(item.posx,item.posy,item.posWidth,item.posHeight)
                    self.projectmgr.createStep(*params)
                    #create clickstep
                    pass
                elif(Settings.matchStep in type(item).__name__):
                    #create matchstep
                    params = item.getDatas()
                    if(item.anchorDialog is not None):
                        item.anchorDialog.hide()
                    self.projectmgr.createStep(*params)
                    pass
                elif(Settings.mouseStep in type(item).__name__):
                    #create mouseStep
                    params = item.getDatas()
                    if(item.anchorDialog is not None):
                        item.anchorDialog.hide()
                    self.projectmgr.createStep(*params)
                    pass
                elif(Settings.piskelStep in type(item).__name__):
                    params = item.getDatas()
                    if(item.anchorDialog is not None):
                        item.anchorDialog.hide()
                    self.projectmgr.createStep(*params)
                    #create piskelStep
                    pass
                else:
                    pass
        except:
            logging.exception(Settings.projectStepCreationError)
            return False
            
        #save project and exit
        
        self.projectmgr.saveLocalProject()
        if(self.threadForUpDown.isAlive() == False):
            self.threadForUpDown = UpDownLoadThread(self)
            self.threadForUpDown.isUpLoad = True
            self.threadForUpDown.start()
        
        return True
        





