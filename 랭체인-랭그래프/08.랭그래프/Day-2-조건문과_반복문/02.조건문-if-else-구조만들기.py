# START

#  |
 
# check_user

#  |

# VIP -------- vip_node

# 일반 ------- normal_node

#  |

# END


from typing import TypedDict
from langgraph.graph import *


class State(TypedDict):

    name:str
    level:str
    message:str



def check_user(state):

    print("사용자 확인")

    return state



def vip_node(state):

    return {
        "message":
        "VIP 고객입니다."
    }



def normal_node(state):

    return {
        "message":
        "일반 고객입니다."
    }

def user_router(state):

    if state["level"]=="VIP":
        return "vip"
    else:
        return "normal"



builder = StateGraph(State)

builder.add_node(
    "check",
    check_user
)

builder.add_node(
    "vip",
    vip_node
)

builder.add_node(
    "normal",
    normal_node
)

builder.add_edge(
    START,
    "check"
)

builder.add_conditional_edges(
    "check",
    user_router,
    {
        "vip":"vip",
        "normal":"normal"
    }
)

builder.add_edge(
    "vip",
    END
)

builder.add_edge(
    "normal",
    END
)

graph=builder.compile()

print(
graph.invoke(
    {
        "name":"홍길동",
        "level":"VIP",
        "message":""
    }
))