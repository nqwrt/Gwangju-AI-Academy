# 반복문 구현
# Loop

# LangGraph에서는 Edge를 자기 자신에게 연결하면 반복 가능

from typing import TypedDict
from langgraph.graph import *


class State(TypedDict):
    count:int

def counter(state):
    count = state["count"]
    print(
        "현재 숫자:",
        count
    )

    return {
        "count":count+1
    }


def check_count(state):

    if state["count"]>=3:
        return "end"
    else:
        return "continue"



builder=StateGraph(State)

builder.add_node(
    "counter",
    counter
)



builder.add_edge(
    START,
    "counter"
)



builder.add_conditional_edges(
    "counter",
    check_count,
    {
        "continue":"counter",
        "end":END
    }
)

graph=builder.compile()

graph.invoke(
    {
        "count":0
    }
)

#stream으로 확인하기
for chunk in graph.stream(
    {
        "count":0
    }
):

    print(chunk)

# START
#   │
# counter
#   │
# continue
#   │
# counter
#   │
# continue
#   │
# counter
#   │
# END

# → add_conditional_edges()를 이용한 Graph 내부 반복