import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np


width, height = 680, 400
folderPath = "presentation"
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
pathImages = sorted(os.listdir(folderPath), key=len)


imgNumber = 1
hs, ws = int(140*1), int(230*1)
gestureThreshold = 250
buttonPressed = False
buttonCounter = 0
buttonDelay = 10
annotations = [[]]
annotationNumber = 0
annotationStart = False
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)
    hands, img = detector.findHands(img)
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']
        xVal = int(np.interp(lmList[8][0], [width//2, w],[0,width]))
        yVal = int(np.interp(lmList[8][1], [150,height-150], [0, height]))
        indexFingers = xVal, yVal

        if cy <= gestureThreshold:
            annotationStart = False

            # Gesture-1 Left
            if fingers == [1,0,0,0,0]:
                annotationStart = False
                print("Left")
                if imgNumber > 0:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    imgNumber -= 1
            # Gesture-2 Right
            if fingers == [0,0,0,0,1]:
                annotationStart = False
                print("Right")
                if imgNumber < len(pathImages)-1:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    imgNumber += 1

        # Gesture-3 Show Pointer
        if fingers == [0,1,1,0,0]:
            cv2.circle(imgCurrent,indexFingers,8,(0,0,255),cv2.FILLED)
            annotationStart = False

        # Gesture-4 Draw
        if fingers == [0,1,0,0,0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            cv2.circle(imgCurrent,indexFingers,7,(0,0,210),cv2.FILLED)
            annotations[annotationNumber].append(indexFingers)
        else:
            annotationStart = False

        # Gesture-5 Erase
        if fingers == [0,1,1,1,0]:
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                buttonPressed = True
    else:
        annotationStart = False

    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range (len(annotations)):
        for j in range (len(annotations[i])):
            if j != 0:
                cv2.line(imgCurrent, annotations[i][j-1],annotations[i][j],(0,0,200),8)

    imgSmall = cv2.resize(img,(ws, hs))
    h,w,_ = imgCurrent.shape
    imgCurrent[0:hs,w-ws:w] = imgSmall
    cv2.imshow("Image", img)
    cv2.imshow("Slides", imgCurrent)
    key= cv2.waitKey(1)
    if key == ord('q'):
        break