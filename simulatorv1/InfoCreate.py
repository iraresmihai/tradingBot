import pandas as pd
import numpy as np

class InfoCreate():
    def __init__(self, symbols, start = None, end = None, whereToSave = None, spread = 0.02, file_paths = None, data = None, rng = None):
        self.rng = rng
        if rng is None:
            self.rng = np.random.default_rng()
        self.file_paths = file_paths
        self.symbols = symbols
        self.start = start
        self.end = end
        self.spread = spread
        self.whereToSave = whereToSave
        self.data = None
        if data is not None:
            self.data = data.copy()
        self.get_data()

    def get_data(self):
        if self.data is None:
            frames = []
            for name in self.file_paths:
                frames.append(pd.read_parquet(name))
            aux = pd.concat(frames).sort_index()
            aux = aux[aux.index.get_level_values("symbol").isin(self.symbols)]
            aux = aux[~aux.index.duplicated(keep="last")]
            aux = aux.unstack("symbol").swaplevel(axis=1).sort_index(axis=1)
            self.data = aux.ffill()

        if self.start is not None:
            self.data = self.data.loc[self.start:self.end].copy()
        self.makeBidAsk(self.data)

        if self.whereToSave is not None:
            self.data.to_parquet("{}.parquet".format(self.whereToSave))

    def makeBidAsk(self, data):
        names = data.columns.get_level_values("symbol").unique()
        for name in names:
            o = data[name]["open"]
            data.loc[:, (name, "bid")] = o - self.spread
            data.loc[:, (name, "ask")] = o + self.spread
        data.sort_index(axis=1, inplace=True)

    def makePermutation(self, whereToSave = None):
        sym = self.data.columns.get_level_values("symbol").unique()
        logBars = np.log(self.data.loc[:, (sym, ["close", "high", "low", "open"])])
        startTick = logBars.iloc[0]
        a1 = logBars.loc[:, (sym, "open")]
        a2 = logBars.loc[:, (sym, "close")]
        a3 = logBars.loc[:, (sym, "high")]
        a4 = logBars.loc[:, (sym, "low")]

        relGap = a1.to_numpy() - a2.shift().to_numpy()
        relOpen = a1.to_numpy() - a2.to_numpy()
        relHigh = a3.to_numpy() - a2.to_numpy()
        relLow = a4.to_numpy() - a2.to_numpy()
        l = len(a1) - 1
        ids = np.arange(l)
        perm = self.rng.permutation(ids)
        perm2 = self.rng.permutation(ids)
        relLow = relLow[1:][perm]
        relOpen = relOpen[1:][perm]
        relHigh = relHigh[1:][perm]
        relGap = relGap[1:][perm2]

        aux = np.zeros((l + 1, 4 * len(sym)))
        aux[0] = startTick.to_numpy()
        for i in range(len(sym)):
            aux[1:, i * 4] = aux[0, i * 4] + np.cumsum(relGap[:, i] - relOpen[:, i], axis=0)
            aux[1:, i * 4 + 1] = relHigh[:, i] + aux[1:, i * 4]
            aux[1:, i * 4 + 2] = relLow[:, i] + aux[1:, i * 4]
            aux[1:, i * 4 + 3] = relOpen[:, i] + aux[1:, i * 4]

        aux = np.exp(aux)
        ans = self.data.copy()
        ans.loc[:, (sym, ["close", "high", "low", "open"])] = aux
        self.makeBidAsk(ans)

        if whereToSave is not None:
            ans.to_parquet("{}.parquet".format(whereToSave))

        return ans