# 사실 Human in the Loop(HITL)는 LangGraph에서 가장 실무적인 기능인데, 
# 처음 배우면 "왜 굳이 사람이 중간에 끼어들지?"라는 생각이 생김

# 핵심은 한 문장임
# AI가 혼자 결정하면 위험한 일을, 사람이 최종 확인하도록 만드는 것

# 핵심함수 2개 이해
# 이것이 interrupt()와 resume()이 존재하는 이유

from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langgraph.types import (
    interrupt,
    Command
)

# ---------------------------------
# State
# ---------------------------------

class State(TypedDict):
    report: str
    approved: bool

# ---------------------------------
# 보고서 작성
# ---------------------------------

def report_node(state: State):
    print("보고서를 작성했습니다.")
    return {
        "report": "2026년 AI 시장 분석 보고서"
    }

# ---------------------------------
# 사람 승인
# ---------------------------------

def approval_node(state: State):

    print("\n결재 요청...")
    print(state["report"])

    # interrupt()
    # Graph
    # ↓
    # interrupt()
    # ↓
    # Checkpoint 저장
    # ↓
    # Graph 종료
    # ↓
    # (몇 초 후)
    # ↓
    # resume()
    # ↓
    # 계속 실행

    #왜 이렇게 만들었을까?
    #실무에서는 사람이 즉시 입력하지 않는 경우가 많기 때문
    
    #팀장이
    #3시간 뒤
    #승인할 수도 있습니다.

    # "여기서 Graph 실행을 중단하고 현재 상태를 저장한 뒤, 나중에 resume()이 호출되면 
    # 전달받은 값을 answer에 넣어서 이 다음 줄부터 계속 실행하라."
    answer = interrupt(
        "승인하시겠습니까? (yes / no)"
    )

    return {
        "approved": answer
    }


# ---------------------------------
# 최종 처리
# ---------------------------------

def finish_node(state: State):

    if state["approved"]:
        print("\n보고서가 승인되었습니다.")
    else:
        print("\n보고서가 거절되었습니다.")
    return state


# ---------------------------------
# Graph
# ---------------------------------

builder = StateGraph(State)

builder.add_node("report",report_node)
builder.add_node("approval",approval_node)
builder.add_node("finish",finish_node)

builder.add_edge(START,"report")
builder.add_edge("report","approval")
builder.add_edge("approval","finish")
builder.add_edge("finish",END)

from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()

graph = builder.compile(
    checkpointer=memory
)

# ---------------------------------
# 실행
# ---------------------------------

config = {
    "configurable": {
        "thread_id": "approval-demo"
    }
}

print("=" * 50)
print("1차 실행")
print("=" * 50)

result = graph.invoke(
    {}, # => 초기 state 값
    config=config
)

print(result)

print()
print("=" * 50)
print("재개")
print("=" * 50)

answer = input("승인 여부 (True / False) : ")

approved = answer.strip().lower() in ["yes", "y", "승인"]

result = graph.invoke(
    Command(resume = approved),   # => LangGraph가 answer = interrupt(...) 로 돌아감  다시 돌아옴.
    config=config
)

print(result)

# from util import show_graph
# show_graph(graph)