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
import streamlit as st
from datetime import datetime

# 현재 파일 기준으로 3단계 위 폴더를 import 경로에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))

from llm_loader import init_custom_llm

llm = init_custom_llm()


st.set_page_config(
    page_title="AI 톡",
    layout="centered"
)

st.title("💬 AI 친구")

if "messages" not in st.session_state:

    st.session_state.messages = [
        SystemMessage(
            content="당신은 친절한 AI입니다."
        )
    ]

for msg in st.session_state.messages:

    if isinstance(msg, SystemMessage):
        continue

    now = datetime.now().strftime("%H:%M")

    if isinstance(msg, HumanMessage):

        st.markdown(
            f"""
<div style="
display:flex;
justify-content:flex-end;
margin:10px;
">

<div style="
background:#FEE500;
padding:12px;
border-radius:15px;
max-width:70%;
">

{msg.content}

<div style="
font-size:10px;
text-align:right;
color:gray;
">

{now}

</div>

</div>

</div>
""",
            unsafe_allow_html=True
        )

    elif isinstance(msg, AIMessage):

        st.markdown(
            f"""
<div style="
display:flex;
justify-content:flex-start;
margin:10px;
">

<div style="
background:white;
border:1px solid #ddd;
padding:12px;
border-radius:15px;
max-width:70%;
">

{msg.content}

<div style="
font-size:10px;
color:gray;
">

{now}

</div>

</div>

</div>
""",
            unsafe_allow_html=True
        )

question = st.chat_input("메시지를 입력하세요")

if question:

    st.session_state.messages.append(
        HumanMessage(content=question)
    )

    response = llm.invoke(
        st.session_state.messages
    )

    st.session_state.messages.append(response)

    st.rerun()