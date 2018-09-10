import pandas as pd
from collect import crawling_min as cm

class Simulator():

    def __init__(self):
        timeDic = cm.now()
        self.yyyy=timeDic['yyyy']
        self.mm = timeDic['mm']
        self.dd = timeDic['dd']
        self.hh = timeDic['hhmm'][0:2]
        self.ss = timeDic['hhmm'][2:4]

    def setData(self):
        # 2018-09-04 15:17
        time = self.yyyy+'-'+self.mm+'-'+self.dd+' '+self.hh+':'+self.ss

        # 데이터 로드
        df = pd.read_csv('../data/weatherByMin_%s.csv' % (self.yyyy+self.mm+self.dd))

        # 특정 시간대의 데이터 selection
        liveData = df.loc[ df['시간']==time,: ]
        print(liveData)
        return liveData

    def saveData(self, liveData):
        with open('../data/weatherLog_%s.csv' % (self.yyyy+self.mm+self.dd),
                  mode='a',
                  encoding='utf-8') as f:
            liveData.to_csv(f, header=False)

def main():
    simulator = Simulator()
    liveData = simulator.setData()
    simulator.saveData(liveData)