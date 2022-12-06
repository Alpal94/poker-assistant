import time
import monitor

class Main:
    def __init__(self, loop):
        while True:
            holdings = monitor.getPreflopHoldings()
            print(holdings)
            if not loop:
                return
            else:
                time.sleep(1)

main = Main(False)
