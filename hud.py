class HUDPlayer:
    preflopRaises = 0
    preflopCalls = 0
    limps = 0
    hands = 0

    def __init__(self, name):
        self.name =  name

    def setPreflopRaise():
        preflopRaises += 1

    def setLimps():
        limps += 1

    def setHands():
        hands += 1

    def setPreflopCalls():
        preflopCalls += 1


    def getVPIP():
        return (preflopRaises + limps + preflopCalls) / hands
