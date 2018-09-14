import time
from bs4 import BeautifulSoup
import pandas as pd
from itertools import count
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

#조회 파라미터 셋팅
def setPram(yyyy,mm,dd):
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    # os 종류에 따라 다른 드라이버 로드
    if os.name == 'nt':
        driverPath='./driver/chromedriver.exe'
    elif os.name=='posix':
        driverPath='/home/datamaster/weather_detection/collect/driver/chromedriver'

    driver = webdriver.Chrome(executable_path=driverPath
                              ,chrome_options=chrome_options
                              )
    driver.implicitly_wait(3)
    driver.get('https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36')

    #   1. set Search Type
    data_type = 'F00503'  # 분 자료
    set_time = driver.find_element_by_xpath("//option[@value='" + data_type + "']")
    set_time.click()

    #       달력 프로그램 실행
    script_startDt = "datePickerShow('startDt')"
    driver.execute_script(script_startDt)

    #       start 파라미터 셋팅
    driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[1]/option[@value=' + yyyy + ']').click()
    driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[2]/option[@value=' + str(int(mm) - 1) + ']').click()
    driver.find_element_by_xpath('//a[contains(text(), "{0}") and @class="ui-state-default"]'.format(str(int(dd))) ).click()

    script_endDt = "datePickerShow('endDt')"
    driver.execute_script(script_endDt)

    #       end 파라미터 셋팅
    driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[1]/option[@value=' + yyyy+ ']').click()
    driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[2]/option[@value=' + str(int(mm) - 1) + ']').click()
    driver.find_element_by_xpath('//a[contains(text(), "{0}") and @class="ui-state-default"]'.format(str(int(dd))) ).click()

    #       지점명으로 선택
    driver.find_element_by_xpath('//*[@id="btnStn1"]').click()
    time.sleep(3)

    #       지점명 전체 선택
    driver.find_element_by_xpath('//*[@id="ztree_1_check"]').click()
    driver.execute_script('fnStnConfirm()')

    #       요소 선택
    driver.find_element_by_xpath('//*[@id="gubun"]').click()
    time.sleep(3)

    #       요소 전체선택
    driver.find_element_by_xpath('//*[@id="ztree_1_check"]').click()
    driver.execute_script('fnElementConfirm()')

    driver.find_element_by_xpath('//*[@id="schListCnt"]/option[10]').click()

    # 조회!
    driver.find_element_by_xpath('//*[@id="dsForm"]/div[3]/a[1]/span').click()
    time.sleep(5)

    return driver

def crawlingData(yyyy, mm, dd, driver):
    #   4. Source crawling
    header = []
    dataset = []
    for page in count(start=1):#range(1360,1377):
        script = 'goPage(%d)' % page
        driver.execute_script(script)
        time.sleep(2)

        html = driver.page_source
        html = html.replace('<td style="width:100px;"></td>', '<td style="width:100px;">0</td>')
        bs = BeautifulSoup(html, 'html.parser')
        table = bs.find('table', attrs={'class': 'bbsList table'})
        if page == 1:
            #       데이터 그리드를 잡아서 header를 가져온다.
            tag_thead = table.find('thead')
            tag_trs = tag_thead.find('tr', attrs={'id': 'headerNm'})
            # 1row Header
            for tag_tr in list(tag_trs.strings):
                header.append(tag_tr)

        #       데이터 그리드를 잡아서 data를 가져온다.
        tbody = table.find('tbody', attrs={'id': 'contentsList'})
        tds = tbody.findAll('tr')

        # 마지막 페이지에 도달하면 빠져나온다.
        if len(tds)==0:
            break

        # 복수row Data
        for td in tds:
            dataset.append(list(td.strings))
            print(list(td.strings))

    result = pd.DataFrame(dataset, columns=header)
    result.to_csv(
        '../data/min/weatherByMin_{0}.csv'.format(yyyy+mm+dd),
        encoding='utf-8',
        mode='w',
        index=False
    )

def main(yyyy,mm,dd):
    # cm = crawling_min()
    driver = setPram(yyyy, mm, dd)
    crawlingData(yyyy, mm, dd, driver)

# if __name__=='__main__':
#     cm = crawling_min()
#     cm.setPram()
#     cm.crawlingData()
