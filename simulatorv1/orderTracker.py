from marketplaceComm import OrderFiller
from clockCounter import ClockCounter
import pandas as pd

class OrderTracker:
    def __init__(self, orderFill : OrderFiller, clock : ClockCounter, startCapital):
        self.clock = clock
        self.currTime = 0
        orderFill.addToCall(self.onUpdOrder)
        clock.addFun(self.onUpdTime)
        self.positions = {}
        self.cash = startCapital
        self.times = []
        self.equities = []

    def onUpdOrder(self, order):
        if order.status == "filled":
            sgn = 1
            if order.side == "sell":
                sgn = -1

            self.cash -= sgn * order.qty * order.filled_avg_price
            #print(self.cash)
            if order.symb not in self.positions:
                self.positions[order.symb] = 0

            self.positions[order.symb] += sgn * order.qty

    def getCurrentValue(self):
        ans = self.cash
        data = self.clock.getData()
        for symb, pos in self.positions.items():
            ans += pos * data.loc[symb, "open"]
        return ans

    def onUpdTime(self, currTime):
        self.currTime = currTime
        #print(currTime)
        self.times.append(currTime)
        self.equities.append(self.getCurrentValue())

    def getHoleEquityHistory(self):
        return pd.Series(self.equities, index=pd.Index(self.times, name="timestamp"), name="equity")