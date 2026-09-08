from strategy import Strategy

class SMAStrategy(Strategy):
    def __init__(self, SMA_S, SMA_L, startCapital, symb):
        super().__init__(startCapital)
        self.short = SMA_S
        self.long = SMA_L
        self.currLen = 0
        self.sumShort = self.sumLong = 0
        self.lastPos = []
        self.symb = symb

    def onInfoUpd(self, data):
        super().onInfoUpd(data)
        self.sumShort += self.currInfo[self.symb]['open']
        self.sumLong += self.currInfo[self.symb]['open']
        self.lastPos.append(self.currInfo[self.symb]['open'])
        if len(self.lastPos) > self.short:
            self.sumShort -= self.lastPos[-(self.short+1)]
        if len(self.lastPos) > self.long:
            self.sumLong -= self.lastPos[-(self.long+1)]
        #print(self.currInfo.name, self.sumShort / self.short, self.sumLong / self.long)
        if len(self.lastPos) >= self.long:
            if self.sumShort / self.short < self.sumLong / self.long:
                super().matchBalance(self.symb, 1)
            else:
                super().matchBalance(self.symb, -1)