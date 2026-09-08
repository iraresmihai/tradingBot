from InfoCreate import InfoCreate
from clockCounter import ClockCounter
from marketplace import Marketplace
from marketplaceComm import OrderFiller
from orderTracker import OrderTracker
from strategy import Strategy
from infoFeed import InfoFeed
import numpy as np

class Backtester():
    def __init__(self, strategy):
        self.strategy = strategy

    def testOnData(self, data):
        self.strategy.reset()

        indexData = data.index
        clock = ClockCounter(indexData, indexData[-1], data)
        marketplace = Marketplace(clock)
        infoFeed = InfoFeed(self.strategy, clock, self.strategy.symbToTrade)
        orderFill = OrderFiller(self.strategy, marketplace)
        self.strategy.orderFiller = orderFill

        pnlTrack = OrderTracker(orderFill, clock, self.strategy.startCash)

        clock.run()

        return pnlTrack

    def makeInSamplePermutationTest(self, data):
        lenPerm = len(data) - 1
        sym = data.columns.get_level_values("symbol")
        aux = InfoCreate(sym, data = data)
        perm = aux.makePermutation()

        return self.testOnData(perm)

