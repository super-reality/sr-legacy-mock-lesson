import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, \
QAction, QTabWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QFrame,QLabel,QSlider,QScrollArea,QCheckBox,QSizePolicy,QFileDialog,QDockWidget, QDialog , QComboBox, QHBoxLayout
from PyQt5.QtGui import QIcon,QFont,QCursor,QPixmap
from PyQt5.QtCore import pyqtSlot, Qt, QSize,QEvent
from Setting import Settings
import webbrowser


class MyCommonButton(QPushButton):
    def __init__(self,parent=None):
        super(MyCommonButton, self).__init__(parent)
        self.setFixedSize(20,20)
    def enterEvent(self,event):
        self.setCursor(QCursor(Qt.PointingHandCursor))

class PlayResumeButton(MyCommonButton):
    def __init__(self,parent):
        super(PlayResumeButton, self).__init__(parent)
        self.isPlaying = False
        self.__initUI()
    def __initUI(self):
        self.setIcon(QIcon('icons/play.png'))
        self.clicked.connect(self.changeState)
        pass
    def changeState(self):
        self.isPlaying = (not self.isPlaying)
        if(not self.isPlaying):
            self.setIcon(QIcon('icons/play.png'))
        else:
            self.setIcon(QIcon('icons/resume.png'))
    def reset(self):
        self.isPlaying = False
        self.setIcon(QIcon('icons/play.png'))

class CarmineButton(MyCommonButton):
    def __init__(self,parent):
        super(CarmineButton, self).__init__(parent)
        self.__initUI()
    def __initUI(self):
        self.setIcon(QIcon('icons/carmine.png'))
        pass

class SpeakerButton(MyCommonButton):
    def __init__(self,parent):
        super(SpeakerButton, self).__init__(parent)
        self.__initUI()
    def __initUI(self):
        self.setIcon(QIcon('icons/speaker.png'))
        pass

class SearchButton(MyCommonButton):
    def __init__(self,parent):
        super(SearchButton, self).__init__(parent)
        self.__initUI()
    def __initUI(self):
        self.setIcon(QIcon('icons/search.png'))
        pass

class QuestionButton(MyCommonButton):
    def __init__(self,parent):
        super(QuestionButton, self).__init__(parent)
        self.__initUI()
    def __initUI(self):
        self.setIcon(QIcon('icons/question.png'))
        
        pass

class SocialButton(MyCommonButton):
    def __init__(self,parent):
        super(SocialButton, self).__init__(parent)
        self.__initUI()
    def __initUI(self):
        self.setIcon(QIcon('icons/social.png'))
        pass

class BookButton(MyCommonButton):
    def __init__(self,parent):
        super(BookButton, self).__init__(parent)
        self.__initUI()
    def __initUI(self):
        self.setIcon(QIcon('icons/book.png'))
        pass

class EditButton(MyCommonButton):
    def __init__(self,parent):
        super(EditButton, self).__init__(parent)
        self.__initUI()
    def __initUI(self):
        self.setIcon(QIcon('icons/edit.png'))
        pass

class NewFolderButton(MyCommonButton):
    def __init__(self,parent):
        super(NewFolderButton, self).__init__(parent)
        self.__initUI()
    def __initUI(self):
        self.setIcon(QIcon('icons/newfolder.png'))
        pass

class SearchPlusButton(MyCommonButton):
    def __init__(self,parent):
        super(SearchPlusButton, self).__init__(parent)
        self.__initUI()
    def __initUI(self):
        self.setIcon(QIcon('icons/searchplus.png'))
        pass

class CloudButton(MyCommonButton):
    def __init__(self,parent):
        super(CloudButton, self).__init__(parent)
        self.__initUI()
    def __initUI(self):
        self.setIcon(QIcon('icons/cloud.png'))
        pass
    def enterEvent(self,event):
        self.setCursor(QCursor(Qt.PointingHandCursor))

class CloseButton(MyCommonButton):
    def __init__(self,parent):
        super(CloseButton,self).__init__()
        self.parent = parent
        self.setStyleSheet('border:None')
        self.setIcon(QIcon('icons/close.png'))

    def enterEvent(self,event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
    def leaveEvent(self,event):
        self.setWindowOpacity(0.1)

class TitleButton(MyCommonButton):
    def __init__(self,parent):
        super(TitleButton,self).__init__()
        self.parent = parent
        self.__initUI()
        self.setStyleSheet(' border:None')
        self.clicked.connect(self.openUrl)
    def __initUI(self):
        self.setIcon(QIcon('icons/logo.png'))
        self.setText('OpenVerse')
    def enterEvent(self,event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
    def openUrl(self):
        webbrowser.open('http://www.openverse.co/', new=2)

class CommonButton(MyCommonButton):
    def __init__(self,parent,title):
        super(CommonButton,self).__init__()
        self.parent = parent
        self.setStyleSheet('background-color:rgb(240,240,240); border:None')
        self.title = title
        if(self.title == 'Profile'):
            self.clicked.connect(self.openProfile)
        elif(self.title == 'Setting'):
            self.clicked.connect(self.openSetting)
        else:
            pass

    def enterEvent(self,event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
    def leaveEvent(self,event):
        self.setWindowOpacity(0.1)
    
    def openProfile(self):
        profile = QDialog(self)
        profile.setWindowTitle("Profile")
        profile.setFixedSize(400,400)
        profile.show()
        pass
    
    def openSetting(self):
        Setting = QDialog(self)
        Setting.setWindowTitle("Setting")
        Setting.setFixedSize(400,400)
        Setting.show()
        pass

class LookStepButton(MyCommonButton):
    def __init__(self,parent):
        super(LookStepButton,self).__init__()
        self.parent = parent
        self.setStyleSheet('border:None')
        self.setIcon(QIcon('icons/lookstep.png'))

    def enterEvent(self,event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
    def leaveEvent(self,event):
        self.setWindowOpacity(0.1)

class ClickStepButton(MyCommonButton):
    def __init__(self,parent):
        super(ClickStepButton,self).__init__()
        self.parent = parent
        self.setStyleSheet('border:None')
        self.setIcon(QIcon('icons/clickstep.png'))

    def enterEvent(self,event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
    def leaveEvent(self,event):
        self.setWindowOpacity(0.1)

class MatchStepButton(MyCommonButton):
    def __init__(self,parent):
        super(MatchStepButton,self).__init__()
        self.parent = parent
        self.setStyleSheet('border:None')
        self.setIcon(QIcon('icons/matchstep.png'))

    def enterEvent(self,event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
    def leaveEvent(self,event):
        self.setWindowOpacity(0.1)

class MouseStepButton(MyCommonButton):
    def __init__(self,parent):
        super(MouseStepButton,self).__init__()
        self.parent = parent
        self.setStyleSheet('border:None')
        self.setIcon(QIcon('icons/mousestep.png'))

    def enterEvent(self,event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
    def leaveEvent(self,event):
        self.setWindowOpacity(0.1)

class AttachStepButton(MyCommonButton):
    def __init__(self,parent):
        super(AttachStepButton,self).__init__()
        self.parent = parent
        self.setStyleSheet('border:None')
        self.setIcon(QIcon('icons/attachstep.png'))

    def enterEvent(self,event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
    def leaveEvent(self,event):
        self.setWindowOpacity(0.1)

class PlayButton(MyCommonButton):
    def __init__(self,parent):
        super(PlayButton,self).__init__()
        self.parent = parent
        self.setStyleSheet('border:None')
        self.setIcon(QIcon('icons/play.png'))

    def enterEvent(self,event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
    def leaveEvent(self,event):
        self.setWindowOpacity(0.1)

class VideoButton(MyCommonButton):
    def __init__(self,parent):
        super(VideoButton,self).__init__()
        self.parent = parent
        self.setStyleSheet('border:None')
        self.setIcon(QIcon('icons/video.png'))

    def enterEvent(self,event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
    def leaveEvent(self,event):
        self.setWindowOpacity(0.1)

class PictureButton(MyCommonButton):

    def __init__(self,parent):
        super(PictureButton,self).__init__()
        self.parent = parent
        self.setStyleSheet('border:None')
        self.setIcon(QIcon('icons/camera.png'))

    def enterEvent(self,event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
    def leaveEvent(self,event):
        self.setWindowOpacity(0.1)

class DeleteButton(MyCommonButton):

    def __init__(self,parent):
        super(DeleteButton,self).__init__()
        self.parent = parent
        self.setStyleSheet('border:None')
        self.setIcon(QIcon('icons/delete.png'))

    def enterEvent(self,event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
    def leaveEvent(self,event):
        self.setWindowOpacity(0.1)

class NewProjectButton(MyCommonButton):

    def __init__(self,parent):
        super(NewProjectButton,self).__init__()
        self.parent = parent
        self.setStyleSheet('border:None')
        self.setIcon(QIcon('icons/newProject.png'))

    def enterEvent(self,event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
    def leaveEvent(self,event):
        self.setWindowOpacity(0.1)

class SignalButton(MyCommonButton):

    def __init__(self,parent):
        super(SignalButton,self).__init__()
        self.parent = parent
        self.setStyleSheet('border:None')
        self.setIcon(QIcon('icons/signal.png'))

    def enterEvent(self,event):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
    def leaveEvent(self,event):
        self.setWindowOpacity(0.1)

class MyCheckBox(QCheckBox):
    def __init__(self,parent):
        super(MyCheckBox,self).__init__(parent)
        self.__initUI()
        self.setFont(QFont('Arial',16))
    def __initUI(self):
        pass

class MyComboBox(QComboBox):
    def __init__(self,parent):

        super(MyComboBox,self).__init__(parent)
        self.__initUI()
        self.setFont(QFont('Arial',16))
        pass
    def __initUI(self):
        pass
    def wheelEvent(self,event):
        event.ignore()