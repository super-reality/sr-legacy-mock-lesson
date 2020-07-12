import pytesseract as pyt
from PIL import Image
import cv2
import numpy as np
from pytesseract import Output
import os

'''Set path to tessaract.ext '''
pyt.pytesseract.tesseract_cmd = os.path.join("D:\\upwork\\indian\\pyqt-floating","Tesseract-OCR\\tesseract")

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

    #reading the image..
    img = cv2.imread(image)
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
    string = pyt.image_to_string(Image.open(image))
    print("Expected: ",correct)
    print("Got: ",string)
    data = pyt.image_to_boxes(Image.open(image))

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
        return
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
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),1)
            errors +=1

    print(errors," Errors found.")

    cv2.imshow("Result:",img)
    cv2.waitKey(0)



#basic function to mark an image...
#get_marked_image(expected_string, path_to_image)

'''tHIS function is to only mark the values for:
    - 1 line input.
    - Exact same length of strings (expected and received), if not Same, we can ask the user to write the string of same length as expected.
    - Capitalization should be exact too.
    '''
get_marked_image("HELLO MY NAME Is SAADsss.","text_test2.png")
