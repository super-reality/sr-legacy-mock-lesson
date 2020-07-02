import tkinter as tk
from tkinter import *
import random
import time
import cv2
from pynput.mouse import Listener
import numpy as np
import pyautogui
from tkinter import messagebox

# this module creates templates for 'matching' for example we draw a circle and then want the student to do the same
#then we could give some feedback to the student...

#variable for matchin score 0-100

score = 0


# XY coordinates of the 'anchor image'
# anchor image is a piece of windows screen which doesnt change that much.

#teacher would specify this,,


X_orig = 0
Y_orig = 0
anchor_found = False



#this function matches the features in two given images.
def kaze_match(im1, im2):
    # load the image and convert it to grayscale

    #cv2.imshow("im1",im1)
    #cv2.imshow("im2",im2)
    #cv2.waitKey(0)

  try:
    gray1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    # initialize the AKAZE descriptor, then detect keypoints and extract
    # local invariant descriptors from the image
    detector = cv2.AKAZE_create()
    (kps1, descs1) = detector.detectAndCompute(gray1, None)
    (kps2, descs2) = detector.detectAndCompute(gray2, None)

    #print("keypoints: {}, descriptors: {}".format(len(kps1), descs1.shape))
    #print("keypoints: {}, descriptors: {}".format(len(kps2), descs2.shape))

    # Match the features
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(descs1, descs2, k=2)  # typo fixed

    # Apply ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.85 * n.distance:
            good.append([m])

    # cv2.drawMatchesKnn expects list of lists ascv matches.
    im3 = cv2.drawMatchesKnn(im1, kps1, im2, kps2, good, None, flags=2)
    max = None
    if (len(kps1) > len(kps2)):
        max = len(kps1)
    elif (len(kps2) > len(kps1)):
        max = len(kps2)
    else:
        max = len(kps1)

    print("Matching: ", round(len(good) * 100 / max, 1), "%")
    # print(len(good))
    # cv2.imshow("AKAZE matching", im3)
    # cv2.waitKey(0)

    return round(len(good) * 100 / max, 1)

  except:
      return 0

#return\s the position of any Tkinter window
def get_position(window):
    geometry = window.geometry()
    geometry = window.geometry()
    print("Testig gemoetry: ", geometry)
    W = int(geometry.split("x")[0])
    H = int((geometry.split("x")[1]).split("+")[0])
    posx = int(geometry.split("+")[1])
    posy = int(geometry.split("+")[2])
    return (posx, posy, W, H)





def check_image():
    global score, template, root

    #these are offset values for croppig the match area

    #yoffset is 40 becuse tkinter window has a top bar of almost 40px height..
    xoff = 10
    yoff = 40
    marginx = 0
    marginy = 0

    #for testing the score
    #we locate the lcation and dimensions of the tkinter box on the screen.
    (testx, testy, testw, testh) = get_position(root)

    #adding the offset values...

    testx += xoff
    testy += yoff



    '''
    
    
    TAKING A SCREENSHOT....'''

    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)


    if (testw > 10 and testh > 10):

        #CROPPING THE AREA OF INTEREST.....
        cropped = screen[testy + marginy: testy + testh - marginy, testx + marginx: testx + testw - marginx]
        # red = (0,0,255)
        # cv2.imshow("Test image:",cropped)
        # cv2.rectangle(screen, (testx + marginx, testy + marginy), (testx +testw - marginx, testy + testh - marginy), red, 2)
        # cv2.imwrite("result.png",cropped)
        # cv2.imshow("Test:", cropped)

        # cv2.waitKey(0)

        #GETTING THE SCORE AND SETTING IT ON THE GUI
        score = kaze_match(template, cropped)

    score_label.set(str(score))

    #CHECKING the area again and again after each 500ms
    root.after(500, check_image)

#this function finds the ANCHOR image on the screen
def find_anchor():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    anchor = cv2.imread("match_template/anchor.png",0)
    print(image.shape,anchor.shape)
    (found,X,Y,W,H,R) = match_image(image,anchor)
    return (found,X,Y,W,H,R)




#main code

#reading the template ("the drawing which student needs to replicate")
template = cv2.imread("match_template/template.png")


#opening the saved txt file
file = open("match_template/match_info.txt", "r")
line = file.readlines()[0].strip()

# RELATIVE postion of the drawing box w.r.t X_orig,Y_orig (coordinates of the anchor image left upper corner)
X_ref = int(line.split(",")[1])
Y_ref = int(line.split(",")[2])

(h, w, c) = template.shape
w = w
h = h

#just a transparent image ...
area_icon = cv2.imread("area_box.png")
area_icon = cv2.resize(area_icon, (w, h))

cv2.imwrite("temp.png", area_icon)


#waiting for two seconds....
time.sleep(2)

print("Waiting..")


#waiting for the anchor
while(not anchor_found):

    (anchor_found,X,Y,W,H,R) = find_anchor()

    if(anchor_found):
        print("anchor found!")
        X_orig = X
        Y_orig = Y
        break
    else:
        #messagebox.showerror("Error", "Whoops! Couldnt find the image")
        print("NOT FOND")
        time.sleep(2)

#creating a tkinter window (in which the strudent will draw...
root = tk.Tk()
root.title("Area:")
root.attributes("-transparentcolor", "white")
# root.overrideredirect(1)

# position of the drawing box..
x = X_ref + X_orig
y = Y_ref + Y_orig - 40

#x = x - 70
#y = y - 113 - 32


root.geometry('%dx%d+%d+%d' % (w, h, x, y))
print("Geometry: ", '%dx%d+%d+%d' % (w, h, x, y))
CANVAS = tk.Canvas(root, width=w, height=h)
CANVAS.pack()

img = PhotoImage(file="temp.png")
print(img)
CANVAS.create_image(int(w / 2), int(h / 2), anchor=CENTER, image=img)

root.call('wm', 'attributes', '.', '-topmost', '1')


#creating second window to show the template (target drawing)

second_win = tk.Toplevel(root)
second_win.title("Template:")
second_win.attributes('-topmost', 'true')
canvas2 = tk.Canvas(second_win, width=w, height=h)
canvas2.pack()

img_temp = PhotoImage(file="match_template/template.png")

canvas2.create_image(int(w / 2), int(h / 2), anchor=CENTER, image=img_temp)

#variable for showing score..
score_label = tk.StringVar()
score_label.set(str(score))

#3rd window which shows the resulting score...
third_win = tk.Toplevel(root)
third_win.title("Result:")
third_win.geometry('%dx%d+%d+%d' % (250, 200, 600, 300))
label = Label(third_win, text="Score: ")
label.grid(row=0, column=0, padx=20, pady=20)

score_value = Label(third_win, textvariable=score_label)
score_value.grid(row=0, column=1)
third_win.attributes('-topmost', 'true')

check_image()
root.mainloop()