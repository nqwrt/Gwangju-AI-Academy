# 넘파이 특징
# 1. 모든 원소가 같은 자료형이어야 한다.
# 2. 원소의 갯수를 바꿀수 없다.

import numpy as np

arr =  np.array([0, 1, 2, 3, 4])

# 넘파이 배열을 읽는 방법은 리스트의 인덱싱과 같음
print(arr[2])
print(arr[-1])
print(arr[-2])

print(arr.dtype)

# 리스트와 다른점은 무조건 데이터 타입을 맞추어야 업데이트가 됨
# arr[0] = int(7.6)
# print(arr)

arr =  np.array([
                    [0, 1, 2], 
                    [3, 4, 5]
                ])
#문제 
#1) 해당 배열의 차원을 출력하시오  (2, 3)
#2) 0 을 뽑아 내시오
#2) 5 을 뽑아 내시오

print(arr.shape)
print(arr[0][0])
print([0, 1, 2][0])
print([3, 4, 5][2],arr[-1][-1])

# 넘파이는 좌표 방식 접근도 지원
print(arr[0,0])

#슬라이싱
arr = np.array([10, 20, 30, 40, 50, 60, 70])
print("원본 배열:", arr)

#인덱스 1부터 3까지 (1부터 4사이)
print(arr[1:4])

# 인덱스 4부터 끝까지
print(arr[4:])

#처음부터 끝까지, 2칸씩 건너뛰기
print(arr[::2])

# 마지막 3개 원소
print(arr[-3:])

# 2차원 배열 슬라이싱
arr = np.array([
                    [0, 1, 2, 3], 
                    [4, 5, 6, 7]
                ])
print(arr.shape)

# 첫번째 행 전체
print(arr[0 ,:], arr[0][:] )

# 두번째 행 전체 [4 5 6 7]
print(arr[1,:], arr[1][:] )

# 두번째 열 전체 [1 5]
print(arr[:,1] )


# 두번째 행의 두번째 열부터 끝열까지[ 5 6 7]
print(arr[1,1:])