# Supervisor Agent: 어떤 Agent가 작업할지 결정하는 관리자
# Calculator Agent: 계산 전담
# Chat Agent: 일반 대화 전담
# Conditional Edge: Supervisor의 결정(next)에 따라 실행할 Node를 동적으로 선택

from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)

# =====================================================
# State
# =====================================================

class State(TypedDict):
    question: str
    next: str
    answer: str


# =====================================================
# Supervisor Agent
# =====================================================

def supervisor(state: State):

    question = state["question"]

    print("=" * 50)
    print("Supervisor Agent")
    print("질문 분석 중...")
    print(f"질문 : {question}")

    # 계산 관련 질문
    if any(keyword in question for keyword in ["계산", "+", "-", "*", "/"]):

        print("→ Calculator Agent에게 전달\n")
        return {
            "next": "calculator"
        }

    # 일반 대화
    print("→ Chat Agent에게 전달\n")

    return {
        "next": "chatbot"
    }


# =====================================================
# Calculator Agent
# =====================================================

def calculator(state: State):

    print("Calculator Agent 실행")

    return {
        "answer": "계산 결과입니다."
    }


# =====================================================
# Chat Agent
# =====================================================

def chatbot(state: State):

    print("Chat Agent 실행")

    return {
        "answer": "일반 대화입니다."
    }


# =====================================================
# Graph 생성
# =====================================================

builder = StateGraph(State)

builder.add_node("supervisor", supervisor)
builder.add_node("calculator", calculator)
builder.add_node("chatbot", chatbot)

builder.add_edge(START, "supervisor")

def route(state):
    return state["next"]


builder.add_conditional_edges(
    "supervisor",
    route, #lambda state: state["next"],
    {
        "calculator": "calculator",
        "chatbot": "chatbot"
    }
)

builder.add_edge("calculator", END)
builder.add_edge("chatbot", END)

graph = builder.compile()


# =====================================================
# 실행
# =====================================================

while True:

    question = input("\n질문(exit 종료) : ")

    if question.lower() == "exit":
        break

    result = graph.invoke(
        {
            "question": question
        }
    )

    print("-" * 50)
    print("최종 답변")
    print(result["answer"])

# 실행 예시 1
# 질문(exit 종료) : 10 + 20 계산해줘

# ==================================================
# Supervisor Agent
# 질문 분석 중...
# 질문 : 10 + 20 계산해줘

# → Calculator Agent에게 전달

# Calculator Agent 실행

# --------------------------------------------------
# 최종 답변
# 계산 결과입니다.
# 실행 예시 2
# 질문(exit 종료) : 안녕하세요

# ==================================================
# Supervisor Agent
# 질문 분석 중...
# 질문 : 안녕하세요

# → Chat Agent에게 전달

# Chat Agent 실행

# --------------------------------------------------
# 최종 답변
# 일반 대화입니다.