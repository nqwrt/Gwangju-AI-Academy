# | 구분    | Session     | Cache          |
# | ----- | ----------- | -------------- |
# | 목적    | 사용자 상태 유지   | 작업 결과 재사용      |
# | 기준    | 사용자별        | 앱/서버 기준        |
# | 저장 내용 | 로그인 정보, 입력값 | 데이터, 모델, 계산 결과 |
# | 공유    | 사용자마다 다름    | 여러 사용자가 공유 가능  |
# | 변경 주체 | 사용자 행동      | 프로그램 실행        |
# | 예     | 로그인 상태      | AI 모델          |


# ✅ Session State 이해
# ✅ 카운터 (+ / - / Reset)
# ✅ 로그인 / 로그아웃
# ✅ Sidebar
# ✅ Tabs
# ✅ Spinner
# ✅ Progress Bar
# ✅ cache_data
# ✅ cache_resource
# ✅ 메모장 만들기 과제


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

    st.title("Streamlit 실습")

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

    st.write(
        "현재 값:",
        st.session_state.count
    )

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


                st.rerun() # 앱을 즉시 처음부터 다시 실행하는 함수


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

    # =====================================================
    # cache_data 예제
    # =====================================================

    # 함수의 반환 결과를 캐시에 저장한다.
    # 같은 인자(number)로 다시 호출하면
    # 함수를 실행하지 않고 저장된 결과를 반환한다.
    @st.cache_data
    def slow_function(number):

        # 일부러 3초 지연시켜
        # 캐시의 효과를 확인하기 위한 코드
        time.sleep(3)

        # 입력받은 숫자의 제곱 반환
        return number * number

    # =====================================================
    # cache_resource 예제
    # =====================================================

    # 모델, DB Connection처럼
    # 무거운 객체를 한 번만 생성하기 위한 캐시
    @st.cache_resource
    def create_model():
        
        # 모델 생성 시간이 오래 걸린다고 가정
        time.sleep(3)

        # 실제 프로젝트에서는
        # ChatOpenAI(), 머신러닝 모델 등을 반환

        return {
            "model":"AI Model"
        }

    number = st.number_input(
        "숫자 입력",
        value=10
    )

    start = time.time()
    
    # 캐시 함수 실행
    result = slow_function(number)

    end = time.time()


    # 실행 시간을 계산하여 출력
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
    # =====================================================
    # Resource Cache 테스트
    # =====================================================

    # 모델 생성 함수 호출
    # 처음 한 번만 3초가 걸리고
    # 이후에는 캐시된 객체를 사용한다.
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

# 사용자 실행
#       │
#       ▼
# number_input()
#       │
#       ▼
# start = time.time()
#       │
#       ▼
# slow_function(number)
#       │
#       ├── 캐시 없음
#       │      │
#       │      ▼
#       │   3초 대기
#       │      │
#       │      ▼
#       │   계산
#       │      │
#       │      ▼
#       │   캐시에 저장
#       │
#       └── 캐시 있음
#              │
#              ▼
#       저장된 결과 즉시 반환
#       │
#       ▼
# end = time.time()
#       │
#       ▼
# 실행 시간 출력


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

# |           | Session            | Cache                                 |
# | --------- | ------------------ | ------------------------------------- |
# | Streamlit | `st.session_state` | `st.cache_data` / `st.cache_resource` |
# | 위치        | 서버 메모리(Session별)   | 서버 캐시 영역                              |
# | 사용자 구분    | O                  | 보통 X                                  |
# | 서버 재시작    | 삭제                 | 삭제                                    |
# | 영구 저장     | ❌                  | ❌                                     |


# 언제 무엇을 사용할까?
# Session State 사용
# 사용자와 관련된 것:
# ✅ 로그인 여부
# login=True
# ✅ 선택한 메뉴
# page="dashboard"
# ✅ 채팅 기록
# messages=[]
# ✅ 입력 중인 값
# name="홍길동"


# Cache 사용
# 비용이 큰 작업:
# ✅ CSV 읽기
# pd.read_csv()
# ✅ 데이터 전처리
# clean_data()
# ✅ AI 모델 생성
# load_model()
# ✅ DB 연결
# create_connection()