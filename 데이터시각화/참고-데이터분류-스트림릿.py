import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

# -----------------------------
# 데이터 타입 분류
# -----------------------------
def classify_column(df, col):
    if pd.api.types.is_numeric_dtype(df[col]):
        unique_ratio = df[col].nunique() / len(df)
        if unique_ratio < 0.05:
            return "이산형"
        else:
            return "연속형"
    else:
        return "범주형"

# -----------------------------
# 그래프 추천
# -----------------------------
def recommend_plot(type1, type2=None):
    if type2 is None:
        if type1 == "연속형":
            return "histogram"
        else:
            return "bar"
    else:
        if type1 == "연속형" and type2 == "연속형":
            return "scatter"
        else:
            return "box"

# -----------------------------
# 앱 시작
# -----------------------------
st.set_page_config(page_title="Auto Data Viz", layout="wide")

st.title("📊 자동 데이터 시각화 시스템")

# -----------------------------
# 데이터 선택
# -----------------------------
data_option = st.selectbox(
    "데이터 선택",
    ["Iris", "Titanic", "Tips"]
)

if data_option == "Iris":
    df = sns.load_dataset("iris")
elif data_option == "Titanic":
    df = sns.load_dataset("titanic")
else:
    df = sns.load_dataset("tips")

st.write("데이터 미리보기")
st.dataframe(df.head())

# -----------------------------
# 컬럼 선택
# -----------------------------
col1 = st.selectbox("X축 선택", df.columns)
col2 = st.selectbox("Y축 선택 (선택)", ["None"] + list(df.columns))

# -----------------------------
# 타입 분석
# -----------------------------
type1 = classify_column(df, col1)

if col2 != "None":
    type2 = classify_column(df, col2)
    plot_type = recommend_plot(type1, type2)
else:
    plot_type = recommend_plot(type1)

# -----------------------------
# 그래프 출력
# -----------------------------
st.subheader("📊 자동 생성 그래프")

if col2 == "None":
    if plot_type == "histogram":
        fig = px.histogram(df, x=col1)
    else:
        fig = px.histogram(df, x=col1)

else:
    if plot_type == "scatter":
        fig = px.scatter(df, x=col1, y=col2)
    else:
        fig = px.box(df, x=col1, y=col2)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 설명
# -----------------------------
st.subheader("🧠 분석 결과")

if col2 == "None":
    st.write(f"{col1} → {type1} → {plot_type} 선택됨")
else:
    st.write(f"{col1} ({type1}) vs {col2} ({type2}) → {plot_type}")