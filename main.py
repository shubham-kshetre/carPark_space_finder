 
import cv2 as cv
import cvzone
import numpy as np
import pickle

#1 display parking area video
#2 video is ending after finish create loop so that video can play again and again
#3 crop all the images according to rectangles (later we have to crop dilated image)
#4 convert image to grayscale and do gaussian blur
#5 use adaptive threshold

cap = cv.VideoCapture('carPark.mp4')
width, height = 107, 50

with open('carParkPositions','rb') as f:
    positionList = pickle.load(f)

def checkParkingSpace(imgDilated):
    for pos in positionList:
        x,y = pos
         
        imgCrop = imgDilated[y:y+height, x:x+width]
        # cv.imshow(str(x+y),imgCrop)
        count = cv.countNonZero(imgCrop) #zero is non light and 255 is most light 
        # cv.putText(img,str(count),(x,y+height-10), cv.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv.LINE_AA)
        cvzone.putTextRect(img,str(count),(x,y+height-10), scale= 1, offset=0, thickness=1)
        if count < 800:
            colour = (0,255,0)
            thickness = 5
        else:
            colour = (0,0,255)
            thickness = 2
        cv.rectangle(img,pos,(pos[0]+width, pos[1]+height),colour,thickness)  

while True:

    #2 to loop the video file
    if cap.get(cv.CAP_PROP_POS_FRAMES) == cap.get(cv.CAP_PROP_FRAME_COUNT):
            cap.set(cv.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()


    #BGR to gray image
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray,(3,3),2)
    imgThreshold = cv.adaptiveThreshold(imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv.THRESH_BINARY_INV,25,16) #image will only black and white
    #for more blur, so that dots in empty will less
    imgMedian = cv.medianBlur(imgThreshold,5)
    # To get more thick borders use dilate image
    kernel = np.ones((3,3), np.uint8)
    imgDilate = cv.dilate(imgMedian, kernel, iterations=1)


    checkParkingSpace(imgDilate)
    # for pos in positionList:




    cv.imshow('Threshold after median blur video', imgMedian)
    # cv.imshow('Threshold video', imgThreshold)
    # cv.imshow('Blur and Gray video', imgBlur)
    cv.imshow('video', img)
    cv.waitKey(5)








