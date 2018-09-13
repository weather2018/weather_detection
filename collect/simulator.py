import pandas as pd

def setData(yyyy,mm,dd,hhss):
    # 2018-09-04 15:17
    time = yyyy+'-'+mm+'-'+dd+' '+hhss[0:2]+':'+hhss[2:4]

    # 데이터 로드
    df = pd.read_csv('../data/min/weatherByMin_%s.csv' % (yyyy+mm+dd))

    # 특정 시간대의 데이터 selection
    liveData = df.loc[ df['시간']==time,: ]
    # print(liveData)
    return liveData

def saveData(liveData):
    with open('../data/weatherLog.csv' ,
              mode='a',
              encoding='utf-8') as f:
        liveData.to_csv(f, header=False)

def main(yyyy,mm,dd,hhss):
    # simulator = Simulator()
    liveData = setData(yyyy,mm,dd,hhss)
    saveData(liveData)