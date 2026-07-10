"""
=========================================================
03_return.py

3교시
주제 : Node의 반환(return)

학습목표
---------------------------------------------------------
1. Node는 반드시 State를 반환해야 한다.
2. print()와 return의 차이를 이해한다.
3. return된 State가 다음 Node로 전달된다.
=========================================================
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# =====================================================
# State
# =====================================================

class State(TypedDict):
    number: int


# =====================================================
# Node
# =====================================================

def plus(state: State):

    print("=" * 60)
    print("plus Node")
    print("=" * 60)

    print("입력 :", state)

    new_number = state["number"] + 1

    print("1 증가 :", new_number)

    print("return 실행")

    return {
        "number": new_number
    }


# =====================================================
# Graph
# =====================================================

builder = StateGraph(State)

builder.add_node("plus", plus)
builder.add_edge(START, "plus")
builder.add_edge("plus", END)

graph = builder.compile()


# =====================================================
# Graph 구조
# =====================================================

print("=" * 60)
print("Graph")
print("=" * 60)

print(graph.get_graph().draw_ascii())


# =====================================================
# 실행
# =====================================================

print("\n")
print("=" * 60)
print("Graph 시작")
print("=" * 60)

result = graph.invoke(
    {
        "number": 10
    }
)

print("\n")
print("=" * 60)
print("Graph 종료")
print("=" * 60)

print(result)