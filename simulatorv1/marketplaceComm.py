from __future__ import annotations
from typing import TYPE_CHECKING

from marketplace import Marketplace

if TYPE_CHECKING:
    from strategy import Strategy
    from order import Order

class OrderFiller:
    def __init__(self, strategy: Strategy, market: Marketplace):
        self.strategy = strategy
        self.toCall = [strategy.onOrderUpd]
        self.market = market
        self.orders = {}

    def addToCall(self, call):
        self.toCall.append(call)

    def onUpdate(self, order: Order):
        self.orders[order.id] = order
        if order.status == "filled":
            for x in self.toCall:
                x(order)

    def makeTrade(self, symb, qty, side):
        self.market.makeTrade(side, qty, symb, self.onUpdate)

