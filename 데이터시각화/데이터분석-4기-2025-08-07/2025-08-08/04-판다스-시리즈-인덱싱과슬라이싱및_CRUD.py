# 차원 배열 구조 - Series : 1차원 배열
# 행번호 + 인덱스 + 데이타 3개의 변수를 기본적으로 가지고 있음
# 인덱스(index) 사용 가능 - 인덱싱/슬라이싱
# 데이터 타입을 가짐 (dtype)

import pandas as pd
import numpy as np

series = pd.Series({'사과': 1200, '딸기': 3500, '키위': 2100, '메론': 9600})
print(series)
# 사과    1200
# 딸기    3500
# 키위    2100
# 메론    9600
# dtype: int64

# 단일값 접근
print(series['사과'])
#1200

print(series[ ['사과'] ]) #결과 값이 시리즈 타입(객채)으로 리턴 됨
# 사과    1200
# dtype: int64

#여러값 접근(두개이상)
print(series[ ['사과','딸기','키위'] ])
# print(series[ '사과','딸기','키위' ]) => 에러발생

# 과일 중에 2100 초과 한 과일을 시리즈로 뽑아 내시오.
# 조건 필터링을 통한 접근(불린 인덱싱) => 시리즈도 넘파이 처럼 불린인덱싱이 지원됨
print(series[ series > 2100 ])

# 사과    1200
# 딸기    3500
# 키위    2100
# 메론    9600

# 행번호 인덱싱
print(series[1:3])
print(series[0]) # 단일 값 가져오는걸 확인
print(series[:])

# 인덱스기반 인덱싱
print(series['사과':'메론'])
print(series['사과':'딸기'])

# loc 함수(인덱스)와 iloc(행번호) 함수 활용
print(series.loc['사과':'딸기'])
print(series.loc['사과':'메론'])

#iloc 함수 활용 i = integer
print(series.iloc[0:3])
print(series.iloc[1:3])

#특정 위치에 있는 값 가져오기
print(series.iloc[0])
print(series.iloc[-1])

# 시리즈에서 추가
series.loc['바나나'] = 5000
print(series)

# 없으면 추가 , 있으면 업데이트 
series.loc["바나나"] = 7000
print(series)

# 행번호로 업데이트 
series.iloc[-1] = 9000
print(series)

# 삭제 
#series = series.drop('사과')
series.drop('사과', inplace=True)
print(series)

series.drop(['딸기','바나나'], inplace=True)
print(series)


