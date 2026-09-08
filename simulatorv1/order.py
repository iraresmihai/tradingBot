class Order:
    def __init__(self, qty, side, id, symb):
        self.symb = symb
        self.qty = qty
        self.side = side
        self.id = id
        self.filled_qty = 0
        self.filled_avg_price = 0
        self.sum = 0
        self.status = "new"
        self.updFun = []

    def addUpdFun(self, updFun):
        self.updFun.append(updFun)
        updFun(self)

    def onUpdate(self):
        for x in self.updFun:
            x(self)

    def fill(self, qty, price):
        self.sum += qty * price
        self.filled_qty += qty
        self.filled_avg_price = self.sum / self.filled_qty
        self.status = "partially_filled"
        if self.filled_qty == self.qty:
            self.status = "filled"
        self.onUpdate()