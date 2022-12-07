import pyautogui
import time
import numpy as np
import pytesseract
from PIL import Image
import cv2 as cv
from matplotlib import pyplot as plt
from os.path import exists

def targetArea(img, monitorNo, quarter):
    width = int(img.shape[1])
    height = int(img.shape[0])
    if monitorNo == 2:
        if quarter == 1:
            return img[0: int(height/2), int(width/2): int(3*width/4)]

def canny(img):
    rangeMax = 255
    rangeMin = 190
    grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    grey = cv.inRange(grey, rangeMin, rangeMax)
    edges = cv.Canny(grey,50,100)
    return edges


def findPositionIndicator(img):
    rangeMax = 255
    rangeMin = 30
    indicator = templateMatch(img, './templates/position/position-indicator.png', -1, rangeMax, rangeMin)
    topLeft = indicator["topLeft"]
    bottomRight = indicator["bottomRight"]
    return img[topLeft[1]: bottomRight[1], topLeft[0]: bottomRight[0]] 

def shapeMatchCard(img):
    suits = ['small-clubs', 'small-spades', 'small-hearts', 'small-diamonds']
    cards = ['small-2','small-3','small-4','small-5','small-6','small-7','small-8','small-9','small-T','small-J','small-Q','small-K','small-A']

    matches = []
    edges = canny(img)

    identifiedSuits = []
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for suit in suits:
        suitPath = './templates/cards/' + suit + '.png'
        if not exists(suitPath):
            print("Suit not found! " + suitPath)
            continue

        suitTemplate = cv.imread(suitPath, cv.IMREAD_COLOR)
        suitEdges = canny(suitTemplate)
        suitContours, suitHierarchy = cv.findContours(suitEdges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        res = templateMatch(img, suitPath, -1)
        identifiedSuits.append({"suit": suit, "res": res})

    for card in cards:
        cardPath = './templates/cards/' + card + '.png'
        if not exists(cardPath):
            print("Card not found! " + cardPath)
            continue

        res = templateMatch(img, cardPath, -1, 255, 130, True)
        if res["score"] > 0.7:
            print(card + " " + str(res["score"]))
            for s in identifiedSuits:
                if s["res"]["score"] > 0.7:
                    x = s["res"]["topLeft"][0] - res["topLeft"][0]
                    y = s["res"]["topLeft"][1] - res["topLeft"][1]
                    print(x)
                    print(y)
                    if x < 15 and x > -15 and y > -15 and y < 15:
                        matches.append({"rank": card, "suit": s["suit"]})

    return matches

def templateCardWidth(card):
    if card == 'hearts' or card == 'clubs' or card == 'diamonds' or card == 'spades':
        return 11
    elif card == 'Q' or card == 'J' or card == 'K' or card == 'A':
        return 14
    elif card == 'T':
        return 19
    elif int(card) > 0 and int(card) < 10:
        return 9

    return 15

def templateMatch(img, templatePath, tWidth, rangeMax=255, rangeMin=130, useCanny=False):
    grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    template = cv.imread(templatePath, cv.IMREAD_GRAYSCALE)
    if tWidth != -1:
        template = cv.resize(template, (int(tWidth), int(tWidth * template.shape[0] / template.shape[1])))
    if useCanny:
        template = cv.inRange(template, rangeMin, rangeMax)
        kernal = np.ones((1, 1), np.uint8)
        template = cv.dilate(template, kernal)
        grey = cv.dilate(grey, kernal)
        #template = canny(template)
        #template = cv.Canny(template,50,100)
        #grey = canny(img)

    else:
        template = cv.inRange(template, rangeMin, rangeMax)

    w, h = template.shape[::-1]
    res = cv.matchTemplate(grey, template, cv.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    top_left = max_loc

    bottom_right = (top_left[0] + w, top_left[1] + h)
    if max_val > 0.75:
        cv.rectangle(img,top_left, bottom_right, 255, 2)
    return {"score": max_val, "topLeft": top_left, "bottomRight": bottom_right}

def templateMatchCard(img):
    rangeMax = 255
    rangeMin = 185
    grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    grey = cv.inRange(grey, rangeMin, rangeMax)
    #9s and Qc are small
    cards = ['Ac', '1c', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc', 
            'Ad', '1d', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd',
            'Ah', '1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh',
            'As', '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks']
    matches = []
    for card in cards:
        path = './templates/cards/' + card + '.png'
        if exists(path):
            template = cv.imread(path, cv.IMREAD_GRAYSCALE)
            tWidth = 28
            template = cv.resize(template, (int(tWidth), int(tWidth * template.shape[0] / template.shape[1])))
            template = cv.inRange(template, rangeMin, rangeMax)

            w, h = template.shape[::-1]
            res = cv.matchTemplate(grey, template, cv.TM_CCOEFF_NORMED)

            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            top_left = max_loc

            if max_val > 0.7:
                matches.append(card)
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv.rectangle(img,top_left, bottom_right, 255, 2)
    return matches

def getPreflopHoldings():
    monitor = pyautogui.screenshot()
    img = np.array(monitor.convert('RGB'))

    img = targetArea(img, 2, 1)
    grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    aoi = findPositionIndicator(img)
    return shapeMatchCard(aoi)
