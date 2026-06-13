

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from langchain_core.prompts import (
    MessagesPlaceholder
)

from langchain.chat_models import init_chat_model

from langchain_core.chat_history import (
    InMemoryChatMessageHistory
)

from langchain_core.runnables.history import (
    RunnableWithMessageHistory
)

# pip install langchain_community
from langchain_community.chat_message_histories import FileChatMessageHistory

import os

load_dotenv()

LLM_MODEL = os.getenv("LLM_AI_MODEL")

# 1. LLM 생성
llm = init_chat_model(
    LLM_MODEL,
    temperature=0.1,
    max_tokens=1000
    )


# 2. Prompt 구성 (history + question 구조)
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 AI 비서입니다."),
    ("placeholder", "{history}"),
    ("human", "{question}")
])

# 3. 기본 chain 생성
chain = prompt | llm

# 4. 파일 저장 폴더 생성
os.makedirs("chat_histories", exist_ok=True)

# 5. 파일 기반 세션 메모리
def get_file_session_history(session_id: str):
    return FileChatMessageHistory(f"chat_histories/{session_id}.json")

# InMemoryChatMessageHistory()
# HumanMessage ──┐
#                ├──> InMemoryChatMessageHistory
# AIMessage   ───┘
#                      |
#                      v
#               messages 리스트 저장

# 5. Memory가 붙은 chain
# 👉 “메모리를 직접 관리하지 않는 Agent 구조 완성” = 메모리를 자동으로 관리하는 Agent

# # ✅ RunnableWithMessageHistory가 하는 것
# 1. history 불러오기
# 2. prompt에 넣기
# 3. LLM 호출
# 4. 결과 저장 구조 완성

# RunnableWithMessageHistory = "메모리 로딩 + 프롬프트 삽입 + 저장"을 자동화한 시스템
# 6. Memory 붙이기
chain_with_file_history = RunnableWithMessageHistory(
    chain,
    get_file_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

# 6. 실행 루프
while True:

    q = input("질문: ")

    if q == "exit":
        break

    res = chain_with_file_history.invoke(
        {
            "question": q
        },
        config={
            "configurable": {
                "session_id": "user-1"
            }
        }
    )

    print("\nAI:", res.content)

#             [User Question]
#                |
#                v
# -------------------------------------
# RunnableWithMessageHistory
# -------------------------------------
#                |
#                v
#         session_id 확인
#                |
#                v
# -------------------------------------
# store["user01"] 조회
# -------------------------------------
#                |
#                v
#      InMemoryChatMessageHistory
#                |
#                v
# -------------------------------------
# PromptTemplate + history 삽입
# -------------------------------------
#                |
#                v
#               LLM
#                |
#                v
#          AI Response 생성
#                |
#                v
# -------------------------------------
# history 자동 저장 (핵심)
# -------------------------------------
#                |
#                v
#          다음 질문에 재사용