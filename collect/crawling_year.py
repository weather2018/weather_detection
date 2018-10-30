import time
from selenium import webdriver
from pywinauto import Application

def yungdo():
    # 용도신청
    driver.find_element_by_xpath('//*[@id="requestForm"]/ul/li[2]/input[4]').click()
    time.sleep(1)
    # 요청
    try:
        driver.execute_script('dataOrder()')
        time.sleep(10)
    except:
        print('yungdo, 로그인 예외처리!')
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[3]/button').click()
        downloadClick(driver,1)
        time.sleep(10)

    try:
        app = pgmConnect()
        app.다른_이름으로_저장.Button2.click()
        time.sleep(5)
        app = Application().connect(title='다른 이름으로 저장', )
        app.다른_이름으로_저장.Button2.click()
        time.sleep(2)
    except:
        # print('saveCheck, %d라인, app connetct fail'%(j))
        pass

def downloadClick(driver,i):
    driver.find_element_by_xpath('//*[@id="contentsList"]/tr[%d]/td[4]/input' % (i)).click()
    time.sleep(5)

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

def save(app,j):
    savePath = 'D:\DEV\PycharmProjects\weather_detection\data\Y%s\%s_C%s_%s.csv' % \
               (str(year), str(year), str(locCode).zfill(4), attr)
    print(str(j),'라인: ',savePath)
    app.다른_이름으로_저장.Edit1.set_edit_text(savePath)
    time.sleep(1)
    app.다른_이름으로_저장.Button1.click()
    # keyboard.SendKeys('{ENTER}')
    time.sleep(1)

def saveCheck():
    try:
        app = Application().connect(title='다른 이름으로 저장', )
        app.다른_이름으로_저장.Button1.click()
        # time.sleep(5)
        # app = Application().connect(title='다른 이름으로 저장', )
        # app.다른_이름으로_저장.Button1.click()
        time.sleep(2)
    except:
        # print('saveCheck, %d라인, app connetct fail'%(j))
        pass

def cancelCheck():
    try:
        app = Application().connect(title='다른 이름으로 저장', )
        app.다른_이름으로_저장.Button2.click()
        time.sleep(2)
    except:
        # print('saveCheck, %d라인, app connetct fail'%(j))
        pass

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

for year in range(2017,2018):
    # for month in range(1, 13):
    # start 파라미터
    driver.find_element_by_xpath('//*[@id="startDt"]/option[@value=' + str(year) + ']').click()
    driver.find_element_by_xpath('//*[@id="startMt"]/option[@value=' + '01' + ']').click()

    # end 파라미터
    driver.find_element_by_xpath('//*[@id="endDt"]/option[@value=' + str(year) + ']').click()
    driver.find_element_by_xpath('//*[@id="endMt"]/option[@value=' + '12' + ']').click()

    # 지역 코드 선정을 위한 시퀀스 변수
    # 0부터 시작한다. 다시 시작할 경우, 지역의 처음 코드로 정한다.
    locCode = 425

    # 지역 순차적으로 선택
    for spanId in [
                   # 'ztree_2',     # 서울
                   'ztree_452',   # 부산
                   'ztree_674',   # 대구
                   'ztree_822',   # 인천
                   'ztree_983',   # 광주
                   'ztree_1084',  # 대전
                   'ztree_1169',  # 울산
                   'ztree_1231',  # 세종
                   'ztree_1249',  # 경기도
                   'ztree_1852',  # 강원도
                   'ztree_2064',  # 충청북도
                   'ztree_2232',  # 충청남도
                   'ztree_2456',  # 전라북도
                   'ztree_2713',  # 전라남도
                   'ztree_3033',  # 경상북도
                   'ztree_3391',  # 경상남도
                   'ztree_3722',  # 제주
                   'ztree_3768'   # 이어도
    ]:
        element=driver.find_element_by_xpath('//*[@class="selectBtn1 btn btn-primary VAR3_BTN"]')
        driver.execute_script('arguments[0].click();',element)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="%s_check"]' % (spanId)).click()
        driver.execute_script('fnStnConfirm()')

        # 조회
        selectcnt=driver.find_element_by_xpath('//*[@id="schListCnt"]/option[1]').click() # 10개씩 뿌린다.
        driver.find_element_by_xpath('//*[@id="dsForm"]/div[3]/a/span').click()
        time.sleep(5)

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

        # 페이징 처리 시, 마지막 더하기
        if int(totCnt) % 10==0:
            plus_p=1
        else:
            plus_p=2

        ####### 페이지별, 다운로드
        for page in range(1,(int(totCnt)//10)+plus_p):
            print('########### ',str(page),'페이지 실행',' ###########')
            for i in range(1, 20, 2):
                # 다운로드 클릭
                try:
                    downloadClick(driver,i)
                except:
                    break
                # 다운로드창 Connetct
                connectYN = True
                tryCnt=1
                while (connectYN):
                    try:

                        app = pgmConnect()
                        connectYN = False
                    except:
                        connectYN = True
                        tryCnt += 1
                        pass

                print('시도횟수: %d' % (tryCnt))
                # 저장
                save(app=app,j=j)
                # 저장 확인
                saveCheck()

                j += 1
                if j % 8 == 0:
                    attr = 'wsd' # 풍속
                elif j % 8 ==1:
                    locCode += 1 # 지역 변경
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
            time.sleep(3)