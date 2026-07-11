# 입력 위젯 조합하기
import streamlit as st


st.title(
    "학생 정보 입력 프로그램"
)


name = st.text_input(
    "학생 이름"
)


student_id = st.text_input(
    "학번"
)


major = st.selectbox(
    "전공",
    [
        "컴퓨터공학",
        "전자공학",
        "경영학",
        "통계학"
    ]
)


grade = st.slider(
    "학년",
    1,
    10
)


python_level = st.radio(
    "Python 수준",
    [
        "초급",
        "중급",
        "고급"
    ]
)


skills = st.multiselect(
    "관심 분야",
    [
        "AI",
        "데이터분석",
        "웹",
        "앱"
    ]
)


if st.button("학생 정보 확인"):
    st.success("입력 완료")

    st.write(
        f"""
        이름 : {name}
        학번 : {student_id}
        전공 : {major}
        학년 : {grade}
        Python : {python_level}
        관심분야 : {skills}
        """
    )