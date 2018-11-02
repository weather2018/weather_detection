import pandas as pd

def dataLoad(year,attr,locCode,dateMst):
    # 데이터 로드
    df = pd.read_csv('../data/Y%d/%d_C%s_%s.csv' % (year,year,str(locCode).zfill(4), attr))
    # 데이터 전처리
    df = preProcess(df=df, year=year, dateMst=dateMst, attr=attr, locCode=locCode)
    return df

def preProcess(df,year,locCode, dateMst,attr):
    # 컬럼명 지정
    df.columns = (['DD', 'HH',attr])
    # Start가 들어 있는 row 삭제
    df = df[df['DD'].astype(str).str.contains('Start')==False]
    # 인덱스 reset
    df=df.reset_index(drop=True)
    # 컬럼 추가
    df['YYYYMM'] = dateMst['Y'+str(year)].replace('-','',regex=True).astype(str).str[:6]
    df['LOCATION'] = 'C' + str(locCode).zfill(4)
    # 컬럼 포멧 재처리
    df['DD'] = df['DD'].replace(' ','',regex=True).astype(str).str.zfill(2)
    df['HH'] = df['HH'].replace(' ','',regex=True).astype(str).str.zfill(6).str[:2]
    return df

def main(year):
    pty = pd.DataFrame()
    reh = pd.DataFrame()
    rn1 = None
    sky = None
    t1h = None
    lgt = None
    vec = None
    wsd = None
    for locCode in range(1,3504):
        # 데이터 로드 & 전처리
        for attr in ['pty','reh','rn1','sky','t1h','lgt','vec','wsd']:
            if attr == 'pty':
                pty = dataLoad(year=year, attr=attr, locCode=locCode, dateMst=dateMst)
            elif attr =='reh':
                reh = dataLoad(year=year, attr=attr, locCode=locCode, dateMst=dateMst)
            elif attr =='rn1':
                rn1 = dataLoad(year=year, attr=attr, locCode=locCode, dateMst=dateMst)
            elif attr =='sky':
                sky = dataLoad(year=year, attr=attr, locCode=locCode, dateMst=dateMst)
            elif attr =='t1h':
                t1h = dataLoad(year=year, attr=attr, locCode=locCode, dateMst=dateMst)
            elif attr =='lgt':
                lgt = dataLoad(year=year, attr=attr, locCode=locCode, dateMst=dateMst)
            elif attr =='vec':
                vec = dataLoad(year=year, attr=attr, locCode=locCode, dateMst=dateMst)
            elif attr =='wsd':
                wsd = dataLoad(year=year, attr=attr, locCode=locCode, dateMst=dateMst)

        # 데이터 조인
        tmpTable = pd.merge(pty,reh).merge(rn1).merge(sky).merge(t1h).merge(lgt).merge(vec).merge(wsd)
        tmpCnt=tmpTable.YYYYMM.count()
        # print(tmpTable)

        if(dateCnt==tmpCnt):
            tmpTable.to_csv(
                '../data/Y%d/%d_weather.csv' % (year,year),
                encoding='utf-8',
                mode='a',
                index=False
            )
            print('년: %d, 지역: C%s, 건수: %d 적재 성공' % (year, str(locCode).zfill(4),tmpCnt))
        else:
            print('데이터누락이 발생!')
            break

for year in range(2015,2016):
    dateMst = pd.read_csv('../data/yyyymmdd.csv')
    dateCnt = dateMst.Y2015.count()
    main(year=year)


