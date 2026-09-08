from clockCounter import ClockCounter
import pandas as pd
from order import Order

class Marketplace:
    def __init__(self, clock : ClockCounter):
        self.clock = clock
        self.ct = 0
        #clock.addFun(self.onUpd, phase="exchange")

    #def onUpd(self):
    #    self.currTime = self.clock.getTime()

    def makeTrade(self, side, qty, symb, toCall):
        currOrder = Order(qty, side, self.ct, symb)
        self.ct += 1
        print(self.clock.getTime(), qty, symb, side, self.clock.getData()[(symb, "open")], self.ct)
        currOrder.addUpdFun(toCall)
        if side == "buy":
            currOrder.fill(qty, self.clock.getData()[(symb, "ask")])
        else:
            currOrder.fill(qty, self.clock.getData()[(symb, "bid")])
