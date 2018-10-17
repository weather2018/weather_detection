import time
import pandas as pd
from selenium import webdriver
import os
from pywinauto import Application
import pywinauto.keyboard as keyboard

def yungdo():
    # 용도신청
    driver.find_element_by_xpath('//*[@id="requestForm"]/ul/li[2]/input[4]').click()
    time.sleep(1)
    # 요청
    try:
        driver.execute_script('dataOrder()')
        time.sleep(10)
    except:
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[3]/button').click()
        downloadClick(driver,1)
        time.sleep(10)

    # app = pgmConnect()
    # dlg=app['다른 이름으로 저장']
    # dlg.SetFocus()
    keyboard.SendKeys('{ESC}')
    time.sleep(2)

def pgmConnect():
    try:
        app = Application().connect(title='다른 이름으로 저장', )
    except:
        time.sleep(20)
        print('요청 실패에 따른 예외처리 시작!!')
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[3]/button').click()
        downloadClick(driver,i)
        time.sleep(10)
        app = Application().connect(title='다른 이름으로 저장', )
    return app

def downloadClick(driver,i):
    driver.find_element_by_xpath('//*[@id="contentsList"]/tr[%d]/td[4]/input' % (i)).click()
    time.sleep(8)

def save(app,j):
    time.sleep(2)
    savePath = 'C:\DEV\PycharmProjects\weather2018\data\Y%s\%s_C%s_%s.csv' % \
               (str(year), str(year), str(locCode).zfill(4), attr)
    print(str(j),'라인: ',savePath)
    app.다른_이름으로_저장.Edit1.set_edit_text(savePath)
    time.sleep(2)
    # app.다른_이름으로_저장.Button1.click()
    keyboard.SendKeys('{ENTER}')
    time.sleep(2)



# 드라이버 생성
driverPath = './driver/chromedriver.exe'
driver = webdriver.Chrome(executable_path=driverPath)
driver.get('https://data.kma.go.kr/data/rmt/rmtList.do?code=400&pgmNo=570')

# 로그인
driver.find_element_by_xpath('//*[@id="loginBtn"]').click()
time.sleep(2)
id=driver.find_element_by_id('loginId')
id.send_keys('moon_ki@naver.com')
pw=driver.find_element_by_id('passwordNo')
pw.send_keys('ansrl*6dls')
driver.find_element_by_xpath('//*[@id="loginbtn"]').click()

# 요소 전체 선택
element = driver.find_element_by_xpath('//*[@class="selectBtn1 btn btn-primary VAR1_BTN"]')
driver.execute_script('arguments[0].click();', element)
time.sleep(2)
driver.find_element_by_xpath('//*[@id="ztree_1_check"]').click()
driver.execute_script('fnStnConfirm()')

# 지역 마스터 데이터 로드
# locMst=pd.read_csv('../data/location_mst.csv',encoding='ms949')

for year in range(2015, 2018):
    # for month in range(1, 13):
    # start 파라미터
    driver.find_element_by_xpath('//*[@id="startDt"]/option[@value=' + str(year) + ']').click()
    driver.find_element_by_xpath('//*[@id="startMt"]/option[@value=' + '01' + ']').click()

    # end 파라미터
    driver.find_element_by_xpath('//*[@id="endDt"]/option[@value=' + str(year) + ']').click()
    driver.find_element_by_xpath('//*[@id="endMt"]/option[@value=' + '12' + ']').click()

    # 지역 코드 선정을 위한 시퀀스 변수
    locCode = 1

    # 지역 순차적으로 선택
    for spanId in [
                   'ztree_2'
                   #  ,'ztree_452','ztree_674','ztree_822','ztree_983',
                   # 'ztree_1084','ztree_1169','ztree_1231','ztree_1249','ztree_1852',
                   # 'ztree_2064','ztree_2232','ztree_2456','ztree_2713','ztree_3033',
                   # 'ztree_3391','ztree_3722','ztree_3768'
    ]:
        element=driver.find_element_by_xpath('//*[@class="selectBtn1 btn btn-primary VAR3_BTN"]')
        driver.execute_script('arguments[0].click();',element)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="%s_check"]' % (spanId)).click()
        driver.execute_script('fnStnConfirm()')

        # 조회
        selectcnt=driver.find_element_by_xpath('//*[@id="schListCnt"]/option[6]').click() # 100개씩 뿌린다.
        driver.find_element_by_xpath('//*[@id="dsForm"]/div[3]/a/span').click()
        time.sleep(2)

        # 페이징 처리를 위한 변수 셋팅
        totCnt = driver.find_element_by_xpath('//*[@class="SEARCH_LIST_COUNT"]').text
        j = 1  # 그리드 시퀀스
        attr = 'pty'  # 속성

        ####### 최초 작업 (시.도 별로 변함)
        downloadClick(driver,1)
        try:
            yungdo()
        except: # 로그인창이 뜰 경우, 예외처리.
            # 로그인
            driver.find_element_by_xpath('//*[@id="loginbtn"]').click()
            time.sleep(2)
            # 다운로드 클릭
            downloadClick(driver, 1)
            yungdo()


        ####### 페이지별, 다운로드
        for page in range(2,(int(totCnt)//100)+2):
            for i in range(1, 200, 2):
                # 다운로드 클릭
                downloadClick(driver,i)
                try: # APP과 Connect
                    app = pgmConnect()
                except:
                    time.sleep(5)
                    app = pgmConnect()
                save(app,j)

                j += 1
                if j % 8 == 0:
                    attr = 'wsd' # 풍속
                elif j % 8 ==1:
                    locCode += 1    # 지역 변경
                    attr = 'pty' # 강수형태
                elif j % 8 ==2:
                    attr = 'reh' # 습도
                elif j % 8 ==3:
                    attr = 'rn1' # 강수
                elif j % 8 ==4:
                    attr = 'sky' # 하늘상태
                elif j % 8 ==5:
                    attr = 't1h' # 기온
                elif j % 8 ==6:
                    attr = 'lgt' # 뇌전
                elif j % 8 ==7:
                    attr = 'vec' # 풍향

            driver.find_element_by_xpath('//*[@title="다음페이지"]').click()
            time.sleep(2)