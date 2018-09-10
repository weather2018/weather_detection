import time
from selenium import webdriver
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
from itertools import count

class crawling_min():
    def __init__(self):
        now = str(datetime.now() - timedelta(days=1))
        now = now.split(' ')
        yyyymmdd = now[0].replace('-', '')
        hhmmss = now[1].split('.')[0].split(':')[:2]
        self.timeDic = {'yyyy': yyyymmdd[0:4],
                        'mm': yyyymmdd[4:6],  # str(int(yyyymmdd[4:6]) - 1),
                        'dd': yyyymmdd[6:8],  # str(int()),
                        'hhmm': hhmmss[0] + hhmmss[1]}

        self.driver = webdriver.Chrome('../chromeself.driver.exe')
        url = 'https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36'
        self.driver.get(url)

# 전일 시간으로 년월일시분초 초기화
    def now(self):
        now = str(datetime.now() - timedelta(days=1))
        now = now.split(' ')
        yyyymmdd = now[0].replace('-', '')
        hhmmss = now[1].split('.')[0].split(':')[:2]
        self.timeDic = {'yyyy': yyyymmdd[0:4],
                   'mm': yyyymmdd[4:6],  # str(int(yyyymmdd[4:6]) - 1),
                   'dd': yyyymmdd[6:8],  # str(int()),
                   'hhmm': hhmmss[0] + hhmmss[1]}
        return self.timeDic

#조회 파라미터 셋팅
    def setPram(self):
        print(self.timeDic)
        #   1. set Search Type
        data_type = 'F00503'  # 분 자료
        set_time = self.driver.find_element_by_xpath("//option[@value='" + data_type + "']")
        set_time.click()

        #       달력 프로그램 실행
        script_startDt = "datePickerShow('startDt')"
        self.driver.execute_script(script_startDt)

        #       start 파라미터 셋팅
        self.driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[1]/option[@value=' + self.timeDic['yyyy'] + ']').click()
        self.driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[2]/option[@value=' + str(int(self.timeDic['mm']) - 1) + ']').click()
        self.driver.find_element_by_xpath('//a[contains(text(), "{0}") and @class="ui-state-default"]'.format(str(int(self.timeDic['dd']))) ).click()

        script_endDt = "datePickerShow('endDt')"
        self.driver.execute_script(script_endDt)

        #       end 파라미터 셋팅
        self.driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[1]/option[@value=' + self.timeDic['yyyy'] + ']').click()
        self.driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/select[2]/option[@value=' + str(int(self.timeDic['mm']) - 1) + ']').click()
        self.driver.find_element_by_xpath('//a[contains(text(), "{0}") and @class="ui-state-default"]'.format(str(int(self.timeDic['dd']))) ).click()

        #       지점명으로 선택
        self.driver.find_element_by_xpath('//*[@id="btnStn1"]').click()
        time.sleep(3)

        #       지점명 전체 선택
        self.driver.find_element_by_xpath('//*[@id="ztree_1_check"]').click()
        self.driver.execute_script('fnStnConfirm()')

        #       요소 선택
        self.driver.find_element_by_xpath('//*[@id="gubun"]').click()
        time.sleep(3)

        #       요소 전체선택
        self.driver.find_element_by_xpath('//*[@id="ztree_1_check"]').click()
        self.driver.execute_script('fnElementConfirm()')

        self.driver.find_element_by_xpath('//*[@id="schListCnt"]/option[10]').click()

        # 조회!
        self.driver.find_element_by_xpath('//*[@id="dsForm"]/div[3]/a[1]/span').click()
        time.sleep(5)

    def crawlingData(self):
        #   4. Source crawling
        header = []
        dataset = []
        for page in count(start=1):#range(1360,1377):
            script = 'goPage(%d)' % page
            self.driver.execute_script(script)
            time.sleep(2)

            html = self.driver.page_source
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
            '../data/weatherByMin_{0}.csv'.format(self.timeDic['yyyy']+self.timeDic['mm']+self.timeDic['dd']),
            encoding='utf-8',
            mode='w',
            index=False
        )

def main():
    cm = crawling_min()
    cm.setPram()
    cm.crawlingData()

if __name__=='__main__':
    cm = crawling_min()
    cm.setPram()
    cm.crawlingData()
