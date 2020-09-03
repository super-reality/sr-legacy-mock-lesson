from ProjectMgr import LocalMgr
import os
from Setting import Settings
from MyUtil import NeonGlowText
projectmgr = LocalMgr.LocalProjectMgr()
effectEngine = NeonGlowText(None)
def getAbsolutePathFromNodePath(path = None):
    if(path is None):
        return

    result = os.path.join(os.getcwd(),Settings.projectTeacherPath,path)
    return result
