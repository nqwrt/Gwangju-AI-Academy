# 결측치란 데이터에서 누락된 값 또는 빠진 값을 말합니다.
# 결측치가 문제가 되는 이유
# 통계 분석이나 머신러닝 모델에서 왜곡된 결과를 초래할 수 있음

import pandas as pd
import numpy as np

data = {
    '이름' : ['유재석', '박명수', '정준하', '노홍철', '정형돈', '하하'],
    '지역' : ['서울', '부산', np.nan, '서울', '서울', '서울'],
    '나이' : [19, 23, 20, 25, 18, 21],
    '국어점수' : [86, 90, 80, 65, 50, 60],
    '수학점수' : [86, 100, 66, 70, 40, 80],
    '코딩' : ['Python', 'Java', np.nan, 'Javascript', 'PYTHON', np.nan]
}
df = pd.DataFrame(data, index=['1번', '2번', '3번', '4번', '5번', '6번'])
print(df)

# 데이터프레임의 '지역' 컬럼 내 데이터들을 모두 결측치로 지정
#df['지역'] =  np.nan
#print(df)

# fillna 를 통해 결측치 값을 바꿈
#df.fillna('없음', inplace=True)
#print(df)

# 특정 열지정하여 처리하기
# df['코딩'].fillna('없음',inplace=True)
# print(df)

# 삭제
# NaN 을 가진 모든 행 삭제
# 결측치가 하나라도 있는 행을 삭제합니다.
#df.dropna(inplace=True)
#print(df)

#NaN가 하나라도 있는 row 삭제
#df.dropna(axis='index', how='any',inplace=True)
#print(df)

 #NaN가 하나라도 있는 컬럼 삭제
#df.dropna(axis='columns', how='any',inplace=True)
#print(df)

# 결측치 체크함수
print(df.isnull())
print(df.isnull().sum())

# | 데이터 상태   | 추천       |
# | -------- | -------- |
# | 정규분포(대칭) | 평균       |
# | 이상치 많음   | 중앙값 ← 추천 | # 이유는 평균을 쓰면 이상치의 영향을 크게 받음
# | 범주형      | 최빈값      |
# | 시계열      | 앞값/뒤값    |


