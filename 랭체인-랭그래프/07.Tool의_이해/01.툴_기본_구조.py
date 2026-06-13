from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()

LLM_MODEL = os.getenv("LLM_AI_MODEL")

# OpenAI 모델 초기화 (OPENAI_API_KEY 환경변수 필요)
llm = init_chat_model(
    LLM_MODEL,
    temperature=0.1,
    max_tokens=1000
    )

# tool 이란, LLM이 "행동"할 수 있게 해주는 함수

# LLM
#  ↓
# Tool 선택 (multiply)
#  ↓
# 실행
#  ↓
# 결과 반환

from langchain.tools import tool
from datetime import datetime

#LLM 은 현재 시각을 학습 하지 않았기 때문에, 시간을 알려줄수 없음
@tool
def get_time(city: str) -> str:
    """도시 이름을 받아 현재 시간을 알려준다"""
    now = datetime.now()
    return f"{city} 현재 시간: {now.strftime('%Y-%m-%d %H:%M:%S')}"

print(get_time)
print(type(get_time))

print(get_time.invoke({"city": "Seoul"}))
