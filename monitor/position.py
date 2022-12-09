import numpy as np
import time
import cv2 as cv
import pytesseract


def findPlayerPosition(img, playerID):
    button = findDealerButton(img)

    if button is None:
        raise Exception("Button not found")

    activePlayers = []
    for playerX in range(1, 10):
        playerPosition = getPlayerPositionCoordinates(img, getPlayerColour(playerX))
        if playerPosition is not None:
            dist = pow(pow(playerPosition[0] - button[0], 2) + pow(playerPosition[1] - button[1], 2), 0.5)
            activePlayers.append({"player": playerX, "dist":dist})
    print(activePlayers)


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

    edges = cv.Canny(grey,50,100)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        approx = cv.approxPolyDP(contour, epsilon=1, closed=True)
        area = cv.contourArea(approx)
        if area > 150 and area < 220:
            m = cv.moments(approx)
            cx = int(m['m10']/m['m00'])
            cy = int(m['m01']/m['m00'])
            cv.circle(img, (cx,cy), 7, (255, 0, 0), 2)
            return [cx, cy, 7]

    cv.imshow('circle', img)
    cv.waitKey(0)
    return None

def getPlayerColour(playerID):
    playerIDColours = [
            (0,201,183),
            (132,94,194),
            (255,83,91),
            (43,105,104),
            (189,67,48),
            (255,146,42),
            (255,136,151),
            (0,137,202),
            (248,190,13),
    ]
    return playerIDColours[playerID - 1]
