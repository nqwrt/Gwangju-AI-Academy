# 2차원 데이타 구조
# excel 문서의 시트와 유사
# 행 과 열로 구성
# 각 열별로 데이타 타입을 가짐
# 시리즈 + 컬럼

import pandas as pd
import numpy as np


# 딕셔너리를 통한 생성
data = {
    '이름': ['김철수', '이영희', '홍길동'], 
    '학교': ['서울고', '대전고', '경기고'], 
    '점수': [80, 95, 85]
}

df = pd.DataFrame(data)
print(df)


# 인덱스 수정
df.index = ['1번', '2번', '3번']
print(df)


# 인덱스 이름 설정
df.index.name = '번호'
print(df)

#인덱스 초기화
df.reset_index(inplace=True)
print(df)

#인덱스 설정(특정 컬럼을 인덱스로 변경)
df.set_index('이름',inplace=True)
print(df)

# 인덱스 정렬
df.sort_index(inplace=True)
print(df)

df.sort_index(ascending=False, inplace=True)
print(df)
