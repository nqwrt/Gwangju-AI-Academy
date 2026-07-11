#                사용자 질문
#                      │
#                      ▼
#              Supervisor Agent (LLM)
#                      │
#         ┌────────────┴────────────┐
#         ▼                         ▼
#   Research Agent             Math Agent
#        (LLM)                     (LLM)
#         │                         │
#         └────────────┬────────────┘
#                      ▼
#                   최종 답변

from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from llm_loader import init_custom_llm

llm = init_custom_llm()

# ====================================================
# State
# ====================================================

class State(TypedDict):
    question: str
    next: str
    answer: str


# ====================================================
# Supervisor Agent
# ====================================================

def supervisor(state: State):

    prompt = f"""
당신은 Supervisor Agent입니다.

사용자의 질문을 보고

research
math

둘 중 하나만 출력하세요.

질문:
{state["question"]}

답:
"""

    response = llm.invoke(prompt)

    next_agent = response.content.strip().lower()

    print("=" * 50)
    print("Supervisor :", next_agent)

    if "math" in next_agent:
        next_agent = "math"
    else:
        next_agent = "research"

    return {
        "next": next_agent
    }


# ====================================================
# Research Agent
# ====================================================

def research_agent(state: State):

    prompt = f"""
당신은 Research Agent입니다.

다음 질문에 친절하게 답하세요.

질문

{state["question"]}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }


# ====================================================
# Math Agent
# ====================================================

def math_agent(state: State):

    prompt = f"""
당신은 수학 전문가입니다.

다음 계산을 수행하세요.

{state["question"]}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }


# ====================================================
# Route
# ====================================================

def route(state):

    return state["next"]


# ====================================================
# Graph
# ====================================================

builder = StateGraph(State)

builder.add_node(
    "supervisor",
    supervisor
)

builder.add_node(
    "research",
    research_agent
)

builder.add_node(
    "math",
    math_agent
)

builder.add_edge(
    START,
    "supervisor"
)

builder.add_conditional_edges(
    "supervisor",
    route,
    {
        "research": "research",
        "math": "math"
    }
)

builder.add_edge(
    "research",
    END
)

builder.add_edge(
    "math",
    END
)

graph = builder.compile()

# ====================================================
# 실행
# ====================================================

while True:

    question = input("\n질문(exit 종료): ")

    if question == "exit":
        break

    result = graph.invoke(
        {
            "question": question
        }
    )

    print()
    print("=" * 50)
    print(result["answer"])