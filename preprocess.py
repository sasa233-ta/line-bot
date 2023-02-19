
# ライブラリのインポート
import datetime
import numpy as np
import pandas as pd
from pandas_datareader import data
# import matplotlib.pyplot as plt
import yfinance as yf

import pandas_datareader.data as web

yf.pdr_override()

# add_column = ["USDJPY=X","^N225","^DJI","^GSPC","998405.T"]
add_column = ["USDJPY=X","^N225","998405.T","1563.T","2516.T","1551.T"]

# 移動平均を追加
SMA1 = 3   #短期3日
SMA2 = 5  #中期5日
SMA3 = 10  #長期10日

def mk_adddata(start,end):
    i=0
    for val in add_column:
        temp = web.get_data_yahoo(val, start)
        temp['SMA1']  = temp['Close'].rolling(SMA1).mean() 
        temp['SMA2']  = temp['Close'].rolling(SMA2).mean() 
        temp['SMA3']  = temp['Close'].rolling(SMA3).mean() 
        temp.drop('Volume', axis=1,inplace=True)
        temp = temp.add_prefix(val+"_")
        temp.dropna(inplace=True)
        temp.rename(index = lambda x:x.date(),inplace=True)
        if i == 0:
            add_data = temp
        else:
            if temp.tail(1).index == end:
                add_data = pd.merge(add_data, temp, on="Date", how="inner")
            else:
                print("b")
        i += 1
    add_data.to_pickle("./add_data/{}_add_data.pickle".format(end))

def stock_preprocess(df):

    df['weekday'] = df.index.weekday
    df.rename(index = lambda x:x.date(),inplace=True)

    df = df.dropna(how='any')

    df['SMA1'] = df['Close'].rolling(SMA1).mean() #短期移動平均の算出
    df['SMA2'] = df['Close'].rolling(SMA2).mean() #中期移動平均の算出
    df['SMA3'] = df['Close'].rolling(SMA3).mean() #長期移動平均の算出

    # OpenとCloseの差分を実体Bodyとして計算
    df['Body'] = df['Open'] - df['Close']
    # 前日終値との差分Close_diffを計算
    df['Close_diff'] = df['Close'].diff(1)
    # 目的変数となる翌日の終値Close_nextの追加
    df['Close_next'] = df['Close'].shift(-1)
    df['y_'] = 100*(df['Close_next']-df['Close'])/df['Close']
    # 前日より2％以上上昇していれば1，していなければ0
    df['y'] = df['y_'].apply(lambda x:1 if x > 2 else 0)

    # 不要な目的変数削除
    df.drop(columns=['Close_next','y_'],inplace=True)

    # 欠損値がある行を削除
    # df = df.dropna(how='any')
    df = df.fillna(method='ffill')
    df = df.fillna(method='bfill')
    return df


