from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import datetime as dt
from bs4 import BeautifulSoup # BeautifulSoup をインポート

# 情報の取得終了日を指定する
dt_now = dt.datetime.now()
end = dt.date.today()
if dt_now.weekday() == 0:
    end = end + dt.timedelta(days=-3)
elif dt_now.weekday() == 6:
    end = end + dt.timedelta(days=-2)
elif dt_now.weekday() == 5:
    end = end + dt.timedelta(days=-1)   
elif dt_now.hour<20 and 0<dt_now.weekday()<5:
    end = end + dt.timedelta(days=-1)

# sample_file.txtファイルを"読み込みモード"で開く
file_data = open(".././line_bot_local_files/rakuten_pass.txt", "r")
#それぞれの行をまとめて取得する
lines = file_data.readlines()
 
#開いたファイルを閉じる
file_data.close()

url = lines[0]
rak_id = lines[1]
rak_pass = lines[2]
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

driver.find_element_by_id('form-login-pass').send_keys(rak_pass)
driver.find_element_by_id('form-login-id').send_keys(rak_id)

# driver.find_element_by_id('login-btn').click()
time.sleep(3)
driver.find_elements_by_class_name('pcm-gl-nav-01__button')[1].click()
time.sleep(3)
driver.find_elements_by_class_name('pcm-gl-nav-03__button')[1].click()
time.sleep(5)

# iframeの操作へ
driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))
driver.find_element_by_id('R4').click()
time.sleep(5)


html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, "html.parser")
el = soup.find("div",attrs={ 'class': 'resulttablebox' })
table = el.find('table')
df1 = pd.read_html(str(table),header=0)[0]

driver.find_element_by_link_text('次へ').click()
time.sleep(5)

html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, "html.parser")
el = soup.find("div",attrs={ 'class': 'resulttablebox' })
table = el.find('table')
df2 = pd.read_html(str(table),header=0)[0]

dfs = pd.concat([df1,df2])
dfs.to_excel(".././line_bot_local_files/stock_data/{}_割安株.xlsx".format(end))

driver.close()
driver.quit()
exit()                                                                                                                                                                                                                                                                                                                                                                                     