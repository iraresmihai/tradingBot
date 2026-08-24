import pandas as pd

class ClockCounter:
    def __init__(self, indexData, until):
        self.indexData = indexData
        self.until = until
        self.currPos = 0
        self.running = False
        self.phases = {"data": [], "market": [], "strategy": []}


    def addFun(self, fun, phase = "strategy"): #always add callback functions of marketplace and info class first
        self.phases[phase].append(fun)

    def makeIteration(self):
        if not self.running:
            return

        for phase, fn in self.phases.items():
            for x in fn:
                x(self.indexData[self.currPos])
        self.currPos += 1

    def run(self):
        self.running = True
        while self.running:
            self.makeIteration()
            if ( self.currPos >= len(self.indexData) or self.indexData[self.currPos] > self.until):
                self.running = False