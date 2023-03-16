from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import datetime as dt
from bs4 import BeautifulSoup # BeautifulSoup をインポート
from selenium.webdriver.common.keys import Keys

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

options = webdriver.chrome.options.Options()
profile_path = 'C:\\Users\\sassa\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
options.add_argument('--user-data-dir=' + profile_path)

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

driver.find_element_by_id('form-login-pass').send_keys(rak_pass)
driver.find_element_by_id('form-login-id').send_keys(rak_id)

time.sleep(3)
driver.find_elements_by_class_name('pcm-gl-nav-01__button')[1].click()
time.sleep(3)
driver.find_elements_by_class_name('pcm-gl-nav-03__button')[1].click()
time.sleep(5)

# iframeの操作へ
driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))
time.sleep(5)
# driver.find_element_by_class_name('goright').click()
# driver.find_element_by_id('U1').click()
# time.sleep(5)

advanced = driver.find_element_by_id('criteria_advanced')
itemboxes=advanced.find_elements_by_class_name("advancedcriteriaitembox")
i=0
link_text=['PER(株価収益率)(倍)','自己資本比率(%)','PSR(株価売上高倍率)(倍)','売上高変化率(%)','信用残/売買高レシオ(倍)']
for itembox in itemboxes:
    if i < 5:
        itembox.click()
        time.sleep(3)
        driver.find_element_by_link_text(link_text[i]).click()
        time.sleep(3)
        i+=1 
    else:
        break
time.sleep(5)

# PER(株価収益率)(倍)
driver.find_element_by_class_name('caf_per_to').send_keys((Keys.CONTROL + "a"))
driver.find_element_by_class_name('caf_per_to').send_keys(Keys.DELETE)
time.sleep(3)
driver.find_element_by_class_name('caf_per_to').send_keys('30')
time.sleep(3)

# 自己資本比率(%)
driver.find_element_by_class_name('caf_tot_asset_eqty_ratio_from').send_keys((Keys.CONTROL + "a"))
driver.find_element_by_class_name('caf_tot_asset_eqty_ratio_from').send_keys(Keys.DELETE)
time.sleep(3)
driver.find_element_by_class_name('caf_tot_asset_eqty_ratio_from').send_keys('30')
time.sleep(3)

# PSR(株価売上高倍率)(倍)
driver.find_element_by_class_name('caf_psr_to').send_keys((Keys.CONTROL + "a"))
driver.find_element_by_class_name('caf_psr_to').send_keys(Keys.DELETE)
time.sleep(3)
driver.find_element_by_class_name('caf_psr_to').send_keys('5')
time.sleep(3)

# 売上高変化率(%)
driver.find_element_by_class_name('caf_rev_growth_rate_from').send_keys((Keys.CONTROL + "a"))
driver.find_element_by_class_name('caf_rev_growth_rate_from').send_keys(Keys.DELETE)
time.sleep(3)
driver.find_element_by_class_name('caf_rev_growth_rate_from').send_keys('15')
time.sleep(3)

# 信用残/売買高レシオ(倍)
driver.find_element_by_class_name('caf_margin_vol_ratio_to').send_keys((Keys.CONTROL + "a"))
driver.find_element_by_class_name('caf_margin_vol_ratio_to').send_keys(Keys.DELETE)
time.sleep(3)
driver.find_element_by_class_name('caf_margin_vol_ratio_to').send_keys('15')
driver.find_element_by_class_name('caf_margin_vol_ratio_to').send_keys(Keys.TAB)
time.sleep(5)

html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, "html.parser")
el = soup.find("div",attrs={ 'class': 'resulttablebox' })
table = el.find('table')
df1 = pd.read_html(str(table),header=0)[0]

resultpanel = soup.find("div",attrs={ 'id': 'resultpanel' })
countval = resultpanel.find("span",attrs={ 'class': 'countval' })

countval = countval.string
print(countval)
pages = int(countval)/50
df = {}
for num in range(int(pages)):
    driver.find_element_by_link_text('次へ').click()
    time.sleep(5)

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    el = soup.find("div",attrs={ 'class': 'resulttablebox' })
    table = el.find('table')
    df[num] = pd.read_html(str(table),header=0)[0]
    if num == 0:
        df2 = pd.concat([df1,df[num]])
    else:
        df2 = pd.concat([df2,df[num]])

dfs = pd.concat([df1,df2])
dfs.to_excel(".././line_bot_local_files/stock_data/{}_成長株.xlsx".format(end))

driver.close()
driver.quit()
exit()