# | 구분    | Session     | Cache          |
# | ----- | ----------- | -------------- |
# | 목적    | 사용자 상태 유지   | 작업 결과 재사용      |
# | 기준    | 사용자별        | 앱/서버 기준        |
# | 저장 내용 | 로그인 정보, 입력값 | 데이터, 모델, 계산 결과 |
# | 공유    | 사용자마다 다름    | 여러 사용자가 공유 가능  |
# | 변경 주체 | 사용자 행동      | 프로그램 실행        |
# | 예     | 로그인 상태      | AI 모델          |


import streamlit as st
import time


# =====================================================
# 페이지 설정
# =====================================================

st.set_page_config(
    page_title="Streamlit Day3",
    layout="wide"
)


# =====================================================
# Session State 초기화
# =====================================================

if "count" not in st.session_state:
    st.session_state.count = 0


if "login" not in st.session_state:
    st.session_state.login = False


if "username" not in st.session_state:
    st.session_state.username = ""


if "memo" not in st.session_state:
    st.session_state.memo = ""


# =====================================================
# Sidebar
# =====================================================

st.sidebar.title("메뉴")


menu = st.sidebar.radio(
    "페이지 선택",
    [
        "카운터",
        "로그인",
        "Cache",
        "메모장"
    ]
)


st.sidebar.divider()

st.sidebar.write(
    "현재 상태"
)

st.sidebar.write(
    st.session_state
)



# =====================================================
# Tab 예제
# =====================================================

tab1, tab2 = st.tabs(
    [
        "설명",
        "실습"
    ]
)


with tab1:

    st.title("Streamlit Day3")

    st.write(
        """
        오늘 학습 내용

        - Session State
        - Sidebar
        - Tabs
        - Spinner
        - Progress
        - Cache
        """
    )


with tab2:

    st.write(
        "실습 화면"
    )



# =====================================================
# 1. Counter
# =====================================================


if menu == "카운터":

    st.header("🔢 Session State 카운터")


    st.write(
        "현재 값:",
        st.session_state.count
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        if st.button("+ 증가"):

            st.session_state.count += 1


    with col2:

        if st.button("- 감소"):

            st.session_state.count -= 1


    with col3:

        if st.button("Reset"):

            st.session_state.count = 0



    st.info(
        """
        버튼 클릭 시 Streamlit은 전체 코드를 다시 실행합니다.

        일반 변수:

        count = 0

        -> 매번 초기화됨


        session_state:

        st.session_state.count

        -> 값을 유지함
        """
    )



# =====================================================
# 2. Login
# =====================================================


elif menu == "로그인":

    st.header("🔐 로그인 화면")


    if not st.session_state.login:


        username = st.text_input(
            "아이디"
        )


        password = st.text_input(
            "비밀번호",
            type="password"
        )


        if st.button("로그인"):


            if username == "admin" and password == "1234":


                st.session_state.login = True

                st.session_state.username = username

                st.success(
                    "로그인 성공"
                )


                st.rerun()


            else:

                st.error(
                    "아이디 또는 비밀번호 오류"
                )



    else:


        st.success(
            f"{st.session_state.username}님 환영합니다."
        )


        if st.button("로그아웃"):


            st.session_state.login = False

            st.session_state.username = ""

            st.rerun()



# =====================================================
# 3. Cache
# =====================================================


elif menu == "Cache":


    st.header("🚀 Cache 실습")


    @st.cache_data
    def slow_function(number):

        time.sleep(3)

        return number * number



    @st.cache_resource
    def create_model():

        time.sleep(3)

        return {
            "model":"AI Model"
        }




    number = st.number_input(
        "숫자 입력",
        value=10
    )


    start = time.time()


    result = slow_function(number)


    end = time.time()


    st.write(
        "결과:",
        result
    )


    st.write(
        "실행시간:",
        round(end-start,3),
        "초"
    )



    st.divider()


    model = create_model()


    st.write(
        "Resource Cache:",
        model
    )



    st.info(
        """
        @st.cache_data

        - 데이터 처리 결과 저장
        - CSV 읽기
        - API 결과


        @st.cache_resource

        - 모델 객체 저장
        - DB Connection
        - 머신러닝 모델
        """
    )



# =====================================================
# 4. Memo
# =====================================================


elif menu == "메모장":


    st.header("📝 Streamlit 메모장")


    memo = st.text_area(
        "내용 입력",
        value=st.session_state.memo,
        height=300
    )


    col1, col2 = st.columns(2)



    with col1:


        if st.button("저장"):


            st.session_state.memo = memo


            st.success(
                "저장되었습니다."
            )



    with col2:


        if st.button("삭제"):


            st.session_state.memo = ""


            st.success(
                "삭제되었습니다."
            )



    st.divider()


    st.subheader(
        "현재 메모"
    )


    st.write(
        st.session_state.memo
    )



# =====================================================
# Spinner / Progress 공통 실습
# =====================================================


st.divider()

st.subheader(
    "⏳ Spinner / Progress 실습"
)


if st.button("작업 실행"):


    progress = st.progress(0)


    with st.spinner(
        "처리 중입니다..."
    ):


        for i in range(100):

            time.sleep(0.03)

            progress.progress(
                i + 1
            )


    st.success(
        "완료!"
    )