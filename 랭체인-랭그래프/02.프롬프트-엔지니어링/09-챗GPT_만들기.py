from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI
import sys
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import *

# 현재 파일 기준으로 3단계 위 폴더를 import 경로에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))

from llm_loader import init_custom_llm

llm = init_custom_llm()

############################### 대화 이어가기  = 챗 GPT 만들기 

messages = [
    SystemMessage(
        content="당신은 친절한 AI입니다."
    )
]

while True:
    question = input("질문 : ")    
    if question == "exit":
        break

    messages.append(
        HumanMessage(content=question)
    )

    response = llm.invoke(messages)
    print("AI :", response.content)
    messages.append(response)