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
import Globals


class MyTableWidget(QWidget):
    sig_startUpDown = pyqtSignal(int)
    sig_playLesson = pyqtSignal(str)
    sig_NewBucketData = pyqtSignal(list)
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

        

        #projectmgr setup
        self.projectmgr = Globals.projectmgr
        self.waitForLoading = WaitingSpinner(self)
        self.threadForUpDown = UpDownLoadThread(self)

        #event bind
        self.tab_student.sig_bt_signal.connect(self.sig_bt_signal)
        self.tab_student.sig_bt_carmin.connect(self.sig_bt_carmin)
        self.tab_student.sig_bt_resumeplay_with_Path.connect(self.sig_bt_resumeplay_with_Path)
        self.sig_playLesson.connect(self.tab_student.changeProjectPathForLesson)
        self.tab_teacher.sig_upLoadFolder.connect(self.UploadFolderToCloud)
        self.sig_NewBucketData.connect(self.refreshStudentTab)
        self.tab_teacher.gotoStudentTab.connect(self.gotoStudentTab)
        self.sig_startUpDown.connect(self.startUpDown)
        self.tab_teacher.sig_saveCurrentProject.connect(self.saveProjectToLocal)
        self.tab_student.sig_doublClickedItem.connect(self.processDoubleClickItemEvent)

        self.relativePath = None
        self.isStarting = False

    def processDoubleClickItemEvent(self,path):
        #if leaf pass
        self.relativePath = path
        path = Globals.projectmgr.getProjectPathFromRelativePath(isTeacherProject=False,relativePath=path)

        #if path not exist , then download it first
        if os.path.exists(path) == False:
            self.sig_bt_signal_copy()
            pass

        if MyUtil.isLeaf(path):
            pass
        else:
            return
        self.sig_bt_resumeplay_with_Path(path)
        #change play button to resume button
        self.tab_student.changeStatePlayButton()
        pass

    def UploadFolderToCloud(self,path=None):
        if(path is None):
            return
        self.uploadProjectsToAws()

    def startUpDown(self,state = -1):
        
        if(state == 0):
            self.waitForLoading.start()
        else:
            self.waitForLoading.stop()
            if(self.isStarting == True):
                self.isStarting = False
                #emit signal to play lesson
                self.sig_playLesson.emit(self.relativePath)
        

    def sig_bt_resumeplay_with_Path(self,path):
        
        self.relativePath = path
        if(self.tab_student.studentList.isHidden() == True):
            # just go to student body page
            self.sig_playLesson.emit(self.relativePath)
            return
        if os.path.exists(Globals.projectmgr.getProjectPathFromRelativePath(isTeacherProject=False,relativePath=self.relativePath)):
            #this is project dir go to step page directly
            self.sig_playLesson.emit(self.relativePath)
            return
        
        self.downLoadProjectsFromAws()
        self.isStarting = True

        pass

    def refreshStudentTab(self,data):
        self.tab_student.refresh(data)
        pass
    def sig_bt_carmin(self):
        if(self.tab_student.studentList.isHidden()):
            self.tab_student.setupProjectList("")
            pass
        else:
            self.refreshProjectList()
            pass
        pass
    
    def sig_bt_signal(self):
        self.refreshProjectList()
        pass

    def sig_bt_signal_copy(self):
        self.relativePath = self.tab_student.getCurrentPath()
        if(self.relativePath is None):
            self.refreshProjectList()
            pass
        else:
            self.downLoadProjectsFromAws()
        pass
    def refreshProjectList(self):
        if(self.threadForUpDown.isAlive() == False):
            self.threadForUpDown = UpDownLoadThread(self)
            self.threadForUpDown.mode = Settings.refreshProjectsListMode
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
                if self.saveProjectToLocal(isUpload=True) == False:
                    pass
                else:
                    self.tabs.setCurrentWidget(self.tab_student)
                self.waitForLoading.stop()
            else:
                pass
        
        else:
            pass

    def saveProjectToLocal(self,isUpload=False):

        #first Create Project
        projectName = self.tab_teacher.lookstep_page.Secondtoolbar.edit_lesson_title.text()
        title = projectName
        description = self.tab_teacher.lookstep_page.Secondtoolbar.edit_lesson_descripiton.getText()
        tags = self.tab_teacher.lookstep_page.Secondtoolbar.edit_lesson_tag.text()
        pixmapRefer = self.tab_teacher.lookstep_page.Secondtoolbar.lbl_picture.pixmap()
        pixmapAnchor = self.tab_teacher.lookstep_page.Secondtoolbar.anchorDialog.currentPixmap
        anchorPosx = self.tab_teacher.lookstep_page.Secondtoolbar.anchorDialog.lastPosx
        anchorPosy = self.tab_teacher.lookstep_page.Secondtoolbar.anchorDialog.lastPosy
        anchorWidth = self.tab_teacher.lookstep_page.Secondtoolbar.anchorDialog.lastWidth
        anchorHeight = self.tab_teacher.lookstep_page.Secondtoolbar.anchorDialog.lastHeight

        try:
            resp = self.projectmgr.createProject(projectName,title,description,tags,pixmapRefer,pixmapAnchor, anchorPosx,anchorPosy,anchorWidth,anchorHeight)
            if(resp == Settings.projectAlreadyExist):
                # dlg_resp = CustomDialog.showStandardMsgbox(self.window(),Settings.projectAlreadyExistErrorText)
                self.projectmgr.deleteCurrentProject()
                logging.info("delete current Project "+ self.projectmgr.projectPath + " recreating project")
                self.projectmgr.createProject(projectName,title,description,tags,pixmapRefer,pixmapAnchor, anchorPosx,anchorPosy,anchorWidth,anchorHeight)

            elif(resp == Settings.projectNameNotSpecified):
                return False
            else:
                pass
        except:
            logging.exception(Settings.projectFileManagementError)
            return False

        
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

        if(isUpload == True):
            self.uploadProjectsToAws()
        return True
        
    def uploadProjectsToAws(self):

        if(self.threadForUpDown.isAlive() == False):
            self.threadForUpDown = UpDownLoadThread(self)
            self.threadForUpDown.localPath = self.projectmgr.projectPath
            self.threadForUpDown.isUpLoad = True
            self.threadForUpDown.start()

        pass

    def downLoadProjectsFromAws(self):

        if(self.threadForUpDown.isAlive() == False):
            self.threadForUpDown = UpDownLoadThread(self)
            if(self.relativePath is None):
                return Settings.selectProjectBeforeDownloadingError
            self.threadForUpDown.localPath = os.path.join(self.projectmgr.getStudentProjectsLocalPath())
            self.threadForUpDown.remotePath = self.relativePath
            self.threadForUpDown.isUpLoad = False
            self.threadForUpDown.start()

        return True






