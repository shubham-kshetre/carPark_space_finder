import cv2 as cv
import pickle

#1 get the parking area image and display it.
#2 draw rectangle on it
#3 adjust the reactangle width and height according to parking space
#4 write variables for width and height
#5 do something so that on left click of mouse, rectangle will form and on right click rectangle, will delete
#6 on left click store the position of rectangle in list
#7 open that list using file handling
#8 open carparkPosition file in wb mode, so that we can write and save positions of rectangle. saved positions we can use in our main program

# img = cv.imread("carParkImg.png")
width, height = 107, 50


try: #try to find file load positions in it to positionList variabel
    with open('carParkPositions','rb') as f:
        positionList = pickle.load(f) #whatever in the file f put it in positionList
except: #else create new list
    positionList = []


def onMouseClick(event, x, y,flags, params):
    if event == cv.EVENT_LBUTTONDOWN:#to add position in list
        positionList.append((x,y))

    if event == cv.EVENT_RBUTTONDOWN:  #to delete position from list
        for i, pos in enumerate(positionList): 
            x1, y1 = pos
            if x1 < x < x1+width and y1 < y < y1+height:                  
                positionList.pop(i)

    with open('carParkPositions','wb') as f:
        pickle.dump(positionList,f)


while True:
    img = cv.imread("carParkImg.png")   
    for pos in positionList:
        cv.rectangle(img,pos,(pos[0]+width, pos[1]+height),(0,0,255),2)   
    cv.imshow("Parking", img)
    cv.setMouseCallback("Parking",onMouseClick)
    cv.waitKey(1)