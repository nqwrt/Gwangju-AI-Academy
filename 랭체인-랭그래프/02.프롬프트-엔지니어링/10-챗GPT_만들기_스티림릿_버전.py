from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI
import sys
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import *
import streamlit as st

# 현재 파일 기준으로 3단계 위 폴더를 import 경로에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))

from llm_loader import init_custom_llm

llm = init_custom_llm()

st.set_page_config(
    page_title="ChatGPT",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 ChatGPT")

# 처음 한 번만 생성
if "messages" not in st.session_state:

    st.session_state.messages = [

        SystemMessage(
            content="당신은 친절한 AI입니다."
        )

    ]

# 화면 출력
for message in st.session_state.messages:

    if isinstance(message, HumanMessage):

        with st.chat_message("user"):
            st.markdown(message.content)

    elif isinstance(message, AIMessage):

        with st.chat_message("assistant"):
            st.markdown(message.content)

# 입력창
question = st.chat_input("질문을 입력하세요.")

if question:

    human = HumanMessage(
        content=question
    )

    st.session_state.messages.append(human)

    with st.chat_message("user"):
        st.markdown(question)

    response = llm.invoke(
        st.session_state.messages
    )

    st.session_state.messages.append(response)

    with st.chat_message("assistant"):
        st.markdown(response.content)