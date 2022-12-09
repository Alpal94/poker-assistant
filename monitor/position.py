import numpy as np
import time
import cv2 as cv
import pytesseract


def findPlayerPosition(img, playerID):
    button = findDealerButton(img)
    getPlayerPositionCoordinates(img, getPlayerColour(playerID))


def getPlayerPositionCoordinates(img, rbg):
    isolated = cv.inRange(img, rbg, rbg)
    edges = cv.Canny(isolated,50,100)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        approx = cv.approxPolyDP(contour, epsilon=1, closed=True)
        area = cv.contourArea(approx)
        if area > 150 and area < 300:
            m = cv.moments(approx)
            cx = int(m['m10']/m['m00'])
            cy = int(m['m01']/m['m00'])
            return [cx, cy, 7]
    return None



def findDealerButton(img):
    grey = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    circles = cv.HoughCircles(grey,cv.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=3,maxRadius=8)
    circles = np.uint16(np.around(circles))
    custom_config = r'--oem 3 --psm 6'
    for i in circles[0,:]:
        x1 = i[0] - i[2]
        x2 = i[0] + i[2]
        y1 = i[1] - i[2]
        y2 = i[1] + i[2]
        cropped = img[y1:y2,x1:x2]
        dealerID = pytesseract.image_to_string(cropped, config=custom_config).strip()
        if dealerID == 'D':
            print("Found dealer")
            return i
    return None

def getPlayerColour(playerID):
    playerIDColours = [
            (0,0,0),
            (132,94,194),
            (255,83,91),
            (43,105,104),
            (189,67,48),
            (255,151,52),
            (0,0,0),
            (0,137,202),
            (248,190,13),
    ]
    return playerIDColours[playerID - 1]
