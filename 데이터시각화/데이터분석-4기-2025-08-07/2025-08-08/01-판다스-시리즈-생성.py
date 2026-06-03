# 차원 배열 구조 - Series : 1차원 배열
# 행번호 + 인덱스 + 데이타 3개의 변수를 기본적으로 가지고 있음
# 인덱스(index) 사용 가능 - 인덱싱/슬라이싱
# 데이터 타입을 가짐 (dtype)

import pandas as pd
import numpy as np

# numpy 배열로 시리즈 생성
arr = np.arange(100,105)
print(arr)

series = pd.Series(arr)
print(type(series)) #<class 'pandas.core.series.Series'>
print(series)
# 0    100
# 1    101
# 2    102
# 3    103
# 4    104
# dtype: int64

series = pd.Series(arr, dtype='float')
print(type(series)) #<class 'pandas.core.series.Series'>
print(series)

# 리스트로 생성
series = pd.Series([100,200,300,400])
print(type(series)) #<class 'pandas.core.series.Series'>
print(series)

series = pd.Series(['사과', '딸기', '포도', '수박', '참외'])
print(type(series)) # <class 'pandas.core.series.Series'>
print(series)


series = pd.Series([91, 3.14, '사과', 4, 77])
print(type(series)) # <class 'pandas.core.series.Series'>
print(series)

# 딕셔너리로 시리즈 생성
# a    100
# b    200
# c    300
# dtype: int64

data =  {'a': 100, 'b': 200, 'c': 300}
series = pd.Series(data)
print(series)