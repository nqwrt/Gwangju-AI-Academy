import pandas as pd
import matplotlib.pyplot as plt


# CSV 읽기
def load_csv(path):
    return pd.read_csv(path)


# EDA
def run_eda(df):

    result = []

    result.append("===== HEAD =====")
    result.append(df.head())

    result.append("\n===== INFO =====")
    df.info()

    result.append("\n===== DESCRIBE =====")
    result.append(df.describe(include="all"))

    return str(result)


# 코드 실행
def execute_python(df, code):
    local_scope = {
        "df": df,
        "pd": pd,
        "plt": plt
    }

    exec(code, {}, local_scope)

    return local_scope.get("result", "실행 완료")