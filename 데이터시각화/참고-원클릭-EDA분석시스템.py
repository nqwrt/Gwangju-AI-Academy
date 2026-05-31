import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Auto EDA Report", layout="wide")

st.title("📊 원클릭 EDA 자동 리포트")

# -----------------------------
# 파일 업로드
# -----------------------------
uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 데이터 미리보기")
    st.dataframe(df.head())

    # -----------------------------
    # 버튼 클릭
    # -----------------------------
    if st.button("🚀 EDA 리포트 생성"):

        # -----------------------------
        # 기본 정보
        # -----------------------------
        st.subheader("📌 기본 정보")

        col1, col2, col3 = st.columns(3)
        col1.metric("행 수", df.shape[0])
        col2.metric("열 수", df.shape[1])
        col3.metric("결측치", df.isnull().sum().sum())

        # -----------------------------
        # 데이터 타입
        # -----------------------------
        st.subheader("📊 데이터 타입")

        types = df.dtypes.astype(str)
        st.dataframe(types)

        # -----------------------------
        # 결측치 분석
        # -----------------------------
        st.subheader("❗ 결측치 분석")

        nulls = df.isnull().sum()
        nulls = nulls[nulls > 0]

        if len(nulls) > 0:
            fig_null = px.bar(nulls, title="Missing Values")
            st.plotly_chart(fig_null, use_container_width=True)
        else:
            st.success("결측치 없음")

        # -----------------------------
        # 수치형 분석
        # -----------------------------
        st.subheader("📈 수치형 데이터 분석")

        num_cols = df.select_dtypes(include=["int64", "float64"]).columns

        for col in num_cols:
            st.write(f"### {col}")

            col1, col2 = st.columns(2)

            with col1:
                fig = px.histogram(df, x=col)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.box(df, y=col)
                st.plotly_chart(fig, use_container_width=True)

        # -----------------------------
        # 범주형 분석
        # -----------------------------
        st.subheader("📊 범주형 데이터 분석")

        cat_cols = df.select_dtypes(include=["object"]).columns

        for col in cat_cols:
            st.write(f"### {col}")

            counts = df[col].value_counts().reset_index()
            counts.columns = [col, "count"]

            fig = px.bar(counts, x=col, y="count")
            st.plotly_chart(fig, use_container_width=True)

        # -----------------------------
        # 상관관계
        # -----------------------------
        st.subheader("🔥 상관관계 분석")

        if len(num_cols) > 1:
            corr = df[num_cols].corr()

            fig = px.imshow(corr, text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("수치형 컬럼 부족")

        # -----------------------------
        # 자동 인사이트
        # -----------------------------
        st.subheader("🧠 자동 인사이트")

        insights = []

        if df.isnull().sum().sum() > 0:
            insights.append("결측치 존재 → 전처리 필요")

        if len(num_cols) > 0:
            insights.append("수치형 데이터 존재 → 분포 확인 중요")

        if len(cat_cols) > 0:
            insights.append("범주형 데이터 존재 → 그룹 비교 가능")

        for i in insights:
            st.write(f"- {i}")