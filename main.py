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
        monitor.getPreflopHoldings(playerID, monitorNo, quarterNo)

    def startGame():
        for line in sys.stdin:
            holdings = monitor.getPreflopHoldings()
            table = int(line[0])
            position = int(line[1])

            if preflop.RFIHandRangeDecision(holdings, lib.Position(position).name):
                print('Recommended to play hand')
                if len(line) > 3:
                    if len(line) == 4:
                        action = lib.Action.FacingRFI.value
                    else:
                        action = lib.Action.RFIVs3Bet.value

                    aggressor = int(line[2])
                    preflop.aggressorHandRangeDecision(holdings, lib.Position(position).name, lib.Action(action).name, lib.Position(aggressor).name)
                if len(line) > 5:
                    print("3Bet charts not implemented")
            else:
                print('Fold')

main = Main()
