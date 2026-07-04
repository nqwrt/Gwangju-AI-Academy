
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI
import sys
from pathlib import Path

# 현재 파일 기준으로 3단계 위 폴더를 import 경로에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))
from llm_loader import init_custom_llm

# 메세지란?
# System
# 당신은 친절한 AI입니다.

# Human
# AI란 무엇인가요?

# AI
# AI는 인공지능입니다.

# Human
# 예제를 보여주세요.

# 한 줄의 대화 = Message 객체 하나로 관리
# 결론) 전체 대화 = Message List

from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage
)

# 1.시스템 메세지 만들기
system = SystemMessage(
    content="당신은 친절한 AI입니다."
)

print(system)
print(system.content)

ai = AIMessage(
    content="AI는 사람처럼 학습하는 기술입니다."
)

print(ai.content)

human = HumanMessage(
    content="AI란 무엇인가요?"
)

tool = ToolMessage(
    content="5",
    tool_call_id="call_123"
)

print(tool)
print(human)

print(type(system))
print(type(human))
print(type(ai))
print(type(tool))

# Message는 리스트로 관리됨
messages = [
    system,
    human,
    ai
]

print(messages)

for msg in messages:
    print("=" * 40)
    print(type(msg).__name__)
    print(msg.content)

#==============================================
messages = [
    SystemMessage(
        content="당신은 친절한 AI입니다."
    ),
    HumanMessage(
        content="AI란 무엇인가요?"
    )
]

llm = init_custom_llm()
response = llm.invoke(messages)
print(response.content)

#========================================
messages = [
    SystemMessage(
        content="당신은 친절한 AI입니다."
    ),
    HumanMessage(
        content="안녕하세요."
    ),
    AIMessage(   # AIMessage는 이전 대화를 LLM에게 알려주는 역할입니다.
        content="안녕하세요."
    ),
    HumanMessage(
        content="AI란?"
    )
]

response = llm.invoke(messages)

print(response.content)

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