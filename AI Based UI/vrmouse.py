
import cv2
import numpy as np
import handtracker as htm
import time
import pyautogui as autopy
wCam, hCam = 640, 480
frameR = 100
smoothening = 1.5
pTime = 0
plocX, plocY= 0, 0
clocX, clocY = 0, 0,
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.size()
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[6][1:]
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(255, 0, 255), 2)
        if fingers[1] == 1 and fingers[2]==0:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            autopy.moveTo(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        if fingers[1] == 1 and fingers[2]==1 :
            length1, img1, lineInfo1 = detector.findDistance(8, 6, img)
            print(length1)
            length2, img2, lineInfo2 = detector.findDistance(12, 10, img)
            print(length2)
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)
            if length1<20 and length>30:
                cv2.circle(img1, (lineInfo1[4], lineInfo1[5]),15, (0, 255, 0), cv2.FILLED)
                autopy.leftClick()
            if length2<20 and length>30:
                cv2.circle(img2, (lineInfo2[4], lineInfo2[5]),15, (0, 255, 0), cv2.FILLED)
                autopy.rightClick()
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

