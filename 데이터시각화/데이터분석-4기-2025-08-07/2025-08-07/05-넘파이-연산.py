# 넘파이 연산
# 행렬 연산을 기반으로 함

import numpy as np

arr1 = np.array([
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]
                ])

arr2 = np.array([
                    [2, 2, 2],
                    [2, 2, 2],
                    [2, 2, 2]]
                )

# [[ 3  4  5] 
#  [ 6  7  8] 
#  [ 9 10 11]]
print(arr1 + arr2)
print(arr1.__add__(arr2))
print(np.add(arr1,arr2))

print(arr1 - arr2)
print(np.subtract(arr1,arr2))

print(arr1 * arr2)
print(np.multiply(arr1,arr2))

print(arr1 / arr2)
print(np.divide(arr1,arr2))

#스칼라(상수) 와의 곱
print(3 * arr1)
print(3 + arr1)

print(arr2 ** 3)
print(np.sqrt(arr2))

# 몫과 나머지
print( arr2 // 2)
print( arr2 % 2)