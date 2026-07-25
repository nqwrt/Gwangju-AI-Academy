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

st.title("🤖 OpenAI 챗봇")

#항상 화면의 맨 아래에 고정
question = st.chat_input("질문하세요") 

if question:

    response = llm.invoke(question)

    st.write(response.content)