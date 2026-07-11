import streamlit as st
import pandas as pd


st.title(
    "CSV 업로드 분석"
)


file = st.file_uploader(
    "CSV 파일 선택",
    type=["csv"]
)



if file:


    df = pd.read_csv(file)


    st.subheader(
        "데이터"
    )


    st.dataframe(df)


    st.subheader(
        "통계"
    )


    st.write(
        df.describe()
    )

############################
    st.title(
    "이미지 업로드"
)


image = st.file_uploader(
    "이미지 선택",
    type=[
        "png",
        "jpg",
        "jpeg"
    ]
)



if image:

    st.image(
        image,
        caption="업로드 이미지",
        use_container_width=True
    )