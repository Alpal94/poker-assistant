import json
import lib
import os

def RFIHandRangeDecision(hand, position):
    if position == lib.Position.BigBlind.name:
        return True

    f = open("hand-range-charts.json")
    data = json.load(f);
    handRange = data[lib.Action.RFI.name][position];
    hand.sort(key=cardToNumber, reverse=True)

    print(hand)
    for subsetRange in handRange:
        if checkCardInSubsetRange(hand, subsetRange) == True:
            return True
    return False

def aggressorHandRangeDecision(hand, position, action, aggressor):
    f = open("hand-range-charts.json")
    data = json.load(f);
    print(action)
    print(position)
    print(aggressor)
    handRangeChartURL = data[action][position][aggressor];
    os.system("gopen ./preflop-charts/" + handRangeChartURL) 

def checkCardInSubsetRange(hand, subsetRange):
    # Example of a subset of range in shortform: A9s+
    if cardToNumber(hand[0]) < rankToNumber(subsetRange[0]):
        return False
    if cardToNumber(hand[1]) < rankToNumber(subsetRange[1]):
        return False

    if subsetRange[2] == 's': #'s' means cards are suited. 'o' is offsuit
        if hand[0]["suit"] == hand[1]["suit"]: 
            return True

    if subsetRange[2] == 'o': # 'o' is offsuit
        return True

    if subsetRange[0] == subsetRange[1]: # Dealing with pairs
        if hand[0]["rank"] == hand[1]["rank"]:
            if cardToNumber(hand[0]) >= rankToNumber(subsetRange[0]):
                return True

    return False


def cardToNumber(card):
    return rankToNumber(card["rank"])

def rankToNumber(card):
    if card == 'A':
        return 14
    elif card == 'K':
        return 13
    elif card == 'Q':
        return 12
    elif card == 'J':
        return 11
    elif card == 'T':
        return 10
    else:
        return int(card)
