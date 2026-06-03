# 차원 배열 구조 - Series : 1차원 배열
# 행번호 + 인덱스 + 데이타 3개의 변수를 기본적으로 가지고 있음
# 인덱스(index) 사용 가능 - 인덱싱/슬라이싱
# 데이터 타입을 가짐 (dtype)

import pandas as pd
import numpy as np

#딕셔너리로 생성시 자동으로 키가 시리즈의 인덱스로 들어감
series = pd.Series({'사과': 1200, '딸기': 3500, '키위': 2100, '메론': 9600})
print(series)
# 사과    1200
# 딸기    3500
# 키위    2100
# 메론    9600
# dtype: int64

series.name = "과일가격"
print(series)

#인덱스 수정
#인덱스 수정은 전체 수정 가능 , 일부 수정 불가
# series.index[0] ='오렌지'
series.index = ['오렌지', '딸기', '키위', '메론']
print(series)

# 인덱스 삭제
# 인덱스 삭제는 불가능 하며, 초기화 가능
series = series.reset_index(drop=True)
print(series)