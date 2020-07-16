
import json
import pyautogui
import cv2
import numpy as np
import random
import os
import sys


sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from Setting import Settings
import shutil
from ProjectMgr.UpDownloadProject import DownloadProject,UploadProject
import MyUtil
import logging

# define the name of the directory to be created

class LocalProjectMgrVersion1:
    
    def __init__(self):
        #create project local directory if not exist.
        
        self.__localPathForTeacher = os.path.join(os.getcwd(),Settings.projectTeacherPath)
        self.__localPathForStudent = os.path.join(os.getcwd(),Settings.projectStudentPath)
        self.posx = None
        self.posy = None
        self.posWidth = None
        self.posHeight = None
        self.projectPath = None
        self.curStep = None
        self.currentProjectPath = None
        self.json = None

        self.__createDir()

    def changeProjectPath(self):
        self.projectPath = os.path.join(self.__localPathForTeacher,self.currentProjectPath)
        pass

    def getProjectPathFromRelativePath(self,isTeacherProject=False,relativePath=None):
        if relativePath is None:
            return
        if(isTeacherProject):
            return os.path.join(self.__localPathForTeacher,relativePath)
        else:
            return os.path.join(self.__localPathForStudent,relativePath)

    def getAbsCurrentProjectPath(self):
        if(self.currentProjectPath is None):
            return self.__localPathForTeacher
        path = os.path.join(self.__localPathForTeacher,self.currentProjectPath)
        return path
        
    def getStudentProjectsLocalPath(self):
        return self.__localPathForStudent
    def getTeacherProjectsLocalPath(self):
        return self.__localPathForTeacher
    def __createDir(self):

        if not os.path.exists(self.__localPathForTeacher):
            os.makedirs(self.__localPathForTeacher)
            print("Directory " , self.__localPathForTeacher ,  " Created ")
        else:    
            print("Directory " , self.__localPathForTeacher ,  " already exists")

        if not os.path.exists(self.__localPathForStudent):
            os.makedirs(self.__localPathForStudent)
            print("Directory " , self.__localPathForStudent ,  " Created ")
        else:    
            print("Directory " , self.__localPathForStudent ,  " already exists")

    def deleteCurrentProject(self):
        if os.path.exists(self.projectPath):
            shutil.rmtree(self.projectPath,ignore_errors=True)
        
    def createTemplateProject(self,treePath=None):
        if(treePath is None):
            return
        if os.path.exists(treePath):
            shutil.rmtree(treePath)
        os.mkdir(treePath)
        filePath = os.path.join(treePath,Settings.projectFileName)
        templateData = {"metaInfo": {"baseImgUrl": ""}, "header": {"title": "title", "description": "", "imageName": None, "tags": "lesson", "anchorImageName": None}, "lessons": []}
        with open(filePath,mode='a') as outfile:
            json.dump(templateData,outfile)
            pass
        pass

    def createProject(self,projectName=None,title='title',description='description',tags=None,referPixmap=None,anchorPixmap=None):
        
        """
        create project dir named by projectName in projects folder
        if it is successfully created, then return True, else return error text
        """
        
        
        if(self.projectPath is None):
            logging.info("project Path is not defined")
            return Settings.projectNameNotSpecified
        
        if not os.path.exists(self.projectPath):
            os.makedirs(self.projectPath)
            logging.info("creating project success")
        else:
            logging.info("creating project failed ")
            return Settings.projectAlreadyExist
        try:
            renamePath = os.path.join(os.path.dirname(self.projectPath),title)
            os.rename(self.projectPath,renamePath)
        except:
            logging.info("project rename failed")
        self.projectPath = renamePath
        #change project directory name
        
        # create icon file and get file path of it.
        self.json = {
            "metaInfo":{"baseImgUrl":""},
            "header":{"title":"Title","description":"","imageName":"","tags":"","anchorImageName":""},
            "lessons":[
            ]
        }

        imageName = None
        anchorImageName = None
        
        try:
            filename,filepath = self.getFileNameTobeCreated()
            
            
            if(referPixmap is not None):
                # referPixmap.save(filepath)
                # imageName = filename
                pass
            filename,filepath = self.getFileNameTobeCreated()
            if(anchorPixmap is not None):
                anchorImageName = filename
                anchorPixmap.save(filepath)
            pass
            
        except:
            pass
        
        self.json['header']['title'] = title
        self.json['header']['description'] = description
        self.json['header']['tags'] = tags
        self.json['header']['imageName'] = imageName
        self.json['header']['anchorImageName'] = anchorImageName
        
        return True

    def getFileNameTobeCreated(self):

        fileName = str(random.randint(1,10000)) + '.png'
        filePath = os.path.join(self.projectPath,fileName)
        
        while(os.path.exists(filePath)):
            fileName = str(random.randint(1,10000)) + '.png'
            filePath = os.path.join(self.projectPath,fileName)
        
        return fileName,filePath
    
    def createIconFile(self,posx,posy,W,H,iconPath):
        """
        get screenshot with posx,posy,w,h and save it to local file 
        and return the created file name
        else return None
        """
        if(W == 0 or H == 0):
            return None
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        image = image[posy:posy+H,posx:posx+W]
        fileName = str(random.randint(1,10000)) + '.png'
        filePath = os.path.join(iconPath,fileName)
        
        while(not os.path.exists(filePath)):
            fileName = str(random.randint(1,10000)) + '.png'
            filePath = os.path.join(iconPath,fileName)
        try:
            cv2.imwrite(filePath,image)
        except:
            return None

        return fileName

    def setPos(self,posx,posy):
        self.posx = posx
        self.posy = posy
        pass

    def setClickArea(self,posx,posy, width, height):
        self.posx = posx
        self.posy = posy
        self.posHeight = height
        self.posWidth = width

    def createStep(self,stepType=None,title='',description='',sec_description='',uploadPixmap=None,anchorPixmap=None,isChild=False,mouseState=None,matchText=None):
        
        """
        create step. if success, return true else return error string
        """
        
        anchorPixmapName =None
        uploadPixmapName = None
        
        fileName,filePath = self.getFileNameTobeCreated()
        if(anchorPixmap is not None):
            
            anchorPixmap.save(filePath)
            anchorPixmapName = fileName
        fileName,filePath = self.getFileNameTobeCreated()
        if(uploadPixmap is not None):
            
            uploadPixmap.save(filePath)
            uploadPixmapName = fileName
        
        obj = {}
        
        if(stepType == Settings.lookStep):
            obj['type'] = stepType
            obj['title'] = title
            obj['description'] = description
            obj['isChild'] = 'false' if not isChild else 'true'
            obj['anchorPixmap'] = anchorPixmapName
            pass
        elif(stepType == Settings.clickStep):
            obj['type'] = stepType
            obj['title'] = title
            obj['description'] = description
            obj['sec_description'] = sec_description
            obj['isChild'] = 'false' if not isChild else 'true'
            obj['spotposx'] = self.posx
            obj['spotposy'] = self.posy
            obj['spotwidth'] = self.posWidth
            obj['spotheight'] = self.posHeight
            obj['anchorPixmap'] = anchorPixmapName
            obj['matchText'] = matchText
            pass
        elif(stepType == Settings.matchStep):
            obj['type'] = stepType
            obj['title'] = title
            obj['description'] = description
            obj['anchorPixmap'] = anchorPixmapName
            obj['isChild'] = 'false' if not isChild else 'true'
            pass
        elif(stepType == Settings.mouseStep):
            obj['type'] = stepType
            obj['title'] = title
            obj['description'] = description
            obj['sec_description'] =sec_description
            obj['uploadPixmap'] =uploadPixmapName
            obj['anchorPixmap'] =anchorPixmapName
            obj['mouseState'] =mouseState
            obj['isChild'] = 'false' if not isChild else 'true'
            pass
        elif(stepType == Settings.attachStep):
            obj['type'] = stepType
            # obj['referUrl'] = referUrl
            obj['isChild'] = 'false' if not isChild else 'true'
            pass
        elif(stepType == Settings.piskelStep):
            obj['type'] = stepType
            obj['title'] = title
            obj['description'] = description
            obj['isChild'] = 'false' if not isChild else 'true'
            # obj['referUrl'] = referUrl
            pass
        else:
            return 'Unknown type of step'
        self.json['lessons'].append(obj)
        return True
        
    def saveLocalProject(self):
        
        path = os.path.join(self.projectPath,Settings.projectFileName)
        with open(path, 'w') as outfile:
            json.dump(self.json, outfile)
        
    def downLoadProjectsFromRemote(self):
        DownloadProject(self.__localPathForStudent,Settings.bucketName)
        pass

    def getDownLoadPath(self):
        return self.__localPathForStudent

    def uploadProjectsToRemote(self):
        UploadProject("",self.projectPath)
        pass

    def getUploadPath(self):
        return self.__localPathForTeacher

    def getProjectNameList(self):
        localpath = self.__localPathForStudent
        listPath = os.listdir(localpath)
        return listPath

class LocalProjectMgr(LocalProjectMgrVersion1):
    
    def __init__(self):
        super(LocalProjectMgr,self).__init__()
    
    def createProject(self,projectName=None,title='title',description='description',tags=None,referPixmap=None,anchorPixmap=None):
        result = super(LocalProjectMgr,self).createProject(projectName=projectName,title=title,description=description,tags=tags,referPixmap=referPixmap,anchorPixmap=anchorPixmap)
        return result






