
import numpy as np
import cv2
from PyQt5.QtGui import QImage
from desktopmagic.screengrab_win32 import (
getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
getRectAsImage, getDisplaysAsImages)

from PIL.ImageQt import ImageQt
from Setting import Settings
import logging
from PIL import Image
import os
import json
from collections import namedtuple

import threading
import random
import pandas as pd
#################### Get project Tree from current Teacher Lessson folder ##########################

def path_to_dict(pathDir,childList=[]):
    
    for path in os.listdir(pathDir):
        absPath = os.path.join(pathDir,path)
        if os.path.isdir(absPath):
            if isLeaf(absPath):
                childList.append(os.path.basename(path))
            else:
                obj = {}
                obj[os.path.basename(path)] = []
                childList.append(obj)
                path_to_dict(absPath,obj[os.path.basename(path)])
            pass
        else:
            pass
    
def isLeaf(path=None):
    if(path is None):
        return False
    path = os.path.join(path,Settings.projectFileName)
    if(os.path.exists(path)):
        return True
    else:
        return False

def getDataFromCurrentTeacherFolder():
    
    result = []
    path_to_dict( os.path.join(os.getcwd(),"ProjectsForTeacher") , result )
    return result

def convertPathToObj(paths):
    res = {}
    leafs = []
    isHaveObj = False
    for path in paths:
        items = str(path).split('\\')
        if len(items) == 2:
            leafs.append(items[0])
        elif len(items) > 2:
            len_t = len(items[0])
            res.setdefault(items[0],[]).append(path[len_t+1:])
            isHaveObj = True
            pass
        else:
            pass
    leafs = list(set(leafs))
    if(isHaveObj == False):
        paths.clear()
        paths.extend(leafs)
        return
    for key, value in res.items():
        leafs.append({key:value})
    
    paths.clear()
    paths.extend(leafs)
    
    for item in paths:
        if type(item).__name__ == 'dict':
            key = list(item.keys())[0]
            convertPathToObj(item[key])
            pass
        pass
    

    # convertPathToObj(res[key],leafs)
   
########################################## End ###############################################

########################## JSON RPC SERVER CODE ###############################

def makeImageFolder():
    if os.path.exists(os.path.join(os.getcwd(),"image")):
        pass
    else:
        os.mkdir("image")
    return "image"

def makeDownloadFolder():
    if os.path.exists(os.path.join(os.getcwd(),"DownLoad")):
        pass
    else:
        os.mkdir("DownLoad")
    if( os.path.exists(os.path.join(os.getcwd(),'files.csv'))):
        pass
    else:
        #create csv file
        files = pd.DataFrame([[0,1]],columns=['localpath','remotepath'])
        files.to_csv('files.csv')
    return "DownLoad"
    
def getFileNameTobeCreated():
    path = os.path.join(os.getcwd(),makeImageFolder())
    fileName = str(random.randint(1,10000)) + '.png'
    filePath = os.path.join(path,fileName)
    
    while(os.path.exists(filePath)):
        fileName = str(random.randint(1,10000)) + '.png'
        filePath = os.path.join(path,fileName)
    
    return filePath

def checkFileExistsFromUrl(imageUrl):

    files = pd.read_csv("files.csv")
    result = files[files['remotepath'] == imageUrl]
    
    if(result.empty):
        return ""
    else:
        for path in result['localpath'].values:
            if os.path.exists(path):
                return path
            else:
                pass
        return ""

def updateFilesCSV(imageUrl,filepath):
    files = pd.read_csv("files.csv")
    row = pd.DataFrame([[filepath,imageUrl]],columns=['localpath','remotepath'])
    files = files.append(row)
    files.to_csv("files.csv",index=None)
    pass

def getDownloadFileNameTobeCreated(imageUrl):
    #check if imageUrl exists in current folder
    filepath = checkFileExistsFromUrl(imageUrl)
    if(filepath == ""):
        pass
    else:
        return filepath
    path = os.path.join(os.getcwd(),makeDownloadFolder())
    fileName = str(random.randint(1,100000)) + '.png'
    filePath = os.path.join(path,fileName)
    
    while(os.path.exists(filePath)):
        fileName = str(random.randint(1,100000)) + '.png'
        filePath = os.path.join(path,fileName)
    

    f = open(filePath,'wb')
    f.write(requests.get(imageUrl).content)
    f.close()
    updateFilesCSV(imageUrl,filePath)
    return filePath

def delFileByName(fileName):
    path = makeImageFolder()
    filePath = os.path.join(path,fileName)
    if os.path.exists(filePath):
        os.remove(path)

def saveWindowRect(posx,posy,width,height,name):
    if(width <= 0 or height <= 0):
        return None
    if name == "":
        #create new file
        filename  = getFileNameTobeCreated()
        imDisplay = getRectAsImage((posx,posy,posx+width,posy+height))
        imDisplay.save(filename)
        return filename
    else:
        try:
            os.remove(name)
        except:
            pass
        filename  = getFileNameTobeCreated()
        imDisplay = getRectAsImage((posx,posy,posx+width,posy+height))
        imDisplay.save(filename)
        return filename
    pass

import requests

def findCVMatch(imageUrl,parentx,parenty,parentwidth,parentheight):
    #make download dir if not exist.
    makeDownloadFolder()
    fileName = getDownloadFileNameTobeCreated(imageUrl)
    print(fileName,"fileName")
    try:
        (found,X,Y,W,H,R) = match_image(fileName,parentx,parenty,parentwidth,parentheight)
    except:
        (found,X,Y,W,H,R) = (0,0,0,0,0,0)

    return (found,X,Y,H,W,R)

def maintain_aspect_ratio_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # Grab the image size and initialize dimensions
    dim = None
    (h, w) = image.shape[:2]

    # Return original image if no need to resize
    if width is None and height is None:
        return image

    # We are resizing height if width is none
    if width is None:
        # Calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # We are resizing width if height is none
    else:
        # Calculate the ratio of the 0idth and construct the dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # Return the resized image
    return cv2.resize(image, dim, interpolation=inter)

# #this function matches the template by resizing template from 0.7x to 1.3x of the original size to cater different screen sizes..
def match_image(url,parentx,parenty,parentwidth,parentheight):
    gray_image = getWholeScreen()
    template = loadImageFromUrl(url)
    (tH, tW) = template.shape[::-1]  # get the width and height
    # match the template using cv2.matchTemplate
    match = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    threshold = Settings.getSetting()['tolerance']
    
    position = np.where(match >= threshold)  # get the location of template in the image
    
    found = 0
    X = 0
    Y = 0
    W = 0
    H = 0
    R = 0

    scales = np.linspace(0.5, 1.9, 25)[::-1]
    scales = np.insert(scales, 0, 1.0, axis=0)
    for scale in scales:
        # Resize image to scale and keep track of ratio
        resized = maintain_aspect_ratio_resize(template, width=int(template.shape[1] * scale))
        r = template.shape[1] / float(resized.shape[1])

        match = cv2.matchTemplate(gray_image, resized, cv2.TM_CCOEFF_NORMED)
        threshold = Settings.getSetting()['tolerance']
        position = np.where(match >= threshold)  # get the location of template in the image

        for point in zip(*position[::-1]):  # draw the rectangle around the matched template
            found = 1
            (X,Y,W,H,R) = (int(point[0]),int(point[1]),int( tW / r),int(tH / r) , r)
            
            if X < parentx or X + W > parentx +parentwidth or Y < parenty or Y + H > parenty + parentheight:
                break
            else:
                (X,Y,W,H,R) = (0,0,0,0,0)
                found = 0
                continue
            break

        if (found):
            break

    return (found,X,Y,W,H,R)

    #if returns ( template_found? , (X,Y,W,H of the area found), R resized template ratio...

def convertImageToGray(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    return image

def loadImageFromUrl(url):
    img = cv2.imread(url,0)
    return img

# def addTwoCVImage(background,overlay):
#     foreground = overlay
#     gray_overaly = cv2.cvtColor(overlay.copy(),cv2.COLOR_BGR2GRAY)
#     alpha_background = background[:,:,3] / 255.0
#     alpha_background[:,:] = 0.99
#     max_val = np.max(gray_overaly)
#     alpha_foreground = (gray_overaly[:,:] / 255.0)*(gray_overaly[:,:] / 255.0)*(gray_overaly[:,:] / 255.0)*255*255*255/max_val/max_val/max_val
    
#     # set adjusted colors
#     for color in range(0, 3):
#         background[:,:,color] = alpha_foreground * foreground[:,:,color] + \
#             alpha_background * background[:,:,color] * (1 - alpha_foreground)
#     background[:,:,3] = (1 - (1 - alpha_foreground) * (1 - alpha_background)) * 255
#     return background

# def convertPixmapToGray(pixmap=None,isgray=True):
#     if(pixmap is not None):
#         image = pixmap.toImage()
#         _width = image.width()
#         _height = image.height()
#         channels_count = 4
#         s = image.bits().asstring(_width * _height * channels_count)
#         gray = np.fromstring(s, dtype=np.uint8).reshape((_height, _width, channels_count)) 
#         if(isgray == True):
#             gray = convertImageToGray(gray)
#         # cv2.imshow("ttest",test)
#         # cv2.waitKey(0)
#         return gray
#     else:
#         pass

def getWholeScreen(isgray=True):
    
    if(isgray):
        entireScreen = getScreenAsImage()
        image = np.array(entireScreen)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        return image
    else:
        entireScreen = getScreenAsImage()
        image = np.array(entireScreen)
        return convertImageToGray(image)

def getScreenSize():
    entireScreen = getScreenAsImage()
    image = np.array(entireScreen)
    return image.shape[0],image.shape[1]



# ###################TTS#########################
# from google.cloud import texttospeech as tts
# import os
# import playsound
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="game-gen.json"
# from google.cloud import texttospeech
# import io
# def playAudioFromText(Text="",):
    
#     # Instantiates a client
#     client = texttospeech.TextToSpeechClient()
    
#     # Set the text input to be synthesized
    
#     if '<speak>' in Text:
#         synthesis_input = texttospeech.SynthesisInput(ssml=Text)
#     else:
#         synthesis_input = texttospeech.SynthesisInput(text=Text)

#     # Build the voice request, select the language code ("en-US") and the ssml
#     # voice gender ("neutral")
#     voice = texttospeech.VoiceSelectionParams(
#         language_code=Settings.getSetting()['language-tts'],
#         ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,name=Settings.getSetting()['name-tts'])

#     # Select the type of audio file you want returned
#     audio_config = texttospeech.AudioConfig(
#         audio_encoding=texttospeech.AudioEncoding.MP3,speaking_rate=Settings.getSetting()['speaking_rate-tts'])

#     # Perform the text-to-speech request on the text input with the selected
#     # voice parameters and audio file type
#     response = client.synthesize_speech(input=synthesis_input,voice=voice,audio_config=audio_config)
#     # The response's audio_content is binary.
#     mem_file = io.BytesIO(response.audio_content)
#     mem_file.seek(0)
#     mixer.init()
#     mixer.music.load(mem_file)
#     mixer.music.play(0)
#     while mixer.music.get_busy():
#         pass
#     mem_file.close()
