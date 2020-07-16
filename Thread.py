
from threading import Thread
from Setting import Settings
from PyQt5.QtCore import pyqtSignal,pyqtSlot

from ProjectMgr.UpDownloadProject import UploadProject,DownloadProject
import Globals
import os
import MyUtil

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
        self.localPath = None
        self.remotePath = None
        self.mode = None

    def run(self):

        self.parent.sig_startUpDown.emit(0)

        if self.mode == Settings.refreshProjectsListMode:
            data = MyUtil.getDataFromBucket()
            self.parent.sig_NewBucketData.emit(data)
            pass
        else:
            if(self.isUpLoad == True):
                
                #upload project
                if(self.localPath is None):
                    return
                UploadProject("",self.localPath)
                pass

            else:

                if(self.remotePath is None or self.localPath is None):
                    return
                else:
                    DownloadProject(self.remotePath,self.localPath)

        self.parent.sig_startUpDown.emit(1)

        pass
















