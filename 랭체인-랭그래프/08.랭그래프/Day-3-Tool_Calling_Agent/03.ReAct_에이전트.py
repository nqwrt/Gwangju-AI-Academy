# ReAct (Reasoning + Acting) 이란?

# ReAct = Reasoning(생각) + Acting(행동)

# LLM이 단순히 답변만 생성하는 것이 아니라,

# Reasoning : 문제를 분석하고 다음 행동을 결정
# Acting : 필요한 Tool(검색, 계산, DB 조회 등)을 실행
# Observation : Tool 결과를 확인
# 다시 Reasoning → Acting 반복
# 최종 Answer 생성

# 하는 Agent 패턴

# 사용자 질문
#     ↓
# LLM (Reasoning)
#     ↓
# 어떤 Tool을 사용할까?
#     ↓
# Action (Tool 실행)
#     ↓
# Observation (결과 확인)
#     ↓
# LLM 재추론
#     ↓
# 최종 답변


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