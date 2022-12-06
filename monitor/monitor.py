import pyautogui
import time
import numpy as np
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

def shapeMatchCard(img):
    suits = ['clubs', 'spades', 'hearts', 'diamonds']
    cards = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']

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
        res = templateMatch(img, suitPath, templateCardWidth(suit))
        identifiedSuits.append({"suit": suit, "res": res})

    for card in cards:
        cardPath = './templates/cards/' + card + '.png'
        if not exists(cardPath):
            print("Card not found! " + cardPath)
            continue



        res = templateMatch(img, cardPath, templateCardWidth(card))
        if res["score"] > 0.8:

            for s in identifiedSuits:
                if s["res"]["score"] > 0.8:
                    x = s["res"]["topLeft"][0] - res["topLeft"][0]
                    y = s["res"]["topLeft"][1] - res["topLeft"][1]
                    if x < 11 and x > 3 and y > 10 and y < 30:
                        matches.append({"rank": card, "suit": s["suit"]})

    return matches

def templateCardWidth(card):
    if card == 'hearts' or card == 'clubs' or card == 'diamonds' or card == 'spades':
        return 19
    elif card == 'Q' or card == 'J' or card == 'K' or card == 'A':
        return 14
    elif card == 'T':
        return 19
    elif int(card) > 0 and int(card) < 10:
        return 10

    return 15

def templateMatch(img, templatePath, tWidth):
    rangeMax = 255
    rangeMin = 185
    grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    template = cv.imread(templatePath, cv.IMREAD_GRAYSCALE)
    template = cv.resize(template, (int(tWidth), int(tWidth * template.shape[0] / template.shape[1])))
    template = cv.inRange(template, rangeMin, rangeMax)

    w, h = template.shape[::-1]
    res = cv.matchTemplate(grey, template, cv.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    top_left = max_loc

    if max_val > 0.75:
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(img,top_left, bottom_right, 255, 2)
    return {"score": max_val, "topLeft": top_left}

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

            if max_val > 0.8:
                matches.append(card)
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv.rectangle(img,top_left, bottom_right, 255, 2)
    return matches

def getPreflopHoldings():
    monitor = pyautogui.screenshot()
    img = np.array(monitor.convert('RGB'))

    img = targetArea(img, 2, 1)
    grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return shapeMatchCard(img)
