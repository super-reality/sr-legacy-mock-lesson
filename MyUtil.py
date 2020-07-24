
import numpy as np
import cv2
from PyQt5 import QtGui
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QWidget,QFileDialog
from PyQt5.QtCore import QRect,QPoint
from PyQt5.QtGui import QIcon,QFont,QCursor,QPixmap,QPaintDevice,QPainter,QPen,QColor
from desktopmagic.screengrab_win32 import (
getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
getRectAsImage, getDisplaysAsImages)

from PIL.ImageQt import ImageQt
from Setting import Settings
import logging

import pytesseract as pyt
from PIL import Image
from pytesseract import Output
import os
import json
from collections import namedtuple

import threading
import boto3
from pygame import mixer 
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
   
def getDataFromBucket(bucketName=""):
    # return []
    bucketName = Settings.bucketName
    session = boto3.Session(
        aws_access_key_id = Settings.getSetting()['aws_access_key_id'],
        aws_secret_access_key= Settings.getSetting()['aws_secret_access_key'],
        region_name= Settings.region_name
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucketName)
    result = []
    for object in bucket.objects.filter(Prefix = ""):
        result.append(object.key)
    convertPathToObj(result)
    return result

def deleteByThread(path):
    th_delete = threading.Thread(target=deleteBucket,args=(path,),daemon=True)
    th_delete.start()
    pass
def deleteBucket(path):
    bucketName = Settings.bucketName
    session = boto3.Session(
        aws_access_key_id = Settings.getSetting()['aws_access_key_id'],
        aws_secret_access_key= Settings.getSetting()['aws_secret_access_key'],
        region_name= Settings.region_name
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucketName)
    bucket.objects.filter(Prefix=path).delete()

def path_to_dict_s3( pathDir , childList=[] ):
    
    pass

########################################## End ###############################################

def getPixmapFromScreen(posx,posy,W,H):
        """
        get screenshot with posx,posy,w,h and save it to local file 
        and return the created file name
        else return None
        """
        if(W == 0 or H == 0):
            return None
        
        imDisplay = getRectAsImage((posx,posy,posx+W,posy+H))
        qim = ImageQt(imDisplay)
        pix = QtGui.QPixmap.fromImage(qim)

        return pix.copy()

def convertCV2ImageToPixmap(cv2_img=None,parent=None):

    if(cv2_img is None or parent is None):
        return
    
    height, width, channel = cv2_img.shape
    bytesPerLine = channel * width

    cv2_img = np.require(cv2_img, np.uint8, 'C')

    qImg = QImage(cv2_img.data, width, height, bytesPerLine, QImage.Format_ARGB32)
    return qImg

def isImageUrl(url):

    url = str(url)
    if( 'jpg' in url):
        return True
    if( 'JPG' in url):
        return True
    if( 'jpeg' in url):
        return True
    if( 'JPEG' in url):
        return True
    if( 'png' in url):
        return True
    if( 'PNG' in url):
        return True
    if( 'bmp' in url):
        return True
    if( 'BMP' in url):
        return True
    
    return False

# Resizes a image and maintains aspect ratio
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

#this function matches the template by resizing template from 0.7x to 1.3x of the original size to cater different screen sizes..
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
    R = 1

    scales = np.linspace(0.5, 1.9, 25)[::-1]
    scales = np.insert(scales, 0, 1.0, axis=0)

    for scale in scales:
        # Resize image to scale and keep track of ratio
        resized = maintain_aspect_ratio_resize(template, width=int(template.shape[1] * scale))
        r = template.shape[1] / float(resized.shape[1])

        match = cv2.matchTemplate(gray_image, resized, cv2.TM_CCOEFF_NORMED)
        threshold = Settings.getSetting()['tolerance']
        logging.info("threshold value is: %s, and scale value is : %s",threshold, scale)
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

def convertPixmapToGray(pixmap=None,isgray=True):
    if(pixmap is not None):
        image = pixmap.toImage()
        _width = image.width()
        _height = image.height()
        channels_count = 4
        s = image.bits().asstring(_width * _height * channels_count)
        gray = np.fromstring(s, dtype=np.uint8).reshape((_height, _width, channels_count)) 
        if(isgray == True):
            gray = convertImageToGray(gray)
        # cv2.imshow("ttest",test)
        # cv2.waitKey(0)
        return gray
    else:
        pass

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

def openFileDlg(parent = None):
    
    """
    pls give parent to open dlg 'ex:parent = self'
    """
    
    fname = QFileDialog.getOpenFileName(parent, 'Open file', 'c:\\', "Image files (*.jpg *.gif,*.bmp,*.tiff,*.png)")
    imagePath = fname[0]
    if(imagePath is not None and len(imagePath)):
        return imagePath

def drawRectToPixmap(self,x,y,w,h,pixmap=None):
    if(pixmap is None):
        return
    painter = QPainter(pixmap)
    pen = QPen(QColor(*Settings.childAnchorMarkLineColor))
    pen.setWidth(Settings.childAnchorMarkLineWidth)
    painter.setPen(pen)
    painter.drawRect(QRect(x,y,w,h))
    pass


####################### convert json file to object #############################

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())

def loadData(path=''):
    
    try:
        with open(path) as target:
            return json.load(target, object_hook=_json_object_hook)
    except:
        logging.exception(path +" loading error")
        return None

################################# End ###########################################

############################################ Text Match and Tesseract ###################################################

'''Set path to tessaract.ext '''
pyt.pytesseract.tesseract_cmd = os.path.join(os.getcwd(),"Tesseract-OCR","tesseract")

#this function reads the MEAN color value of the image
def find_clr(img):
    data = np.reshape(img, (-1, 3))
    # print(data.shape)
    data = np.float32(data)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(data, 1, None, criteria, 10, flags)

    # print(sum(centers[0])/(3))
    return (sum(centers[0]) / (3))


def get_marked_image(correct,image):

    rects = []
    if correct is None or image is None:
        return rects
    #reading the image..
    img = image.copy()
    
    #print("Clr: ", find_clr(img))
    '''
    if ( find_clr(img) > 125):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (t,thresh) = cv2.threshold(img,200,255,cv2.THRESH_BINARY)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (t, thresh) = cv2.threshold(img, 75, 255,cv2.THRESH_BINARY_INV)

    #img = thresh
    '''

    (h,w,c) = img.shape
        
    
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    string = pyt.image_to_string(image)

    print("Expected string: ",correct)
    print("Got string: ",string)

    data = pyt.image_to_boxes(image)

    #image_to_boxes returns data as a string which can be split using "\n" character.
    data = data.split("\n")
    #print(data)
    errors = 0

    #removing spaces from the correct string, as img_2_boxes doesnt return spaces, carrage return etc.

    #NOTE: This function is for only single line matching,.
    correct = correct.replace(" ","")
    #print(len(correct),len(data))

    '''LOOPING through the characters and maching them, if there is not a match, then draw a rectangle around it..'''
    

    if(len(correct) != len(data)):
        print("Please enter the string of same length.")
        return rects
    for i in range(len(correct)):

        if (correct[i] != data[i][0]):
            #print(data[i][0])
            coords = data[i].split(" ")
            #print(coords)
            x1 = int(coords[1])
            y1 = h-int(coords[2])
            x2 = int(coords[3])
            y2 = h-int(coords[4])
            #print((x1,y2,x2,y2))
            rect = QRect(QPoint(x1,x2),QPoint(x2,y2))
            rects.append(rect)
            
            # cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),1)
            errors +=1

    
    return rects


def getTextFromImage(cv2_img = None):

    if(cv2_img is None):
        return
    cv2_img = cv2.cvtColor(cv2_img,cv2.COLOR_BGR2GRAY)
    string = pyt.image_to_string(cv2_img)

    return string
    

#basic function to mark an image...
#get_marked_image(expected_string, path_to_image)

'''tHIS function is to only mark the values for:
    - 1 line input.
    - Exact same length of strings (expected and received), if not Same, we can ask the user to write the string of same length as expected.
    - Capitalization should be exact too.
    '''
############################################ End ###############################################




####################################Glow effect ###################################
from textwrap import wrap
import argparse
import array
import cairo
from PIL import ImageFilter, Image
import numpy as np

def transform_color(hex_color):
    try:
        color = [_/255.0 for _ in map(lambda x: int(x, 16), wrap(hex_color, 2))]
    except ValueError:
        raise Exception("Invalid color format: {}".format(hex_color))
    if len(color) != 3:
        raise Exception("Invalid color format: {}".format(hex_color))
    return color


class NeonGlowText:
    """Neon glow text"""
    
    MIN_FONT_SIZE = 20
    MAX_FONT_SIZE = 300
    MAX_PADDING   = 120
    MIN_SHADOW    = 20
    FONT          = "Zapfino"

    BG_COLOR   = '000000'
    GLOW_COLOR = '0096ff' #(0.929, 0.055, 0.467)
    FG_COLOR_1 = 'ff31f4' #(1, 0.196, 0.957)
    FG_COLOR_2 = 'ffd796' #(1, 0.847, 0.592)
    FILL_COLOR = 'FFFFFF'

    def __init__(self, args_dict):
        self.text           = 'acer'
        self.filename       = '1.png'
        self.width          = 100
        self.height         = 100
        self.font           = self.FONT
        self.font_size      = self.MIN_FONT_SIZE
        self.bg_color       = self.BG_COLOR
        self.glow_color     = self.GLOW_COLOR
        self.fill_color     = self.FILL_COLOR
        self.stroke_1_color = self.FG_COLOR_1
        self.stroke_2_color = self.FG_COLOR_2
        self.commonStrokeWidth = 5


        if(self.font_size is None):
            self.font_size = self.MIN_FONT_SIZE
    
    def draw(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        
        cr = cairo.Context(surface)
        
        self._set_font(cr)
        self._move_to_center(cr)
        
        self._paint_bg(cr)

        cr.text_path(self.text)
        
        self._draw_glow(cr)
        
        surface = self._blur(surface, 35)
        
        cr = cairo.Context(surface)
        
        self._set_font(cr)
        self._move_to_center(cr)
        
        cr.text_path(self.text)
        self._draw_neon(cr)
        
        surface.write_to_png(self.filename)
    
    def _set_font(self, cr):
        cr.select_font_face(self.font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

        if self.font_size:
            cr.set_font_size(self.font_size)
            return

        # Let's find an appropriate font size...
        f_size = self.MAX_FONT_SIZE
        
        while True:
            cr.set_font_size(f_size)
            _, _, t_width, t_height, _, _ = cr.text_extents(self.text)
            
            # Check if text is within the desired boundaries
            if not (t_width > self.width - min(self.MAX_PADDING, f_size) or
                t_height > self.height - min(self.MAX_PADDING, f_size)) \
                or f_size <= self.MIN_FONT_SIZE:
                    break
                    
            f_size -= 2
        
        self.font_size = f_size

    def _move_to_center(self, cr):
        cr.select_font_face(self.font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(self.font_size)
        x_bearing, y_bearing, t_width, t_height, _, _ = cr.text_extents(self.text)
        
        x = self.width / 2 - (t_width / 2 + x_bearing)
        y = self.height / 2 - (t_height / 2 + y_bearing)

        cr.move_to(x, y)

    def _paint_bg(self, cr):
        cr.set_source_rgb(*transform_color(self.bg_color))
        cr.paint()
        
    def _draw_glow(self, cr):
        if(self.font_size is None):
            self.font_size = self.MAX_FONT_SIZE
        stroke_width = max(self.font_size / 3, self.MIN_SHADOW)
        self._draw_stroke(cr, self.glow_color, stroke_width)
        self._fill(cr, self.fill_color)

    def _draw_stroke(self, cr, rgb, stroke_width):
        cr.set_source_rgb(*transform_color(rgb))
        cr.set_line_width(stroke_width)
        cr.stroke_preserve()
        
    def _fill(self, cr, rgb):
        cr.set_source_rgb(*transform_color(rgb))
        cr.fill()

    def _draw_neon(self, cr):
        self._draw_stroke(cr, self.stroke_1_color, 10 if self.font_size > 100 else 5)
        self._draw_stroke(cr, self.stroke_2_color, 5 if self.font_size > 100 else 2)
        self._fill(cr, self.fill_color)
        
    def _blur(self, surface, blur_amount,width=None,height=None):
        # Load as PIL Image
        bg_image = Image.frombuffer("RGBA",( surface.get_width(), surface.get_height() ), surface.get_data(), "raw", "RGBA", 0, 1)
        
        # Apply blur
        blurred_image = bg_image.filter(ImageFilter.GaussianBlur(blur_amount))
        
        # Restore cairo surface
        image_bytes = blurred_image.tobytes()
        image_array = array.array('B', image_bytes)
        if(width is None):
            stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_ARGB32, self.width)
            return surface.create_for_data(image_array, cairo.FORMAT_ARGB32, self.width, self.height, stride)
        else:
            stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_ARGB32, width)
            return surface.create_for_data(image_array, cairo.FORMAT_ARGB32, width, height, stride)

    def drawRect(self,width,height):

        if width<1 or height<1:
            return None
        
        stroke_width = 25
        bounus = 40
        child_width = width
        child_height = height
        parent_width = width + bounus
        parent_height = height + bounus
        canvas_width = parent_width
        canvas_height = parent_height
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,canvas_width,canvas_height)
        cr = cairo.Context(surface)
        # cr.rectangle(canvas_width//2 - parent_width//2, canvas_height//2 - parent_height//2,parent_width,parent_height)
        cr.rectangle(canvas_width//2-child_width//2,canvas_height//2-child_height//2,child_width,child_height)

        
        ######### drawing and blur
        cr.set_source_rgb(*transform_color(self.glow_color))
        cr.set_line_width(stroke_width)
        cr.stroke_preserve()
        surface = self._blur(surface, stroke_width/2 ,width=canvas_width,height=canvas_height)
        ######## end of drawing and blur

        data = surface.get_data()
        array = np.ndarray(shape=(canvas_height,canvas_width,4),dtype=np.uint8,buffer=data)
        posx = canvas_width//2 - child_width//2 
        posy = canvas_height//2 - child_height//2
        array[posy:posy+child_height,posx:posx + child_width] = [0,0,0,0]
        return array


#################### end #########################


###################TTS#########################
from google.cloud import texttospeech as tts
import os
import playsound
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="game-gen.json"
from google.cloud import texttospeech
import io
def playAudioFromText(Text=""):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=Text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code=Settings.getSetting()['language-tts'],
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,name=Settings.getSetting()['name-tts'])

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,speaking_rate=Settings.getSetting()['speaking_rate-tts'])

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(input=synthesis_input,voice=voice,audio_config=audio_config)
    # The response's audio_content is binary.
    mem_file = io.BytesIO(response.audio_content)
    mem_file.seek(0)
    mixer.init()
    mixer.music.load(mem_file)
    mixer.music.play(0)
    while mixer.music.get_busy():
        pass
    mem_file.close()
