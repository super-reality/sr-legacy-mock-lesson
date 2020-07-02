import tkinter as tk
from tkinter import *
import random
import time
import numpy as np
import keyboard
from pynput.mouse import Listener
import  pyautogui
import cv2



#this demo code saves a template which student needs to replicate...

#NOTE: here I am only taking a screenshot ONCE, when the program starts, so if the teacher wants to makes any updates to the drawing area,
#after opening the option, then you would need to take screenshots again and again after any specified time...


#First the teacher would select and 'anchor image; (a fixed part of the screen) so we can have a reference....

#starting dimension of the boxes
w= 450
h = 200
x = 500
y = 200



#variables to see the progress of the program...
close1 = False
close2 = False


x1=0
y1 = 0

#two windows variables..
root = None
anch = None
X = 0
Y = 0
drawing_pt = False
image = None

posx=0
posy=0
H=0
W=0



#this function creates an anchor window..... with a button...
#you can resize this transparent window over any area and then press the (DONE) button on top of it
#it will save the underlying area as an anchor iamge....

def create_anchor_window():
    global anch1
    anch1 = tk.Tk()

    # root.attributes("-transparentcolor", "white")
    # root.overrideredirect(1)
    anch1.title("Anchor image:")
    anch1.attributes('-alpha', 0.4)
    anch1.resizable(True, True)
    anch1.geometry('%dx%d+%d+%d' % (w, h, x, y))
    print(anch1.geometry())

    button = Button(anch1,text = "DONE",command = close_anchor_window)
    button.pack()
    # CANVAS = tk.Canvas(root, width=50, height=50)
    # CANVAS.pack()
    # img = PhotoImage(file="rectangle.png")

    # CANVAS.create_image(25,25, anchor=CENTER, image=img)

    anch1.call('wm', 'attributes', '.', '-topmost', '1')
    anch1.mainloop()

#this function runs when an anchor image is selected and pressed the button
def close_anchor_window():
    global X,Y,close1,anch1


    #saving the image as anchor.png
    anch1.update()
    geometry = anch1.geometry()


    #X,Y are the cordinates of the anchor image...
    W = int(geometry.split("x")[0])
    H = int((geometry.split("x")[1]).split("+")[0])
    X =int( geometry.split("+")[1])
    Y = int(geometry.split("+")[2])+35
    print("Geo string: ",geometry)
    print("Geometry of anchor:",X,Y,W,H)
    anchor = image[Y:Y + H, X:X + W]
    anch1.destroy()
    print("X,Y: ",X,Y)
    cv2.imshow("Anchor: ", anchor)
    cv2.waitKey(0)

    cv2.imwrite("match_template\\anchor.png", anchor)




    close1 = True
    print("Exiting....")



#this function creates the main template selection window...
def create_window():
    global root
    root = tk.Tk()

    # root.attributes("-transparentcolor", "white")
    # root.overrideredirect(1)
    root.title("Template area:")
    root.attributes('-alpha', 0.4)
    root.resizable(True, True)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    print(root.geometry())

    button = Button(root,text = "DONE",command = close_window)
    button.pack()
    # CANVAS = tk.Canvas(root, width=50, height=50)
    # CANVAS.pack()
    # img = PhotoImage(file="rectangle.png")

    # CANVAS.create_image(25,25, anchor=CENTER, image=img)

    root.call('wm', 'attributes', '.', '-topmost', '1')
    root.mainloop()


def close_window():
    global posx,posy,close2

    #when this is called....
    # the template image is shown in a window...
    file = open("match_template\\match_info.txt", "w+")
    geometry = root.geometry()
    W = int(geometry.split("x")[0])
    H = int((geometry.split("x")[1]).split("+")[0])
    posx =int( geometry.split("+")[1])
    posy = int(geometry.split("+")[2])+35
    print("Geometry:",posx,posy,W,H)
    template = image[posy:posy + H, posx:posx + W]
    root.destroy()
    cv2.imshow("Template: ", template)
    cv2.waitKey(0)

    #template image is saved.

    cv2.imwrite("match_template\\template.png", template)


    #coordinates of the template image W.R.T the anchor image's origin..
    posx = posx - X
    posy = posy - Y
    print("Relative Geometry:", posx, posy, W, H)

    #written in the file as : Match-box, (X,Y relative to anchor image;s position in the screen), width and height,...
    file.write("Match-box," + str(posx) + "," + str(posy) + "," + str(W) + "," + str(H) + "\n")

    file.close()
    close2 = True
    print("Exiting....")








#maing code..
#waitin for 2 secs to let the user switch to his screen.
time.sleep(2)


#taking a screen shot...
image = pyautogui.screenshot()
image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


#asking for anchor image.
create_anchor_window()
while(1):

        #once ANCHOr image is done and YOU PRESS 'M' afterwards,
        # a new window gets launched for setting the template area...

        if keyboard.is_pressed('m') and close1:  # Open match window..

            image = pyautogui.screenshot()
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            print('Opening window....')
            time.sleep(0.5)
            create_window()


        if close2:
            #finishing the program.
            print("program ended.s")
            break

