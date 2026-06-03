import pandas as pd
import numpy as np

data = {
    '이름' : ['유재석', '박명수', '정준하', '노홍철', '정형돈', '하하'],
    '지역' : ['서울', '부산', '부산', '서울', '서울', '서울'],
    '전공' : ['문과', '이과', '이과', '이과', '문과', '문과'], 
    '나이' : [19, 23, 20, 25, 18, 21],
    '국어점수' : [86, 90, 80, 65, 50, 60],
    '수학점수' : [86, 100, 66, 70, 40, 80],
    '코딩' : ['Python', 'Java', np.nan, 'Javascript', 'PYTHON', np.nan]
}
df = pd.DataFrame(data, index=['1번', '2번', '3번', '4번', '5번', '6번'])
print(df)

# group by 는 sql 문법의 group by 와 유사함
# 같은 값을 하나로 묶어 통계 또는 집계 결과를 얻기 위해 사용하는 것

#        나이   국어점수  수학점수
# 지역
# 부산  21.50  85.00  83.0
# 서울  20.75  65.25  69.0
print(df.groupby("지역").mean(numeric_only=True))
print(df.groupby("지역")['국어점수'].mean(numeric_only=True))

#그룹을 여러개 지정도 가능
print(df.groupby(["지역","전공"]).mean(numeric_only=True))
#               나이       국어점수       수학점수
# 지역 전공
# 부산 이과  21.500000  85.000000  83.000000
# 서울 문과  19.333333  65.333333  68.666667
# 서울 이과  25.000000  65.000000  70.000000

print(df.groupby(["지역","전공"])['수학점수'].mean(numeric_only=True))

# 정렬
print(df.groupby("지역").mean(numeric_only=True).sort_values("국어점수"))
print(df.groupby("지역").mean(numeric_only=True).sort_values("국어점수",ascending=False))
print(df.groupby("지역").sum(numeric_only=True).sort_values("국어점수",ascending=False))

# 그룹함수는 반드시 아래의 함수만 같이 쓸수 있으며,
# 집계함수라 한다.

# sum()	합계
# mean()	평균
# median()	중앙값
# max()	최대값
# min()	최소값
# count()	값의 개수 (NaN 제외)
# size()	그룹별 전체 원소 수 (NaN 포함)
# std()	표준편차
# var()	분산
# first()	첫 번째 값
# last()	마지막 값
# nunique()	고유값 개수
# agg()	여러 집계 함수를 한 번에 적용할 때 사용

#     코딩  이름
# 지역
# 부산   1   2
# 서울   3   4
print(df.groupby("지역")[['코딩',"이름"]].count())