import pyautogui
import time
import numpy as np
import pytesseract
import position
from PIL import Image
import cv2 as cv
from matplotlib import pyplot as plt
from os.path import exists

root = './monitor/'

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
    indicator = templateMatch(img, root + 'templates/position/position-indicator.png', -1, rangeMax, rangeMin)
    topLeft = indicator["topLeft"]
    bottomRight = indicator["bottomRight"]
    return img[topLeft[1]: bottomRight[1], topLeft[0]: bottomRight[0]] 

def shapeMatchCard(img):

    suits = ['clubs', 'spades', 'hearts', 'diamonds']
    cards = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']

    matches = []
    #edges = canny(img)

    img_card_1 = extractCardFromAOI(img, 1)
    img_card_2 = extractCardFromAOI(img, 2)
    grey_card_1 = cv.cvtColor(img_card_1, cv.COLOR_BGR2GRAY)
    grey_card_2 = cv.cvtColor(img_card_2, cv.COLOR_BGR2GRAY)
    custom_config = r'--oem 3 --psm 6'
    imgCardRank1 = pytesseract.image_to_string(extractRank(grey_card_1), config=custom_config).strip()
    imgCardRank2 = pytesseract.image_to_string(extractRank(grey_card_2), config=custom_config).strip()
    if imgCardRank1 == '1C' or imgCardRank1 == '10':
        imgCardRank1 = 'T'
    if imgCardRank2 == '1C' or imgCardRank2 == '10':
        imgCardRank2 = 'T'

    #contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for suit in suits:
        for card in cards:
            cardPath = root + 'templates/cards/' + card + suit[0] + '.png'
            if not exists(cardPath):
                print("Card not found! " + cardPath)
                continue


            if cardComp(img_card_1, cardPath, imgCardRank1, card):
                matches.append({"rank": card, "suit": suit})

            if cardComp(img_card_2, cardPath, imgCardRank2, card):
                matches.append({"rank": card, "suit": suit})


    if len(matches) < 2:
        rgb = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        
        first_card = extractCardFromAOI(rgb, 1)
        second_card = extractCardFromAOI(rgb, 2)

        timestamp = str(time.time())
        cv.imwrite("card_" + timestamp + "_number_1.png" , first_card)
        cv.imwrite("card_" + timestamp + "_number_2.png" , second_card)
        #cv.imshow("test", img)
        #cv.waitKey(0)
    return matches

def resize(image, width):
    return cv.resize(image, (int(width), int(width * image.shape[0] / image.shape[1])))

def extractSuit(img):
    width = int(img.shape[1])
    height = int(img.shape[0])

    x1 = int(width * 0.3 / 1.3)
    x2 = int(width * 1.2 / 1.3)
    y1 = int(height * 1.2 / 2.2)
    y2 = int(height * 2.1 / 2.2)
    return img[y1:y2, x1:x2]

def extractRank(img):
    width = int(img.shape[1])
    height = int(img.shape[0])

    x1 = int(width * 0.1 / 1.3)
    x2 = int(width * 1.2 / 1.3)
    y1 = int(height * 0.1 / 2.2)
    y2 = int(height * 1.2 / 2.2)
    return img[y1:y2, x1:x2]



def cardComp(card, templatePath, cardRank, templateRank):
    template = cv.imread(templatePath, cv.IMREAD_GRAYSCALE)
    grey_card = cv.cvtColor(card, cv.COLOR_BGR2GRAY)
    template = resize(template, 50)
    grey_card = resize(grey_card, 50)

    grey_card = cv.GaussianBlur(grey_card, (7,7), 0)
    template = cv.GaussianBlur(template, (7,7), 0)

    kernel = np.ones((5,5), np.uint8)
    grey_card = cv.dilate(grey_card, kernel)
    template = cv.dilate(template, kernel)

    suitComp = templateMatch(extractSuit(template), grey_card, -1, -1, -1, True)
    if suitComp["score"] > 0.99 and templateRank == cardRank:
        return True
    return False

def extractCardFromAOI(img, cardNo):
    x1 = int(117 * 17.5 / 29)
    x2 = int(117 * 21 / 29)
    x3 = int(117 * 22.5 / 29)
    x4 = int(117 * 26 / 29)
    y1 = int(37 * 1.5 / 9.2)
    y2 = int(37 * 7.5 / 9.2)

    if cardNo == 1:
        return img[y1:y2, x1:x2]
    elif cardNo == 2:
        return img[y1:y2, x3:x4]
    else:
        raise Exception("extractCardFromAOI: Card not specified correctly")

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

def templateMatch(img, templatePath, tWidth, rangeMax=255, rangeMin=130, isGrey=False):
    if not isGrey:
        grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    else:
        grey = img

    if isinstance(templatePath, str):
        template = cv.imread(templatePath, cv.IMREAD_GRAYSCALE)
    else:
        template = templatePath
    if tWidth != -1:
        template = cv.resize(template, (int(tWidth), int(tWidth * template.shape[0] / template.shape[1])))
    if rangeMin != -1 and rangeMax != -1:
        template = cv.inRange(template, rangeMin, rangeMax)

    #cv.imshow('template', template)
    #cv.imshow('grey', grey)
    #cv.waitKey(0)
    method = cv.TM_CCOEFF_NORMED
    w, h = template.shape[::-1]
    res = cv.matchTemplate(grey, template, method)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc

    bottom_right = (top_left[0] + w, top_left[1] + h)
    #if max_val > 0.75:
    #    cv.rectangle(img,top_left, bottom_right, 255, 2)
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
        path = root + 'templates/cards/' + card + '.png'
        if exists(path):
            template = cv.imread(path, cv.IMREAD_GRAYSCALE)
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

def getPreflopHoldings(playerID, monitorNo, quarterNo):
    startTime = time.time()
    monitor = pyautogui.screenshot()
    img = np.array(monitor.convert('RGB'))

    img = targetArea(img, monitorNo, quarterNo)
    pos = position.findPlayerPosition(img, playerID)
    print("END RESULT")
    print(pos.name)
    return []
    grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    aoi = findPositionIndicator(img)

    res =  shapeMatchCard(aoi)

    endTime = time.time()
    print(endTime - startTime)
    return res
