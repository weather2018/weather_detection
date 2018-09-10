import time
import datetime
import os
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36'
DIRECTORY = 'D:/prj/log'

now = str(datetime.datetime.now())      # 2018-09-03 20:37:13.008451
today = now.replace('-', '')[:6]        # 201809
DAY = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]      # 월별 마지막 일자 리스트

# 현재 날짜를 기준으로 어제 날짜의 year, month, day 세팅
set_year = now[:4]
set_month = now[5:7] if '0' not in now[5:7] else now[6:7]
set_day = int(now[8:10])-1 if '0' not in now[8:9] else int(now[9:10])-1

# 첫 페이지 로딩
driver = webdriver.Chrome('D:/chromedriver.exe')
driver.get(url)
time.sleep(2)

# set data type (시간/일/월/년/분)
data_type = 'F00501'    # 일 자료
driver.find_element_by_xpath("//option[@value='" + data_type + "']").click()

# set branch (지점)
driver.find_element_by_xpath('//*[@id="btnStn1"]').click()
time.sleep(2)

driver.find_element_by_xpath('//*[@id="ztree_1_check"]').click()
time.sleep(2)

driver.execute_script('fnStnConfirm()')
time.sleep(2)

# set elements (요소)
driver.find_element_by_xpath('//*[@id="gubun"]').click()
time.sleep(2)

driver.find_element_by_xpath('//*[@id="ztree_1_check"]').click()
time.sleep(2)

driver.execute_script('fnElementConfirm()')
time.sleep(2)

# set search list count (10/20/30/40/50/60/70/80/90/100)
driver.find_element_by_xpath('//*[@id="schListCnt"]/option[10]').click()
time.sleep(2)

# make year directory
try:
    if not (os.path.isdir((DIRECTORY + '/year=%s') % set_year)):
        os.makedirs(os.path.join((DIRECTORY + '/year=%s') % set_year))
except OSError as e:
    print("Failed to create directory")

# set range (startDt)
script_startDt = "datePickerShow('startDt')"
driver.execute_script(script_startDt)

driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[1]/option[@value=' + set_year +']').click()
driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[2]/option[' + set_month + ']').click()
day_td = driver.find_element_by_tag_name('td')
try:
    day = day_td.find_element_by_xpath('//a[contains(text(), "{0}") and @class="ui-state-default"]'.format(set_day))
except:
    day = day_td.find_element_by_xpath('//a[contains(text(), "{0}") and @class="ui-state-default ui-state-active"]'.format(set_day))
day.click()

time.sleep(5)

# set range (endDt)
script_endDt = "datePickerShow('endDt')"
driver.execute_script(script_endDt)

driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[1]/option[@value=' + set_year +']').click()
driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[2]/option[' + set_month + ']').click()
day_td = driver.find_element_by_tag_name('td')
try:
    day = day_td.find_element_by_xpath('//a[contains(text(), "{0}") and @class="ui-state-default"]'.format(set_day))
except:
    day = day_td.find_element_by_xpath('//a[contains(text(), "{0}") and @class="ui-state-default ui-state-active"]'.format(set_day))
day.click()

time.sleep(5)

# lookup (조회)
lookup = driver.find_element_by_xpath('//*[@id="dsForm"]/div[3]/a[1]/span')
lookup.click()
time.sleep(5)

# rendering HTML 가져오기
html = driver.page_source
html = html.replace('<td style="width:100px;"></td>', '<td style="width:100px;">0</td>')

# parsing data
bs = BeautifulSoup(html, 'html.parser')
tag_table = bs.find('table', attrs={'class':'bbsList table'})
tag_thead = tag_table.find('thead')
tags_tr1 = tag_thead.find('tr', attrs={'id':'headerNm'})

tag_tbody = bs.find('tbody', attrs={'id':'contentsList'})
tags_tr2 = tag_tbody.findAll('tr')

results = []
headers = []
for head in list(tags_tr1.strings):
    headers.append(head)
results.append(headers)

for tag_tr in tags_tr2:
    strings = list(tag_tr.strings)
    results.append(strings)

# make dataframe
table = pd.DataFrame(results)

# make month directory
RESULT_DIRECTORY = (DIRECTORY + '/year=%s' + '/month=%s') % (set_year, set_month)
try:
    if not (os.path.isdir(RESULT_DIRECTORY)):
        os.makedirs(os.path.join(RESULT_DIRECTORY))
except OSError as e:
    print("Failed to create directory")

day = '0' + str(set_day) if int(set_day) < 10 else str(set_day)

# make csv file
table.to_csv(('{0}/workdate=%s%s.csv' %(today, day)).format(RESULT_DIRECTORY), encoding='utf-8')
