import pandas as pd

data = [
    ["005930", "삼성전자", 66500],
    ["035720", "카카오", 80600],
    ["005380", "현대차", 185000]
]
columns = ["종목코드", "종목명", "현재가"]
df = pd.DataFrame(data=data, columns=columns)
df.set_index('종목코드', inplace=True)
df

df.to_csv("kospi.csv")
df.to_excel("kospi.xlsx")

import pandas as pd

df2 = pd.read_csv("kospi.csv", dtype={'종목코드': str})
df2

#종목코드 컬럼을 인덱스로 변경하기 위하여 set_index 메서드를 호출
df2.set_index("종목코드", inplace=True)

df3 = pd.read_excel("kospi.xlsx", dtype={'종목코드': str})
print(df3)