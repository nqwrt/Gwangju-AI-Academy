import streamlit as st

from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
import sys
from pathlib import Path
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

sys.path.append(
    str(Path(__file__).resolve().parent.parent.parent)
)
from llm_loader import init_custom_llm

llm = init_custom_llm()


st.title("💬 대화 저장")

if "messages" not in st.session_state:

    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("질문")

if question:
    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )

    with st.chat_message("user"):
        st.write(question)

    response = llm.invoke(question)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":response.content
        }
    )

    with st.chat_message("assistant"):

        st.write(response.content)

# 브라우저 메모리
# ↓
# 새로고침 전까지 유지
# ↓
# 채팅 저장 가능