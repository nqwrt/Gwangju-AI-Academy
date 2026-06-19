from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from IPython.display import Image


# =========================
# State
# =========================

class State(TypedDict):
    score:int
    result:str


# =========================
# Node1
# =========================

def check_score(state):
    print("\n점수 검사")
    return state


# =========================
# Node2
# =========================

def pass_node(state):
    state["result"]="합격"
    return state


# =========================
# Node3
# =========================

def fail_node(state):
    state["result"]="불합격"
    return state


# =========================
# 조건 함수
# =========================

def route(state):
    if state["score"] >= 60:
        return "pass"

    return "fail"


# =========================
# Graph
# =========================

builder = StateGraph(State)


builder.add_node("check",check_score)
builder.add_node("pass",pass_node)
builder.add_node("fail",fail_node)


builder.add_edge(START,"check")
builder.add_conditional_edges(
    "check",
    route,
    {
        "pass":"pass",
        "fail":"fail"
    }
)
builder.add_edge("pass",END)
builder.add_edge("fail",END)


graph = builder.compile()


# =========================
# 실행
# =========================

result = graph.invoke({"score":80})

print()
print(result)

from util import show_graph

show_graph(graph)
