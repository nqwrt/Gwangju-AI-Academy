from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ------------------------
# State
# ------------------------
class State(TypedDict):
    answer: int
    guess: int
    message: str

# ------------------------
# Node
# ------------------------
def check_number(state: State):

    answer = state["answer"]
    guess = state["guess"]

    if guess > answer:
        return {
            "message": "작게 입력하세요."
        }

    elif guess < answer:
        return {
            "message": "크게 입력하세요."
        }

    else:
        return {
            "message": "정답입니다!"
        }


# ------------------------
# Graph
# ------------------------
builder = StateGraph(State)

builder.add_node("check", check_number)

builder.add_edge(START, "check")
builder.add_edge("check", END)

graph = builder.compile()


# ------------------------
# 실행
# ------------------------
state = {
    "answer": 7,
    "guess": 0,
    "message": ""
}


while True:

    state["guess"] = int(input("숫자 입력 : "))
    result = graph.invoke(state)
    print(result["message"])

    if result["guess"] == result["answer"]:
        print("게임 종료!")
        break


# while True
#      │
# graph.invoke()
#      │
# 정답?
#  ┌────┴────┐
#  │         │
# No       Yes
#  │         │
# 반복      종료

# → Graph는 판단만 하고, 반복은 Python이 담당합니다.