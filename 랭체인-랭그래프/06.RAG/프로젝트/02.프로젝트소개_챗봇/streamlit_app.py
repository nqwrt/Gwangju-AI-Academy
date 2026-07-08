import streamlit as st
from rag import ask

st.set_page_config(
    page_title="프로젝트 소개 챗봇",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 프로젝트 소개 챗봇")

# 대화 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
question = st.chat_input("질문을 입력하세요.")

if question:
    # 사용자 메시지 출력
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    # AI 응답
    with st.chat_message("assistant"):
        with st.spinner("생각하는 중..."):
            answer = ask(question)

        st.markdown(answer)

    # 대화 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )