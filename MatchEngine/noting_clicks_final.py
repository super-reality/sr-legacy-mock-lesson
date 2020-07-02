#this is a demo program for noting down clicks.... (button clicks) (NOT in the drawing CANVAS)



import cv2
import time
from pynput.mouse import Listener
import keyboard
import numpy as np
from desktopmagic.screengrab_win32 import (
getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
getRectAsImage, getDisplaysAsImages)

#Instead of just cropping out the clicked area, I am cropping an area defined by square_w and square_h as follows:

square_w = 150
square_h = 150

# square_w = 100
# square_h = 75

#Writing a text file to save the clicks_templates names and the location of the click IN the template...
file = open("templates\\clicks.txt","w+")


print("Starting....")

#counter for clicks...
clicks = 0

#two seconds sleep, so you should open may be Paint window during this and then start clicking....
time.sleep(2)

print("Start....")






clicked = False


#taking screenshot of the current window and converting to OpenCV image.

entireScreen = getScreenAsImage()
# entireScreen = getRectAsImage((-50,-50,100,100))
image = np.array(entireScreen)
image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
# cv2.imshow("iamge",image)
# cv2.waitKey(0)
# exit(0)


#this function checks whether the area we are trying to crop out is fully inside the screenshot or NOT..
def in_limits(image,x,y,square_w,square_h):

    (imageh,imagew,imagec) = image.shape

    print(imagew,imageh)

    if ( (x- square_w/2) >= 0 and (x+square_w/2) <= imagew and (y - square_h/2) >= 0 and (y+square_h/2) <= imageh):
        return True
    else:
        return False


#this function will give a valid cropped box, for example:

'''
lets say the screen is 500x500,
user clicks on location, (10,100)
now if we crop area of (100 , 75) while keeping the click pt at the center,
then we see that the box will go out of the left side of the screen.

So in such this function will return a valid box, which will start from x = 0,and then will return the coordinates of the
click point W.R.T. this new valid box... 
'''

def get_my_valid_box(iamge,x,y,square_w,square_h):

    (imageh, imagew, __) = image.shape
    if(imageh == 0 or imagew == 0):
        return None

    x1 = x - int(square_w/2)
    y1 = y - int(square_h/2)
    x2 = x + int(square_w/2)
    y2 = y + int(square_h/2)

    posx = square_w//2
    posy = square_h//2

    if(x1<0):
        posx = x
        x1 = 0
        x2 = x1 + square_w
    if( x2> imagew):
        posx = square_w - (imagew-x)
        x2 = imagew
        x1 = imagew - square_w
    if(y1<0):
        posy = y
        y1 = 0
        y2 = y1 + square_h
    if(y2>imageh):
        posy = square_h - (imageh-y)
        y2 = imageh
        y1 = y2 - square_h


    return (x1,y1,x2,y2,posx,posy)

def get_valid_box(image,x,y,square_w,square_h):

    x1 = x - int(square_w/2)
    y1 = y - int(square_h/2)
    x2 = x + int(square_w/2)
    y2 = y + int(square_h/2)

    coordx = x - x1
    coordy = y - y1

    (imageh, imagew, __) = image.shape

    if ( x - int(square_w/2) < 0):



        x1 = 0
        coordx = x


    if (x + int(square_w/2) > imagew):

        x2 = imagew


    if ( y - int(square_h/2 ) < 0):

        y1 = 0
        coordy = y

    if (y + int(square_h/2) > imageh):

        y2 = imageh


    #x1,y1,x2,y2 are the coordinates of the cropped box...
    #whhile coordx and coordy are the coordinates of the CLICK inside the box... (w.r.t origin of the box)
    return (x1,y1,x2,y2,coordx,coordy)







#this function is binded to the click button
def on_click(x, y, button, pressed):
    
    global file
    global clicks
    global clicked
    global image
    global square_h,square_w
    
    

    #if click pressed, then increment the counter.
    clicks += 1

    # variable for saving the template image. tempx,tempy are the coordinates of the click in the TEMPLATE.
    temp = None
    tempx = 0
    tempy = 0

    if (in_limits(image,x,y,square_w,square_h)):
        #if the cropped box is already in the limits... then.. crop the area from the maing image (screenshot)
        # and save it into temp variable.
        temp = image[ y-int(square_h/2):y+int(square_h/2) , x-int(square_w/2):x+int(square_w/2)  ]

        #location of click in the cropped area is simply the CENTER..
        tempx = int(square_w/2)
        tempy = int(square_h/2)

    else:
        #IF THE BOUNDING box was not fully inside the screenshot.
        #then get a valid box and (X,Y coords of the click pt w.r.t. cropped box)
        # (x1,y1,x2,y2,coordx,coordy) = get_valid_box(image,x,y,square_w,square_h)
        (x1,y1,x2,y2,coordx,coordy) = get_my_valid_box(image,x,y,square_w,square_h)
        temp = image[ y1:y2, x1:x2]
        tempx = coordx
        tempy = coordy

    #writing the click in the file as:
    # click_(click number).png,x_coord of the click in the template, y_coord of the click in the template
    line = "click_" + str(clicks) + ".png,"+str(tempx)+","+str(tempy)+"\n"
    file.write(line)

    #saving the template image in the same folder too.. (check consistent naming)
    
    cv2.imwrite("templates\\"+"click_" + str(clicks) + ".png",temp)


    clicked = True
    print ("Mouse clicked")

    #wait for 0.5 secs and take a screenshot again to update the image...
    time.sleep(0.5)

    time.sleep(0.5)




#main loop of the program...

with Listener(on_click=on_click) as listener:
    #listener.join()

    while(1):



        #press Q button to close the progam and save the values..
        if keyboard.is_pressed('q'):  # if key 'q' is pressed
            print('Closing the program..')

            file.close()
            break  # finishing the loop




