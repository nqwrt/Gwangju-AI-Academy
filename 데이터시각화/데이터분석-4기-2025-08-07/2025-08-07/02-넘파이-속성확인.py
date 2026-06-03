# 넘파이 특징
# 1. 모든 원소가 같은 자료형이어야 한다.
# 2. 원소의 갯수를 바꿀수 없다.

import numpy as np

arr = np.random.randint(10, size = (3, 4, 5), dtype = 'int8') 
print(arr)

print(dir(arr))
# 3
# (3, 4, 5)
# 60
# int8
print(arr.ndim)
# shape
print(arr.shape)
print(arr.size)
print(arr.dtype)
