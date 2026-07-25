import streamlit as st

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from graph import graph


st.set_page_config(page_title="LangGraph Chatbot")

st.title("🤖 LangGraph Chatbot")


# 최초 실행
if "messages" not in st.session_state:
    st.session_state.messages = []


# 이전 대화 출력
for msg in st.session_state.messages:

    if isinstance(msg, HumanMessage):

        with st.chat_message("user"):
            st.write(msg.content)

    elif isinstance(msg, AIMessage):

        with st.chat_message("assistant"):
            st.write(msg.content)


# 질문 입력
question = st.chat_input("질문하세요")

if question:

    # 사용자 출력
    with st.chat_message("user"):
        st.write(question)

    # Memory 저장
    st.session_state.messages.append(
        HumanMessage(content=question)
    )

    # LangGraph 호출
    result = graph.invoke(
        {
            "messages": st.session_state.messages
        }
    )

    answer = result["messages"][-1]

    # Memory 저장
    st.session_state.messages.append(answer)

    # AI 출력
    with st.chat_message("assistant"):
        st.write(answer.content)