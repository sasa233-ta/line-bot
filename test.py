# ライブラリのインポート
import pred
import random
import datetime 
import pandas as pd
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# いくつの株を予測するか(最大50くらいでお願い)
k = 50

# 本日の日時を取得
dt_now = datetime.datetime.now()

# 情報の取得開始日を指定する
start = '2017-02-01'

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
stocks = pd.read_excel(".././line_bot_local_files/stock_data/{}_成長株.xlsx".format(end))

# stocks = stocks[stocks["過去3年平均売上高成長率(予)(%)"] > 5]
stock_list = stocks["コード ▲"].dropna().tolist()

stock_list = [str(s).replace('.0', '') for s in stock_list]
stock_list = random.sample(stock_list,k)
# exit()
# ここから㈱ごとにループ
arr={}
for stock_code in stock_list:
    val_arr = {}
    rank = pred.predict(stock_code)
    if not rank == "企業コードを確認してください":
        if rank[0]<=2:
            val_arr['rank']= rank[0]
            val_arr['threshold']= rank[1]
            arr[stock_code]=val_arr
        else:
             continue
with open(".././line_bot_local_files/recommend.json", mode="wt", encoding="utf-8") as f:
	json.dump(arr, f, ensure_ascii=False, indent=2)

driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.get("http://127.0.0.1:5000/recommend")
driver.get("https://sassa2imo.pythonanywhere.com/recommend")
driver.find_element_by_name('stocklist').send_keys('D:/python/line_bot_local_files/recommend.json')
driver.find_element_by_id('upload').click()

driver.close()
driver.quit()
exit() 