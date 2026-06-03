# 2차원 데이타 구조
# excel 문서의 시트와 유사
# 행 과 열로 구성
# 각 열별로 데이타 타입을 가짐
# 시리즈 + 컬럼

import pandas as pd
import numpy as np

#    0  1  2
# 0  1  2  3
# 1  4  5  6
# 2  7  8  9

# 리스트를 통한 생성
df = pd.DataFrame([
    [1,2,3],
    [4,5,6],
    [7,8,9],    
])

print(df)

# 넘파이를 통한 생성
df = pd.DataFrame(np.array([
    [1,2,3],
    [4,5,6],
    [7,8,9],    
]))

print(df)


#    가  나  다
# a  1  2  3
# b  4  5  6
# c  7  8  9

df = pd.DataFrame(np.array([
    [1,2,3],
    [4,5,6],
    [7,8,9],    
]) , columns=['가','나','다'], index=['a','b','c'])


print(df)

# 딕셔너리를 통한 생성
data = {
    '이름': ['김철수', '이영희', '홍길동'], 
    '학교': ['서울고', '대전고', '경기고'], 
    '점수': [80, 95, 85]
}

#     이름   학교  점수
# 0  김철수  서울고  80
# 1  이영희  대전고  95
# 2  홍길동  경기고  85
df = pd.DataFrame(data)
print(df)

# 데이타 프레임 속성확인
print(df.index)
print(df.columns)
print(df.values)

print(df.shape) #(3, 3)

#인덱스 수정(단독 수정 불가)
df.index = ['1번','2번','3번']
print(df)

#컬럼 이름 변경
df = df.rename(columns={'이름':'name','점수':'score'})
print(df)

# 컬럼가져오기 - 기본형(loc, iloc 함수 사용 안하고)

# 1번    김철수
# 2번    이영희
# 3번    홍길동
# Name: name, dtype: object
print(df['name']) # 리턴값이 시리즈
print(df[['name']]) # 리턴값이 데이타 프레임

# 두개 이상 컬럼 가져오기
print(df[['name','score']]) 
#      이름  점수
# 1번  김철수  80
# 2번  이영희  95
# 3번  홍길동  85
