import json

def handRangeDecision(hand, position, action):
    f = open("hand-range-charts.json")
    data = json.load(f);
    handRange = data[action][position];
    hand.sort(key=cardToNumber, reverse=True)
    print(hand)
    for subsetRange in handRange:
        if checkCardInSubsetRange(hand, subsetRange) == True:
            return True
    return False

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
            if cardToNumber[0] >= rankToNumber[subsetRange[0]]:
                return True

    return False


def cardToNumber(card):
    return rankToNumber(card["rank"])

def rankToNumber(card):
    match card:
        case 'A':
            return 14
        case 'K':
            return 13
        case 'Q':
            return 12
        case 'J':
            return 11
        case 'T':
            return 10
        case _:
            return int(card)
