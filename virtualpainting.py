import cv2
import numpy as np
import os
import pylab as p
import HandTrackModel as hm

folderpath="Header"
pathlist=os.listdir(folderpath)
overlist=[]

thickness = 5
color=(0,0,0)
x,y=0,0
imcanves=p.zeros((720,1280,3),np.uint8)

for path in pathlist:
    image=cv2.imread(f'Header/{path}')
    overlist.append(image)

# print(pathlist)
header=overlist[4]
# print(header.shape[0],header.shape[1])

cam=cv2.VideoCapture(0)
cam.set(3, 1280)
cam.set(4, 720)


# cv2.imshow('Header Image',header)

detector=hm.HandDetector(detectionCon=0.8)
while True:
    ret,frame=cam.read()
    frame=cv2.flip(frame,flipCode=1)

    #helps to detect the hand
    img=detector.FindHands(frame)
    list=detector.FindPosition(img,draw=False)
    if len(list)>0:
        # print(list)
        x1,y1=list[8][1:]#middel finger landmark is 8 for last 2 numbers
        x2,y2=list[12][1:]# index fringer only the last valu x,y not the idnumber

        #checking the finger is open or close
        finger= detector.tipfinding()
        # print(finger)
        if finger[1] and finger[2]:
            cv2.rectangle(img,(x1,y1-30),(x2,y2+30),(255,255,25),cv2.FILLED)
            # print("this is selection")
            if y1 < 170:
                if 170<x1<420:
                    color=(0,0,255,5)
                    thickness = 10
                    header=overlist[1]
                    # print("red")

                if 500<x1<683:
                    color = (255, 0, 0,5)
                    thickness = 10
                    header=overlist[3]
                    # print("blue")

                if  750< x1 < 940:
                    color = (0,255,0,5)
                    thickness = 10
                    header=overlist[2]
                    # print("green")

                if 1010< x1 <1240:
                    color=(0,0,0)
                    thickness=50
                    # print("errszor")

        if finger[1] and finger[2] == False:
            cv2.circle(img, (x1, y1 - 15), 20, color, cv2.FILLED)
            # print("draw it")
            if x==0 and y==0:
                x,y=x1,y1
            cv2.line(imcanves, (x,y), (x1,y1), color,thickness)
            x,y=x1,y1

    # frame[0:125,0:1280]=headerq
    frame[0:header.shape[0], 0:header.shape[1]] = header

    gray_frame = cv2.cvtColor(imcanves, cv2.COLOR_BGR2GRAY)
    _, inv_frame = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY_INV)
    inv_frame = cv2.cvtColor(inv_frame, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame,inv_frame)
    frame = cv2.bitwise_or(frame,imcanves)

    cv2.imshow('frame',frame)
    # cv2.imshow('canves',imcanves)
    key=cv2.waitKey(1)

    if key==ord('q'):
        cam.release()
        cv2.destroyAllWindows()
        break




