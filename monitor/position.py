import numpy as np
import time
import lib
import cv2 as cv
import pytesseract


def findPlayerPosition(img, playerID):
    button = findDealerButton(img)
    hero = {}

    if button is None:
        raise Exception("Button not found")

    activePlayers = []
    for playerX in range(1, 10):
        playerPosition = getPlayerPositionCoordinates(img, getPlayerColour(playerX))
        if playerPosition is not None:
            dist = int(pow(pow(playerPosition[0] - button[0], 2) + pow(playerPosition[1] - button[1], 2), 0.5))

            player = {"player": playerX, "dist":dist}
            activePlayers.append(player)
            if playerID == playerX:
                hero = player

    if hero is {}:
        return None

    activePlayers.sort(key=playerDistanceToButton, reverse=False)
    if abs(activePlayers[0]["dist"] - activePlayers[1]["dist"]) < 50:
        if activePlayers[0]["player"] < activePlayers[1]["player"]:
            dealer = activePlayers[0]
        else:
            dealer = activePlayers[1]
    else:
        dealer = activePlayers[0]

    activePlayers.sort(key=getPlayerID, reverse=False)
    dealerIndex = activePlayers.index(dealer)
    heroIndex = activePlayers.index(hero)

    smallBlindIndex = (dealerIndex + 1) % len(activePlayers)
    bigBlindIndex = (dealerIndex + 2) % len(activePlayers)
    smallBlind = activePlayers[smallBlindIndex]
    bigBlind = activePlayers[bigBlindIndex]

    if hero == smallBlind:
        return lib.Position.SmallBlind
    elif hero == bigBlind:
        return lib.Position.BigBlind
    else:
        heroPosition = 9 - (dealerIndex - heroIndex) % len(activePlayers)
        return lib.Position(heroPosition)


def playerDistanceToButton(player):
    return player["dist"]
def getPlayerID(player):
    return player["player"]

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
    red = cv.inRange(img, (100,0,0), (255,0,0))

    hist = cv.equalizeHist(red)
    blur = cv.GaussianBlur(hist, (31,31), cv.BORDER_DEFAULT)

    circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, 1, 3, param1=14, param2=10, minRadius=5,maxRadius=9)

    #circles = cv.HoughCircles(grey,cv.HOUGH_GRADIENT,1,10,param1=50,param2=30,minRadius=3,maxRadius=11)
    circles = np.uint16(np.around(circles))
    custom_config = r'--oem 3 --psm 6'
    for i in circles[0,:]:
        x1 = i[0] - i[2]
        x2 = i[0] + i[2]
        y1 = i[1] - i[2]
        y2 = i[1] + i[2]
        cropped = img[y1:y2,x1:x2]
        cv.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        dealerID = pytesseract.image_to_string(cropped, config=custom_config).strip()
        print(dealerID)
        if(len(dealerID)) > 1:
            if dealerID[1] == 'D':
                print("Found dealer")
                return i
        if dealerID == 'D' or dealerID == 'D)' or dealerID == '(D' or dealerID == '(D)':
            print("Found dealer")
            return i
        if "D" in dealerID:
            print("Found dealer")
            return i
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
