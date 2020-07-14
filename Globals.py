from ProjectMgr import LocalMgr
import os
from Setting import Settings

projectmgr = LocalMgr.LocalProjectMgr()

def getAbsolutePathFromNodePath(path = None):
    if(path is None):
        return

    result = os.path.join(os.getcwd(),Settings.projectTeacherPath,path)
    return result
