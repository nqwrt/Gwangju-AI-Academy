

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

from langchain_community.chat_message_histories import SQLChatMessageHistory

# MySQL 연결
def get_sql_session_history(session_id: str):

    return SQLChatMessageHistory(
        session_id=session_id,
        connection="mysql+pymysql://scott:tiger@localhost:3306/scott",
        table_name="message_store" # DB에 생성될 테이블 이름 (기본값: message_store)

    )

# 사용자 테이블은 자동 생성됨

# LangChain이 내부적으로:
# langchain_chat_histories
# 같은 테이블 자동 생성합니다.

chain_with_sql_history = RunnableWithMessageHistory(
    chain,
    get_sql_session_history,
    input_messages_key="question",
    history_messages_key="history",
)


while True:

    q = input("질문: ")

    if q == "exit":
        break

    res = chain_with_sql_history.invoke(
        {"question": q},
        config={
            "configurable": {
                "session_id": "user_1"
            }
        }
    )

    print("\nAI:", res.content)

# 저장소 선택 가이드
# 저장소를 선택할 때 고려사항:
# │
# ├─ 개발/테스트 → InMemoryChatMessageHistory
# │
# ├─ 프로덕션 (단일 서버)
# │   │
# │   ├─ 간단한 구현 → SQLite (SQLChatMessageHistory)
# │   └─ 기존 DB 활용 → PostgreSQL
# │
# └─ 프로덕션 (분산 환경)
#     │
#     ├─ 빠른 응답 필요 → Redis
#     ├─ 데이터 영구성 중요 → PostgreSQL
#     └─ 둘 다 필요 → Redis (캐시) + PostgreSQL (영구)