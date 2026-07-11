# 점수

# 90 이상
#  |
# A


# 70 이상
#  |
# B


# 70 미만
#  |
# C

from typing import TypedDict
from langgraph.graph import *


class State(TypedDict):
    score:int
    grade:str



def check_score(state):
    return state



def grading(state):
    score=state["score"]


    if score>=90:
        return "A"
    elif score>=70:
        return "B"
    else:
        return "C"



def a_node(state):
    return {
        "grade":"A"
    }



def b_node(state):
    return {
        "grade":"B"
    }


def c_node(state):
    return {
        "grade":"C"
    }

builder=StateGraph(State)

builder.add_node(
    "check",
    check_score
)

builder.add_node(
    "A",
    a_node
)

builder.add_node(
    "B",
    b_node
)

builder.add_node(
    "C",
    c_node
)

builder.add_edge(
    START,
    "check"
)


builder.add_conditional_edges(
    "check",
    grading,
    {
        "A":"A",
        "B":"B",
        "C":"C"
    }
)

builder.add_edge("A",END)
builder.add_edge("B",END)
builder.add_edge("C",END)

graph=builder.compile()

print(
graph.invoke(
    {
        "score":85,
        "grade":""
    }
))