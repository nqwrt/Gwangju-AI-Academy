from dotenv import load_dotenv
from typing import TypedDict
from langchain.chat_models import (
    init_chat_model
)

from langgraph.graph import (
    StateGraph,
    START,
    END
)

import os

# ==========================
# 환경변수
# ==========================

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from llm_loader import init_custom_llm

llm = init_custom_llm()

from langchain_core.tools import tool
from  datetime import datetime

@tool
def add(a: int, b: int) -> int:
    """
    두 숫자를 더합니다.
    """
    return a + b

print(
    add.invoke(
        {
            "a": 10,
            "b": 20
        }
    )
)

@tool
def age(birth_year: int) -> int:
    """
    출생연도를 입력받아 현재 나이를 계산합니다.
    """
    current_year = datetime.now().year

    return current_year - birth_year


print(
    age.invoke(
        {
            "birth_year": 2000
        }
    )
)

from langchain.agents import create_agent
from langchain_core.messages import (
    HumanMessage,
    SystemMessage
)
# -------------------------
# Agent 생성
# -------------------------
agent = create_agent(
    model=llm,
    tools=[age]
)

# -------------------------
# 질문
# -------------------------
question = "2000년생 나이는?"

# -------------------------
# Agent 실행
# -------------------------
result = agent.invoke(
    {
        "messages": [
            SystemMessage(
                content="당신은 친절한 AI 비서입니다."
            ),
            HumanMessage(
                content=question
            )
        ]
    }
)


# -------------------------
# 결과 출력
# -------------------------
print("="*50)
print(result["messages"][-1].content)