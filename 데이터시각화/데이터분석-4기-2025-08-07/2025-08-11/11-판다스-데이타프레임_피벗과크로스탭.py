import pandas as pd

df = pd.DataFrame({
    "학생":["철수","철수","영희","영희"],
    "과목":["수학","영어","수학","영어"],
    "점수":[90,80,95,85]
})

print(df)

result = df.pivot(
    index="학생",
    columns="과목",
    values="점수"
)

print(result)

df = pd.DataFrame({
    "성별":["남","남","여","여","남"],
    "합격":["O","X","O","O","X"]
})

print(df)

cross_tab = pd.crosstab(
    df["성별"], # 행은 성별
    df["합격"] # 열은 합격
)

# 행 → 성별
# 열 → 합격

#         O   X
# 남      1   2
# 여      2   0
print(cross_tab)

# https://wikidocs.net/216695


data = {
    'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'],
    'Education': ['High School', 'College', 'College', 'High School', 'Graduate'],
    'Age': [25, 30, 22, 35, 28]
}
df = pd.DataFrame(data)

count = pd.crosstab(df['Gender'], df['Education'], margins=True, margins_name='Total')
print(count)

# Education  College  Graduate  High School  Total
# Gender                                          
# Female           1         0            1      2
# Male             1         1            1      3
# Total            2         1            2      5