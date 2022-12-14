import sys
sys.path.insert(0, "./monitor")
sys.path.insert(0, "./position")

import os
import time
from pynput import mouse
import monitor
import position
import preflop
import lib

class Main:
    def __init__(self):


        #monitor.getPreflopHoldings(playerID, monitorNo, quarterNo)
        #self.startGame(playerID, monitorNo, quarterNo)

        with mouse.Listener(on_click=self.onClick) as listener:
            listener.join()

    def mouseListener(self):
        listener = mouse.Listener(on_click=self.onClick)
        listener.start()

    def onClick(self, x, y, button, pressed):
        if len(sys.argv) == 1:
            raise Exception("Invalid commandline arguments")

        if len(sys.argv) == 4:
            monitorNo = int(sys.argv[2])
            quarterNo = int(sys.argv[3])
        else:
            monitorNo = 2
            quarterNo = 1
        playerID = int(sys.argv[1])

        if pressed is True:
            self.evaluateHero(playerID, monitorNo, quarterNo, (x,y))

    def evaluateHero(self, playerID, monitorNo, quarterNo, mousePos):
        screenshot = monitor.getScreenshot(monitorNo, quarterNo)
        holdings = monitor.getPreflopHoldings(screenshot, playerID)
        heroPosition = monitor.getHeroPosition(screenshot, playerID)

        action = lib.Action.RFI
        aggressor = None
        calibratedMouse = monitor.mouseTargetArea(screenshot, mousePos, monitorNo, quarterNo)
        for playerX in range(1, 10):
            playerPosition = position.getPlayerPositionCoordinates(screenshot, position.getPlayerColour(playerX))
            if playerPosition is not None:
                dist = int(pow(pow(playerPosition[0] - calibratedMouse[0], 2) + pow(playerPosition[1] - calibratedMouse[1], 2), 0.5))
                if dist < 10:
                    action = lib.Action.FacingRFI
                    aggressor = position.findPlayerPosition(screenshot, playerX)

        if aggressor is None:
            indicator = monitor.findPositionIndicatorLocation(screenshot)
            topLeft = indicator["topLeft"]
            bottomRight = indicator["bottomRight"]

            if calibratedMouse[0] < topLeft[0] or calibratedMouse[0] > bottomRight[0]:
                return
            if calibratedMouse[1] < topLeft[1] or calibratedMouse[1] > bottomRight[1]:
                return

        os.system("say " + str(quarterNo))
        if preflop.RFIHandRangeDecision(holdings, heroPosition.name):
            if action is lib.Action.FacingRFI and aggressor is not None:
                os.system("say 'check chart'")
                print("Aggressor: " + aggressor.name)
                preflop.aggressorHandRangeDecision(holdings, heroPosition.name, action.name, aggressor.name)
            else:
                print('Recommended to play hand')
                os.system("say play")
        else:
            os.system("say fold")

main = Main()
