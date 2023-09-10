import preprocess
import os
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

dt_now = datetime.datetime.now()
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


# 日経平均などの説明変数準備
files = os.listdir("./add_data/")
if len(files)>1:
    for file in files:
        os.remove("./add_data/{}".format(file))
is_file = os.path.isfile("./add_data/{}_add_data.pickle".format(end))
if not is_file:
    preprocess.mk_adddata(start,end)
add_data = pd.read_pickle("./add_data/{}_add_data.pickle".format(end)) 
print(add_data.columns)
print(end)