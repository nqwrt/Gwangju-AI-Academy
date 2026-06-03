# 넘파이 특징
# 1. 모든 원소가 같은 자료형이어야 한다.
# 2. 원소의 갯수를 바꿀수 없다.

import numpy as np

arr =  np.array([10, 20, 30, 40, 50])
print(arr)

# 30보다 큰 값만 뽑아 내시오.
# for value in arr:
    
#     if value > 30:
#         print(value)

# 그런데 넘파이 배열 에서는 for문을 돌리면 왕따 당함 
# for 문 안돌리려고 numpy 배열 쓰는 거임 ㅋㅋㅋ    

condition = arr > 30
print(condition) #[False False False  True  True]
result = arr[condition]
print(result) #[40 50]

print(arr[ arr >30])
arr =  np.array([10, 20, 30, 40, 50])
print(arr[ [False ,False, False , True , True] ])

# 조건 : 짝수만 선택
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(arr[arr % 2 == 0]) # [ 2  4  6  8 10]

# 1부터 1000까지의 배열을 만들고 그중에서 7의 배수이자 11의 배수인 숫자들만 뽑아내시오.
#[ 77 154 231 308 385 462 539 616 693 770 847 924]
arr = np.arange(1,1001)
#print(arr)

#NumPy 배열 연산에서는 | & (파이프 기호) 
#파이썬 기본 문법은 and or
print(arr[   (arr % 7  == 0) & (arr % 11  == 0)    ])

# 1부터 1000까지의 배열을 만들고 그중에서 7의 배수이거나 
# 또는 11의 배수인 숫자들만 뽑아내시오.
print(arr[   (arr % 7  == 0) | (arr % 11  == 0)    ])

# 1부터 1000까지의 배열에서 짝수이면서 100의 배수
# [ 100  200  300  400  500  600  700  800  900 1000]  
print(arr[   (arr % 2  == 0) & (arr % 100  == 0)    ])