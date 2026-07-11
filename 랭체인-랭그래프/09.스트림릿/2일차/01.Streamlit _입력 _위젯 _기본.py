# 사용자 입력 받기
# Widget 값 저장
# 입력 결과 출력

import streamlit as st


st.title("Streamlit 입력 위젯")


# 텍스트 입력
name = st.text_input(
    "이름 입력"
)


# 숫자 입력
age = st.number_input(
    "나이",
    min_value=0,
    max_value=100,
    value=20
)


# 선택 박스

job = st.selectbox(
    "직업 선택",
    [
        "학생",
        "개발자",
        "디자이너",
        "회사원"
    ]
)


# 여러 선택

hobby = st.multiselect(
    "취미 선택",
    [
        "운동",
        "독서",
        "게임",
        "여행"
    ]
)


# 라디오

gender = st.radio(
    "성별",
    [
        "남자",
        "여자"
    ]
)


# 체크박스

agree = st.checkbox(
    "개인정보 수집 동의"
)


# 슬라이더

score = st.slider(
    "점수",
    0,
    100,
    50
)


# 날짜

date = st.date_input(
    "생년월일"
)


# 시간

time = st.time_input(
    "출근 시간"
)



st.divider()


st.write("이름 :", name)
st.write("나이 :", age)
st.write("직업 :", job)
st.write("취미 :", hobby)
st.write("성별 :", gender)
st.write("동의 :", agree)
st.write("점수 :", score)
st.write("날짜 :", date)
st.write("시간 :", time)