
from threading import Thread
from Setting import Settings
from PyQt5.QtCore import pyqtSignal,pyqtSlot
from ProjectMgr.UpDownloadProject import UploadProject,DownloadProject
class MyCommonThread(Thread):
    
    """
    Class that represents a consumer.
    """

    def __init__(self,parent=None,**kwargs):
        """
        """
        Thread.__init__(self,daemon=True)
        self.parent = parent

    # def run(self):
    #     for i  in range(1,10):
    #         self.parent.sig_increase.emit(i)
    #     pass

class UpDownLoadThread(MyCommonThread):
    
    def __init__(self,parent,**kwargs):
        MyCommonThread.__init__(self,parent=parent,daemon=True)
        self.isUpLoad = True
    def run(self):
        self.parent.sig_startUpDown.emit(0)
        if(self.isUpLoad == True):
            #upload project
            UploadProject(self.parent.projectmgr.getUploadPath())
            pass
        else:
            DownloadProject(self.parent.projectmgr.getDownLoadPath())
            #download project
            pass
        self.parent.sig_startUpDown.emit(1)
        pass


    
        