#  메모리 관리에서 가장 중요한 부분
# **"왜 RunnableWithMessageHistory를 사용하는가?"**를 이해하는 것이 목표
# 흐름은 반드시 아래처럼 진행하는 것을 추천
# 직접 저장 → 불편함 → RunnableWithMessageHistory → 자동 저장

# 예제 1. 직접 저장하는 방식 (복습)
# history.add_user_message(question)
# response = llm.invoke(history.messages)
# history.add_ai_message(response.content)
# 질문
# "매번 이 세 줄을 써야 할까요?"
# 답
# 너무 불편하다.

# 사용자
#    ↓
# add_user_message()
#    ↓
# LLM
#    ↓
# add_ai_message()

# (직접 저장)

# 사용자
#    ↓
# RunnableWithMessageHistory
#    ↓
# 자동 저장
#    ↓
# LLM
#    ↓
# 자동 저장

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from llm_loader import init_custom_llm

llm = init_custom_llm()

prompt = ChatPromptTemplate.from_messages([
    ("system","친절한 AI"),
    MessagesPlaceholder("history"),
    ("human","{question}")
])


####################################################
# 2. Prompt 생성
####################################################

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 친절한 AI 비서입니다."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

####################################################
# 3. Chain 생성
####################################################

chain = prompt | llm

####################################################
# 4. Memory 저장소
####################################################

store = {}

def get_session_history(session_id: str):

    if session_id not in store:
        print(f"\n새로운 메모리 생성 : {session_id}\n")
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


####################################################
# 5. RunnableWithMessageHistory
####################################################

chain_with_history = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

####################################################
# 6. 대화 함수
####################################################


def chat(session_id, question):

    print("=" * 60)
    print("Session :", session_id)
    print("Question :", question)

    response = chain_with_history.invoke(
        {"question": question},
        config={
            "configurable": {
                "session_id": session_id
            }
        },
    )

    print("Answer :", response.content)
    print()

####################################################
# 7. 첫 번째 사용자
####################################################

chat("abc", "안녕하세요.")
chat("abc", "제 이름은 철수입니다.")
chat("abc", "제 이름이 뭐였죠?")

####################################################
# 8. 두 번째 사용자
####################################################

chat("kim", "제 이름이 뭐죠?")
chat("kim", "제 이름은 영희입니다.")
chat("kim", "제 이름이 뭐였죠?")

####################################################
# 9. 첫 번째 사용자 다시
####################################################

chat("abc", "제 이름이 뭐였죠?")
####################################################
# 10. Memory 확인
####################################################

print("\n")
print("=" * 60)
print("ABC Memory")
print("=" * 60)

for message in store["abc"].messages:
    print(message)

print("\n")

print("=" * 60)
print("KIM Memory")
print("=" * 60)

for message in store["kim"].messages:
    print(message)