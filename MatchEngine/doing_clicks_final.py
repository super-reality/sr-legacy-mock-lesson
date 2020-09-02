#this program will guide the user to click on the given points..

import tkinter as tk
from tkinter import *
import random
import time
import cv2
import time
import numpy as np
import pyautogui
from pynput.mouse import Listener
from tkinter import messagebox


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
def match_image(gray_image,template):
    (tH, tW) = template.shape[::-1]  # get the width and height
    # match the template using cv2.matchTemplate
    match = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.80
    position = np.where(match >= threshold)  # get the location of template in the image
    found = 0
    X = 0
    Y = 0
    W = 0
    H = 0
    R = 1

    scales = np.linspace(0.7, 1.3, 15)[::-1]
    scales = np.insert(scales, 0, 1.0, axis=0)
    for scale in scales:

        # Resize image to scale and keep track of ratio
        resized = maintain_aspect_ratio_resize(template, width=int(template.shape[1] * scale))
        r = template.shape[1] / float(resized.shape[1])

        match = cv2.matchTemplate(gray_image, resized, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        position = np.where(match >= threshold)  # get the location of template in the image

        for point in zip(*position[::-1]):  # draw the rectangle around the matched template

            #cv2.rectangle(main_image, point, (int(point[0] + tW / r), int(point[1] + tH / r)), (0, 204, 153), 3)
            #cv2.imshow("FOUND something..", main_image)
            cv2.waitKey(0)
            found = 1
            (X,Y,W,H,R) = (int(point[0]),int(point[1]),int( tW / r),int(tH / r) , r)
            break

        if (found):
            break

    return (found,X,Y,W,H,R)

    #if returns ( template_found? , (X,Y,W,H of the area found), R resized template ratio...




#width and height of floating icon which will guide the click
w = 50
h = 50
x = 500
y = 200


#target locatins
targetx = 0
targety = 0


#a bool for detecting valid click
valid_click = False

x1=0
y1 = 0


#opening the file having clicks info
file = open("templates/clicks.txt","r")

lines = file.readlines()


#2 seconds sleep to allow the user to open paint window..
time.sleep(2)

#taking a screenshot
image = pyautogui.screenshot()
image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
#image = cv2.resize(image,(1920,1080))
#converting to gray iamage...
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)






def on_click(x, y, button, pressed):
    global targetx,targety,valid_click

    #when a click is recorded, check if it was in the guided area or not?


    if(abs(x-targetx) < 30 and abs(y-targety)<30):

        valid_click=True




#this function does all the JOB
def guided_clicks():
    global x1, y1, image, gray_image
    global targetx, targety, valid_click

    #reading all the lines...
    for i in range(len(lines)):


        line = lines[i].strip().split(",")
        print(line)
        #opening the tempalte image (into GRAYSCALE) by reading the name from the file
        template = cv2.imread("templates\\" + line[0], 0) #grey_scale template image.
        # cv2.imshow("Template:", template)

        x_coord = int(line[1])
        y_coord = int(line[2])
        #CHECK If the template is found on the screenshot or not...
        (found,X,Y,W,H,R) = match_image(gray_image,template)

        if ( found ):
            #cv2.rectangle(image, (X,Y), (X+W, Y+H), (0, 0, 255), 3)
            # cv2.imshow("search_image:", image)
            # cv2.waitKey(0)

            #if found,
            #coordinates of the click point in the GLOBAL screenshot...
            click_pt = ( X +int(x_coord /R), Y+ int(y_coord/R))


            #target point = click pt
            (targetx, targety) = click_pt

            # Using this: (x_icon, y_icon) = (click_pt[0] - width_of_floating_icon/2, click_pt[1] - height_of_floating_icon/2)
            (x_icon, y_icon) = (click_pt[0] - 25, click_pt[1] - 25)

            #moving the floating icon to the required location
            move_slowly(x_icon, y_icon)
            root.update()

            valid_click = False
            while (not valid_click):
                #wait till the user clicks inside the valid area
                continue
            valid_click = False

            #waiting for 0.3 secs and taking a screenshot again to update
            time.sleep(0.3)
            image = pyautogui.screenshot()
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


        else:

            # if template not found in the iamge...
            #show error box...
            messagebox.showerror("Error", "Whoops! Couldnt find the image")
            cv2.imshow("Template:", template)
            cv2.waitKey(0)
            return

    print("All done...")
    return



#this function moves the clicking ICON (floating icon to given location)

#rough implementation to create a movement animation
def move_slowly(x1,y1):
    global x, y
    #x1, y1 = (random.randrange(800)), (random.randrange(700))

    while (not (x1 == x and y1 == y)):

        if (abs(x1 - x) > 10):

            if (x1 > x):
                x += 10
            elif (x1 < x):
                x -= 10

        else:
            if (x1 > x):
                x += 1
            elif (x1 < x):
                x -= 1

        if (abs(y1 - y) > 10):

            if (y1 > y):
                y += 10
            else:
                y -= 10

        else:
            if (y1 > y):
                y += 1
            else:
                y -= 1

        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        root.update()
        time.sleep(0.03)



#creating a root window with transparent color///
root = tk.Tk()


#showing the floating icon in a transparent root window with NO upper bar.
root.attributes("-transparentcolor", "white")
root.overrideredirect(1)
# root.attributes('-alpha', 0.4)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

CANVAS = tk.Canvas(root, width=50, height=50)
CANVAS.pack()
img = PhotoImage(file="click_box.png")
CANVAS.create_image(25, 25, anchor=CENTER, image=img)

root.call('wm', 'attributes', '.', '-topmost', '1')


with Listener( on_click=on_click) as listener:
    guided_clicks()
    root.destroy()
    root.mainloop()
