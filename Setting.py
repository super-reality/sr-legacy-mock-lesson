import json
from collections import namedtuple
class Settings:

    #Strings
    lookStep = 'LookStep'
    clickStep = 'ClickStep'
    matchStep = 'MatchStep'
    mouseStep = 'MouseStep'
    attachStep = 'AttachStep'
    piskelStep = 'PiskelStep'
    scrollDown = 'Scroll Down'
    scrollUp = 'Scroll Up'
    rightClick = 'Right Click'
    leftClick = 'Left Click'
    titlePlaceholder = 'add title'
    descriptionPlaceholder = 'add description'
    

    tagsPlaceHolder = 'add tags'
    anchorText = 'SET ANCHOR'
    stepTitlePlaceHolder = 'add step name'
    stepDescriptionPlaceHolder = 'add step description'
    topleft = 'topleft'
    topright = 'topright'
    bottomleft = 'bottomleft'
    bottomright = 'bottomright'
    

    #Errors
    noTitleError = 1
    noTag = 2
    valid = 0
    noAnchor = 3

    lessonError = 1
    stepError = 2


    projectAlreadyExist = 10
    projectNameNotSpecified = 11
    commonOpacity = 0.2
    commonOpacityForStudent = 0.9
    childAnchorMarkLineColor = (255,0,0,255)
    childAnchorMarkLineWidth = 2

    projectFileManagementError = "Cant' delete original project directory"
    projectAlreadyExistErrorText = "Project Folder Already Exist, Will you replace it with new one?"
    projectStepCreationError = "Error occured in Step Creation"
    clickSportText = "Show Click Spot"
    imageMatchText = "Image Match"
    textMatchText = "Text Match"
    textMatchPlaceHolderText = "www.google.com"
    showTextBox = "show test box"
    selectProjectBeforeDownloadingError = "Please select project here before downloading"
    templateFolder = "Template"

    #params
    gotoLessson = 1
    gotoStep = 2
    
    #project
    projectFileName = "data.json"
    dropboxFolder = "D:/dropbox/DropboxApps"
    dropboxCache = "~/.dbdownload.cache"
    projectStudentPath = "ProjectsForStudent"
    projectTeacherPath = "ProjectsForTeacher"
    threshold = 0.9
    bias = 0
    prefixWidth = 2
    gripSize = 20
    commonMargin =10
    commonRowHeightChild = 40
    delta = 45
    refreshProjectsListMode = 1
    anchorDefaultWidth = 300
    anchorDefaultHeight = 200
    arrowwidgetCalibrate = 15
    shortKeyForCapture = 'ctrl+s'
    shortKeyForTruncluate = 'ctrl+d'
    shortKeyForNoTruncluate = 'ctrl+g'


    #dropbox
    # access_token = 'jen1g6kqkAAAAAAAAAAATH8b-4NGTrbgjJ2rK_6UiXqSGUNcYCLgL6kdCbGGNrVR'
    access_token = 'jen1g6kqkAAAAAAAAAAAZoeGMDPQCZVHSIpKGCWP8qdnMTBs7qoWhMN_ZEGpPatX'
    
    region_name=None
    bucketName = 'openverse-lms'


    

    def __init__(self):
       with open('setting.env') as f:
           self.data = json.load(f)
    @staticmethod
    def getSetting():
        with open('setting.env') as f:
           return json.load(f)
    @staticmethod
    def getImagePaths():
        return {'upload':'icons/camera.png','float':'icons/eye.png'}

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
