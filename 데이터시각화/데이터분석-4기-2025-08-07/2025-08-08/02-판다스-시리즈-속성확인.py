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

# 속성 확인
#Index(['사과', '딸기', '키위', '메론'], dtype='object')
print(series.index)
print(series.values)

print(series.dtype)
print(series.shape)# (4,)
print(series.size)