from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)


# ----------------
# State
# ----------------

class State(TypedDict):
    question:str
    answer:str

# ----------------
# Node
# ----------------

def question_node(state:State):
    print("질문 분석")
    return state


def simple_node(state:State):
    print("간단한 답변 생성")
    return {
        "answer":"간단한 질문입니다."
    }


def complex_node(state:State):
    print("복잡한 답변 생성")
    return {
        "answer":"복잡한 질문입니다."
    }

# ----------------
# 조건 함수
# ----------------

def check_question(state:State):

    if len(state["question"]) < 10:
        return "simple"
    else:
        return "complex"

# ----------------
# Graph 생성
# ----------------

builder = StateGraph(State)

builder.add_node(
    "question",
    question_node
)

builder.add_node(
    "simple",
    simple_node
)

builder.add_node(
    "complex",
    complex_node
)

builder.add_edge(
    START,
    "question"
)

# Conditional Edge

builder.add_conditional_edges(
    "question",
    check_question,
    {
        "simple":"simple",
        "complex":"complex"
    }
)

builder.add_edge(
    "simple",
    END
)

builder.add_edge(
    "complex",
    END
)

graph = builder.compile()
result = graph.invoke(
    {
        "question":"안녕하세요! 여러분 저는 홍길동 입니다.",
        "answer":""
    }
)
print(result)