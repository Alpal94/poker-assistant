import sys
sys.path.insert(0, "./monitor")
sys.path.insert(0, "./position")

import time
import monitor
import preflop
import lib

class Main:
    def __init__(self):

        if len(sys.argv) == 1:
            raise Exception("Invalid commandline arguments")

        if len(sys.argv) == 4:
            monitorNo = int(sys.argv[2])
            quarterNo = int(sys.argv[3])
        else:
            monitorNo = 2
            quarterNo = 1

        playerID = int(sys.argv[1])
        #monitor.getPreflopHoldings(playerID, monitorNo, quarterNo)
        self.startGame(playerID, monitorNo, quarterNo)

    def startGame(self, playerID, monitorNo, quarterNo):
        for line in sys.stdin:
            screenshot = monitor.getScreenshot(monitorNo, quarterNo)
            holdings = monitor.getPreflopHoldings(screenshot, playerID)
            position = monitor.getHeroPosition(screenshot, playerID)

            print(position)
            if preflop.RFIHandRangeDecision(holdings, position.name):
                print('Recommended to play hand')
                if len(line) > 1:
                    if len(line) == 2:
                        action = lib.Action.FacingRFI.value
                    else:
                        action = lib.Action.RFIVs3Bet.value

                    aggressor = int(line[0])
                    preflop.aggressorHandRangeDecision(holdings, position.name, lib.Action(action).name, lib.Position(aggressor).name)
                if len(line) > 5:
                    print("3Bet charts not implemented")
            else:
                print('Fold')

main = Main()
