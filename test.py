import pred
# ライブラリのインポート
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas_datareader import data
# import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.model_selection import train_test_split
# 線形回帰モデルのLinearRegressionをインポート
from sklearn.linear_model import LinearRegression

from sklearn.metrics import mean_squared_error as mse

# 時系列分割のためTimeSeriesSplitのインポート
from sklearn.model_selection import TimeSeriesSplit
import pandas_datareader.data as web

yf.pdr_override()


ticker_symbol='7353'

message = pred.predict(ticker_symbol)
print(message)