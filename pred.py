# ライブラリのインポート
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

def predict(code): 
    try:
        # 入力チェック
        try:
            if len(code)!=4:
                raise
            code = int(code)
        except:
            return "4桁の半角数字でお願いします。"

        # 入力された値を取得
        stock_code = str(code)+".T"

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

        # 日経平均などの説明変数準備
        files = os.listdir("./add_data/")
        if len(files)>1:
            for file in files:
                os.remove("./add_data/{}".format(file))
        is_file = os.path.isfile("./add_data/{}_add_data.pickle".format(end))
        if not is_file:
            preprocess.mk_adddata(start,end)
        add_data = pd.read_pickle("./add_data/{}_add_data.pickle".format(end)) 

        # 株の取得
        data_master = yf.download(tickers=stock_code, start=start,interval = "1d")

        # 株データの加工
        data_technical = preprocess.stock_preprocess(data_master)

        # 株データに説明変数の追加
        data_technical = pd.merge(data_technical, add_data, on="Date", how="inner")
        data_technical.index = pd.to_datetime(data_technical.index)

        # 学習用データとする
        train = data_technical[start : '2022-05-31']
        # テストデータとする
        test = data_technical['2022-06-01' :]

        # 学習用データとテストデータそれぞれを説明変数と目的変数に分離する
        X_train = train.drop(columns=['y']) #学習用データ説明変数
        y_train = train['y'] #学習用データ目的変数

        X_test = test.drop(columns=['y']) #テストデータ説明変数
        y_test = test['y'] #テストデータ目的変数

        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        score = np.sqrt(mse(y_test, y_pred))

        # 実際の予測結果確認
        df_result = test
        df_result['Close_pred'] = y_pred

        df_result['Pred_diff'] = df_result['Close_pred'].diff(1)
        threshold = df_result['Pred_diff'].tolist().pop()
        print(df_result[['Pred_diff','Close_pred']].tail(3))
        print(score)
        print(X_test.columns)
        if threshold>0 and score < 0.3:
            message = "期待大（参考値　Pred_diff:{}）".format(threshold)
        elif threshold>0 and 0.3<=score < 0.4:
            message = "期待中（参考値　Pred_diff:{}）".format(threshold)
        elif threshold>0 and 0.4<=score<=0.5:
            message = "期待小（参考値　Pred_diff:{}）".format(threshold)
        else:
            message = "期待なし（参考値　Pred_diff:{}）".format(threshold)

        return message
    except Exception as e:
        return "企業コードを確認してください"




