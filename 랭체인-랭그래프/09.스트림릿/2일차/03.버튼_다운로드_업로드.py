import streamlit as st


st.title(
    "Button 실습"
)



if st.button("클릭"):

    st.success(
        "버튼 클릭!"
    )



text = """
Streamlit 다운로드 테스트
"""


st.download_button(
    label="파일 다운로드",
    data=text,
    file_name="test.txt"
)

file = st.file_uploader(
    "파일 업로드"
)

if file:
    st.write(
        "파일명:",
        file.name
    )