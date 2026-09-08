from SMAStrategy import SMAStrategy
from backtester import Backtester
import pandas as pd
from InfoCreate import InfoCreate
import pyarrow

aux = InfoCreate(file_paths=["aapl_tsla_daily_2024.parquet"], symbols=["AAPL"], start="2024-01-02 09:00:00+00:00", end="2024-01-03 00:59:00+00:00", spread=0.01)

df = aux.data

strat = SMAStrategy(2, 10, 0, 'AAPL')
back = Backtester(strat)
print(back.testOnData(df).getCurrentValue())



