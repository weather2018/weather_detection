import json
import sys
import pandas as pd
import requests
from datetime import *

# 전역 변수
accident_data = './data/traffic_accident_2017.csv'
location_data = './data/location_mst.csv'
APP_KEY = '8467d36f8b78d0708f3cc6441f8cd174'
URL = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json'

# json 데이터 요청
def json_request(url='', encoding='utf-8', success=None, error=lambda e: print('%s : %s' % (e, datetime.now()), file=sys.stderr)):
    headers = {'Authorization': 'KakaoAK {}'.format(APP_KEY)}
    resp = requests.get(url, headers=headers)
    print('%s : success for request [%s]' % (datetime.now(), url))

    return resp.text

# json 데이터 파싱해서 행정동 주소 반환
def reverse_geocode(longitude, latitude):
    # 파라미터 최적화하여 url 생성
    url = '%s?x=%s&y=%s' %(URL, longitude, latitude)

    # json request
    try:
        json_req = json_request(url=url)
        json_data = json.loads(json_req)
        json_doc = json_data.get('documents')[1]
        json_name = json_doc.get('region_3depth_name')
    except:
        json_name = 'NaN'

    return json_name

# 교통사고 파일에서 경위도 추출해서 동 주소 반환
def get_address(data):
    address = []

    # 경도, 위도 추출해서 동 주소 반환
    for i in range(len(data)):
        longitude = data['경도'][i]
        latitude = data['위도'][i]
        address.append(reverse_geocode(longitude, latitude))

    return address

def preprocess(data, address, location):
    # column 추가
    data['DONG'] = address

    # 발생 년월일시 재조정
    data['YYYYMM'] = data['발생년월일시'].astype(str).str[:6]
    data['DD'] = data['발생년월일시'].astype(str).str[6:8]
    data['HH'] = data['발생년월일시'].astype(str).str[8:]

    # 필요없는 데이터 삭제
    features = ['발생년월일시', '발생년', '발생분', '사고유형_대분류', '사고유형_중분류', '사고유형', '법규위반_대분류', '법규위반', '도로형태_대분류', '도로형태', '당사자종별_1당_대분류', '당사자종별_1당', '당사자종별_2당_대분류', '당사자종별_2당', '발생위치X_UTMK', '발생위치Y_UTMK']
    for feature in features:
        del data[feature]

    # header 영어로 변경
    hangul_header = ['요일', '주야', '발생지시도', '발생지시군구', '경도', '위도', '부상신고자수', '경상자수', '중상자수', '사망자수', '사상자수']
    eng_header = ['DAY', 'DAYNIGHT', 'SIDO', 'SIGUNGU', 'LON', 'LAT', 'CAS1', 'CAS2', 'CAS3', 'KD', 'CAS_TOTAL']
    for i in range(len(hangul_header)):
        data.rename(columns={hangul_header[i]:eng_header[i]}, inplace=True)

    # 동을 코드로 변환
    location.rename(columns={'NAME': 'DONG'}, inplace=True)
    df_merge = pd.merge(data, location, how='left', on='DONG')

    # colume 정렬
    output = pd.DataFrame(df_merge, columns=['DD', 'HH', 'YYYYMM', 'DAY', 'DAYNIGHT', 'SIDO', 'SIGUNGU', 'DONG', 'CODE', 'LON', 'LAT', 'CAS1', 'CAS2', 'CAS3', 'KD', 'CAS_TOTAL'])

    # 기존의 행 인덱스 제거
    output = output.set_index('DD')

    return output

def main():
    # 파일 읽기
    data = pd.read_csv(accident_data, encoding='euc-kr')
    location = pd.read_csv(location_data, encoding='euc-kr')

    address = get_address(data)
    data = preprocess(data, address, location)

    # 최종 파일 저장
    data.to_csv('%s_final.csv' % (accident_data[:-4]), sep=',', encoding='euc-kr')

if __name__ == '__main__':
    main()