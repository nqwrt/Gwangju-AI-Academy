import pandas as pd
import matplotlib.pyplot as plt


# CSV 읽기
# 
def load_csv(path):
    
    df = pd.read_csv(path)
    df = convert_datetime_columns(df)
    
    return df


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

# 날짜 타입 자동 탐색
# 컬럼명이 "날짜"가 아닐 수도 있으므로:
def convert_datetime_columns(df):

    for col in df.columns:

        try:
            
            # 이미 숫자면 제외
            if pd.api.types.is_numeric_dtype(df[col]):
                continue

            converted = pd.to_datetime(
                df[col],
                errors="coerce"
            )

            # 변환 가능한 값 비율 확인
            ratio = converted.notna().mean()


            if ratio > 0.8:
                df[col] = converted
                print( f"날짜 변환 완료: {col}" )

        except:
            pass

    return df