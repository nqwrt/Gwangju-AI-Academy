import streamlit as st

from graph_조건분기_추가 import graph

print("graph import")

st.title("📄 PDF ChatBot")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


question = st.chat_input("질문을 입력하세요.")

if question:
    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.spinner("검색중..."):

        result = graph.invoke(
            {
                "question":question
            }
        )

    answer = result["answer"]

    with st.chat_message("assistant"):

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )