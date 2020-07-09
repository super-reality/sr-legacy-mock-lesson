
import numpy as np
import cv2
from PyQt5 import QtGui
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QWidget,QFileDialog
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon,QFont,QCursor,QPixmap,QPaintDevice,QPainter,QPen,QColor
from desktopmagic.screengrab_win32 import (
getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
getRectAsImage, getDisplaysAsImages)

from PIL.ImageQt import ImageQt
from Setting import Settings

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
     
#just a resizing function to resize the template image while checking..
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
    return image

def loadImageFromUrl(url):
    img = cv2.imread(url,0)
    return img

def convertPixmapToGray(pixmap=None):
    if(pixmap is not None):
        image = pixmap.toImage()
        _width = image.width()
        _height = image.height()
        channels_count = 4
        s = image.bits().asstring(_width * _height * channels_count)
        gray = np.fromstring(s, dtype=np.uint8).reshape((_height, _width, channels_count)) 
        gray = convertImageToGray(gray)
        # cv2.imshow("ttest",test)
        # cv2.waitKey(0)
        return gray
        pass
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