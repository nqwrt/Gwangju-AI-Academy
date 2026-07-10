# START
#  ↓
# plus10
#  ↓

# value ≥ 50 ?

# NO
# ↑
# │

# YES
# ↓

# END

from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)


# ==========================
# State
# ==========================

class State(TypedDict):
    value:int


# ==========================
# Node
# ==========================

def plus10(state):
    state["value"] += 10
    print(f"현재 값 → {state['value']}")
    return state


# ==========================
# 조건 함수
# ==========================

def should_continue(state):
    
    if state["value"] >= 50:
        return "end"
    
    return "repeat"


# ==========================
# Graph
# ==========================

builder = StateGraph(State)


builder.add_node("plus10",plus10)

builder.add_edge(START,"plus10")
builder.add_conditional_edges(
    "plus10",
    should_continue,
    {
        "repeat":"plus10",
        "end":END
    }
)

graph = builder.compile()


# ==========================
# 실행
# ==========================
result = graph.invoke(
    {
        "value":0
    }
)


print()

print("최종 결과")
print(result)
from util import show_graph
show_graph(graph)

####  문제
# 실습 문제

# 문제:

# START
#  ↓
# multiply2
#  ↓
# 100 이상이면 종료

# 초기값:

# 5

# 결과:

# 10
# 20
# 40
# 80
# 160
# 종료

from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)


# ==========================
# State
# ==========================

class State(TypedDict):
    value: int


# ==========================
# Node
# ==========================

def multiply2(state):
    state["value"] *= 2
    print(f"현재 값 → {state['value']}")
    return state


# ==========================
# 조건 함수
# ==========================

def route(state):
    if state["value"] >= 100:
        return "end"
    return "repeat"


# ==========================
# Graph 생성
# ==========================

builder = StateGraph(
    State
)

builder.add_node("multiply2",multiply2)
builder.add_edge(START,"multiply2")

# 반복 조건
builder.add_conditional_edges(
    "multiply2",
    route,
    {
        "repeat":"multiply2",
        "end":END
    }
)

# 왜 100이 아니라
# 160에서 끝났을까?
# 조건 검사는 계산 후 실행되기 때문


# 컴파일
graph = builder.compile()
print(
    graph.get_graph().draw_mermaid()
)
# ==========================
# 실행
# ==========================

result = graph.invoke(
    {
        "value":5
    }
)

print()
print("종료")
print(result)
show_graph(graph)