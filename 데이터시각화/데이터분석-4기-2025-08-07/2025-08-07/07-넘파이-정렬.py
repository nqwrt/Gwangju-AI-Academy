# 넘파이 정렬

import numpy as np

arr = np.random.randint(10,size=10)
# print(arr)
# #[8 4 6 0 0 1 8 2 1 9]

# 원본을 바꿈 => arr.sort()
# print(arr.sort()) #None
# #[0 0 1 1 2 4 6 8 8 9]
# print(arr)

# 원본에 영향을 주지 않는다.
print(np.sort(arr)) #[0 0 2 3 3 4 4 5 5 6]
arr = np.sort(arr)
print(arr) #[6 5 3 0 4 4 5 2 3 0]

#내림 차순
print(np.sort(arr)[::-1])  #원래 배열에 영향을 주지 못함
arr = np.sort(arr)[::-1]  #원래 배열까지 바꿀 수 있음
print(arr)

# 2차원 배열

np.random.seed(42)
# [[10 11  3  5]
#  [11  5  7  8]
#  [11 11  8  1]]
arr = np.random.randint(15,size=(3,4))
print(arr)
# [[ 6  3 12 14]
#  [10  7 12  4]
#  [ 6  9  2  6]]

#행단위 정렬
print(np.sort(arr,axis=1))
# [[ 3  6 12 14]
#  [ 4  7 10 12]
#  [ 2  6  6  9]]

#열단위로 정렬
print(np.sort(arr,axis=0))
# [
#    [ 6  3  2  4],
#    [ 6  7 12  6],
#    [10  9 12 14]
# ]
