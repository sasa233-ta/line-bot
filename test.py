# ライブラリのインポート
import preprocess
import pred
import os
import random
import datetime 
import numpy as np
import pandas as pd
from pandas_datareader import data
import pandas_datareader.data as web
# import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.model_selection import train_test_split
# 線形回帰モデルのLinearRegressionをインポート
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as mse
# 時系列分割のためTimeSeriesSplitのインポート
from sklearn.model_selection import TimeSeriesSplit
yf.pdr_override()

# いくつの株を予測するか(最大50くらいでお願い)
k = 10

# 本日の日時を取得
dt_now = datetime.datetime.now()

# 情報の取得開始日を指定する
start = '2019-02-01'

# 情報の取得終了日を指定する
end = datetime.date.today()
if dt_now.weekday() == 0:
    end = end + datetime.timedelta(days=-3)
elif dt_now.weekday() == 6:
    end = end + datetime.timedelta(days=-2)
elif dt_now.weekday() == 5:
    end = end + datetime.timedelta(days=-1)   
elif dt_now.hour<20 and 0<dt_now.weekday()<5:
    end = end + datetime.timedelta(days=-1)

# 予測する証券コードを準備
stocks = pd.read_excel(".././finance/stock_data/{}_割安株.xlsx".format(end))

stocks = stocks[stocks["過去3年平均売上高成長率(予)(%)"] > 5]
stock_list = stocks["コード ▲"].dropna().tolist()

stock_list = [str(s).replace('.0', '') for s in stock_list]
stock_list = random.sample(stock_list,k)
# exit()
# ここから㈱ごとにループ
arr={}
for stock_code in stock_list:
    val_arr = {}
    rank = pred.predict(stock_code)
    if rank[0]<=2:
        val_arr['rank']= rank[0]
        val_arr['threshold']= rank[1]
        arr[stock_code]=val_arr

print(arr)