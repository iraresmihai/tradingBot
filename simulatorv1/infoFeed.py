from clockCounter import ClockCounter
from strategy import Strategy

class InfoFeed:
    def __init__(self,  strat: Strategy, clock: ClockCounter, symb):
        self.clock = clock
        self.symb = symb
        self.currTime = ""
        clock.addFun(self.onUpdate, "data")
        self.strategy = strat
        self.toCall = [self.strategy.onInfoUpd]
        self.oldData = None

    def addToCall(self, f):
        self.toCall.append(f)

    def onUpdate(self, currTime):
        self.currTime = currTime
        data = self.oldData
        self.oldData = self.clock.getData().loc[self.symb]
        if data is not None:
            for f in self.toCall:
                f(data)