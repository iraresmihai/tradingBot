import pandas as pd

class InfoCreate():
    def __init__(self, file_paths, symbols, start, end, whereToSave, spread):
        self.file_paths = file_paths
        self.symbols = symbols
        self.start = start
        self.end = end
        self.spread = spread
        self.whereToSave = whereToSave
        self.get_data()

    def get_data(self):
        frames = []
        for name in self.file_paths:
            frames.append(pd.read_parquet(name))
        aux = pd.concat(frames).sort_index()
        aux = aux[aux.index.get_level_values("symbol").isin(self.symbols)]
        aux = aux[~aux.index.duplicated(keep="last")]
        aux = aux.unstack("symbol").swaplevel(axis=1).sort_index(axis=1)

        self.data = aux.ffill().loc[self.start:self.end].copy()
        names = self.data.columns.get_level_values("symbol").unique()
        for name in names:
            o = self.data[name]["open"]
            self.data.loc[:, (name, "bid")] = o - self.spread
            self.data.loc[:, (name, "ask")] = o + self.spread
        self.data = self.data.sort_index(axis=1)

        if self.whereToSave is not None:
            self.data.to_parquet("{}.parquet".format(self.whereToSave))