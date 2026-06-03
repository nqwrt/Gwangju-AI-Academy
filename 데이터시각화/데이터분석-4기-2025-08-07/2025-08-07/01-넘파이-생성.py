# 넘파이 특징
# 1. 모든 원소가 같은 자료형이어야 한다.
# 2. 원소의 갯수를 바꿀수 없다.

import numpy as np

#CRUD
#리스트에서 배열(numpy) 만들기
arr = np.array( [1,4,2,4,3] )
print(arr) #[1 4 2 4 3]
print(type(arr)) #넘파이 배열
#print(dir(arr))
#print([1,4,2,4,3])

# 모든 원소가 같은 자료형으로 통일 시킴
arr = np.array([3.14 , "안녕" , 2 , 4 , 3])
print(arr) # ['3.14' '안녕' '2' '4' '3']
print(type(arr)) 

# 모든 원소가 같은 자료형으로 통일 시킴
arr = np.array([3.14 , 3 , 2 , 4 , 3])
print(arr) #[3.14 3.   2.   4.   3.  ]
print(type(arr)) 

# 넘파이에서는 데이타 타입을 지정해 줄수 있음
arr = np.array( [2 , 4 , 3], dtype='int32')
print(arr)
print(type(arr))


# 함수를 통한 배열 생성
# 0 으로 채운 배열 생성
arr = np.zeros(10, dtype=int)
print(arr)

# 선형대수 
# 넘파이는 스칼라 벡터 매트릭스의 개념을 가짐
# 1. 스칼라 (Scalar)
# 예시: 3, -1.5, π, 0 등
# 단순한 숫자


# 벡터 (Vector)
# 크기와 방향이 있는 값의 집합. 즉, 숫자의 나열.
# 1차원 배열 [수의 나열]

# 메트릭스
# 2차원 배열이상 : 수의 배열 (행×열)


# 2차원 배열
arr = np.ones( (3,5) , dtype=int)
print(arr)
# [
#   [1 1 1 1 1]
#   [1 1 1 1 1]
#   [1 1 1 1 1]
# ]

# 3차원 이상 
# 3 높이 5 행 2열
arr = np.full( (3,5,2) , 3.14)
print(arr)

# [[[3.14 3.14]
#   [3.14 3.14]
#   [3.14 3.14]
#   [3.14 3.14]
#   [3.14 3.14]]

#  [[3.14 3.14]
#   [3.14 3.14]
#   [3.14 3.14]
#   [3.14 3.14]
#   [3.14 3.14]]

#  [[3.14 3.14]
#   [3.14 3.14]
#   [3.14 3.14]
#   [3.14 3.14]
#   [3.14 3.14]]]

# arrange 함수 사용하기 
# 파이썬 기본함수 range 함수와 유사
#[ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19]
arr = np.arange(0, 20) 
print(arr)

# 0에서 시작해 2씩 더해 20까지 채우는 배열 생성
#[ 0  2  4  6  8 10 12 14 16 18]
arr = np.arange(0, 20, 2) 
print(arr)

# 0과 1 사이에 일정한 간격을 가진 다섯 개의 값으로 채운 배열 만들기
# [0.   0.25 0.5  0.75 1.  ]
arr = np.linspace(0,1,5)
print(arr)

# 랜덤함수로 배열생성
# 0 과 1 사이의 숫자중에 실수 난수
arr = np.random.random((3,3))
print(arr)

# 1부터 10사이
arr = np.random.randint(1,10,(3,3))
print(arr)

# 로또 번호 6개를 넘파이 배열로 뽑아내시오.
# replace=False 
# 중복 없이

lotto = np.random.choice(np.arange(1, 46), size=6, replace=False)
print(lotto)

# 평균 0, 표준 편차 1의 정규 분포를 따르는 3*3 난수 배열
arr = np.random.normal(0, 1, (3, 3))
print(arr)



# import numpy as np
# import matplotlib.pyplot as plt

# # 3x3 정규분포 난수 배열 생성
# arr = np.random.normal(0, 1, (3, 3))
# print(arr)

# plt.hist(arr, bins=5,  edgecolor='black')

# plt.title('Histogram of 3x3 Normal Distribution Samples')
# plt.xlabel('Value')
# plt.ylabel('Frequency')
# plt.show()