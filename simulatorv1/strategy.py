from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from marketplaceComm import OrderFiller
    from order import Order

class Strategy:
    def __init__(self, startCapital):
        self.currInfo = None
        self.symbToTrade = ["AAPL"]
        self.orderFiller = None #HAVE TO SET IT
        self.positions = {}
        self.cash = self.startCash = startCapital

        #if clock is not None:
            #self.orderFiller = OrderFiller(self, market)
            #self.infoFeed = InfoFeed(self, clock, self.symbToTrade)
            #self.tracker = OrderTracker(self.orderFiller, clock, startCapital)

    def reset(self):
        self.currInfo = None
        self.positions = {}
        self.orderFiller = None
        self.cash = self.startCash

    def onOrderUpd(self, order : Order):
        if order.symb not in self.positions:
            self.positions[order.symb] = 0
        if order.status == "filled":
            if order.side == "buy":
                self.positions[order.symb] += order.qty
            else:
                self.positions[order.symb] -= order.qty

    def onInfoUpd(self, data):
        self.currInfo = data

    def matchBalance(self, symb, qty):
        if symb not in self.positions:
            self.positions[symb] = 0
        #qty=0
        if qty > self.positions[symb]:
            self.orderFiller.makeTrade(symb, qty - self.positions[symb], 'buy')
        else:
            if qty < self.positions[symb]:
                self.orderFiller.makeTrade(symb, self.positions[symb] - qty, 'sell')

    def closePositions(self):
        for symb in self.positions:
            if self.positions[symb] != 0:
                if self.positions[symb] > 0:
                    self.orderFiller.makeTrade(symb, self.positions[symb], 'sell')
                else:
                    self.orderFiller.makeTrade(symb, self.positions[symb], 'buy')
