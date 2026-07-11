#pip install streamlit

import streamlit as st

st.title("Hello Streamlit")
st.header("Header")

st.markdown("# 제목")
st.markdown("**굵게**")

name = st.text_input("이름")
st.write(name)


if st.button("클릭"):
    st.write("버튼 클릭")

age = st.number_input("나이")


fruit = st.selectbox(
    "과일",
    ["사과","배","복숭아"]
)

gender = st.radio(
    "성별",
    ["남","여"]
)

agree = st.checkbox("동의")

value = st.slider(
    "숫자",
    0,
    100
)