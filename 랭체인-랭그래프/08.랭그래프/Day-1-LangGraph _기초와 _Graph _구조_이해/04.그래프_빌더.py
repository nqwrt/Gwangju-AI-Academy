# 5교시 실습: Graph Builder + 계산기 Agent 만들기 (2시간)
# 학습 목표

# 이번 실습에서는 LangGraph의 전체 실행 흐름을 익힙니다.

# 배울 내용:

# StateGraph
# add_node()
# add_edge()
# compile()
# invoke()
# stream()

# 최종 구조:

#간단한 LangGraph 예제: 인사 Agent

from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)


# =========================
# 1. State 정의
# =========================

class State(TypedDict):
    name: str
    greeting: str



# =========================
# 2. Node 만들기
# =========================


# 입력 Node

def input_node(state: State):

    print("[Input Node]")
    print( "이름:", state["name"])
    return {}



# 처리 Node

def greeting_node(state: State):
    print("[Greeting Node]")
    greeting = (
        f"안녕하세요 {state['name']}님!"
    )

    return {
        "greeting": greeting
    }



# 출력 Node

def output_node(state: State):
    print("[Output Node]")

    print(
        state["greeting"]
    )


    return {}

# =========================
# 3. Graph Builder
# =========================

builder = StateGraph(State)

# Node 등록

builder.add_node(
    "input",
    input_node
)


builder.add_node(
    "greeting",
    greeting_node
)


builder.add_node(
    "output",
    output_node
)



# Edge 연결

builder.add_edge(
    START,
    "input"
)


builder.add_edge(
    "input",
    "greeting"
)


builder.add_edge(
    "greeting",
    "output"
)


builder.add_edge(
    "output",
    END
)



# =========================
# 4. Compile
# =========================

graph = builder.compile()



# =========================
# 5. invoke 실행
# =========================

result = graph.invoke(
    {
        "name":"홍길동",
        "greeting":""
    }
)


print("\n최종 State")

print(result)

# stream 확인
# graph.stream()은 LangGraph 실행 과정을 단계별로 확인하기 위한 함수

# graph.invoke()와 가장 큰 차이는:

# invoke() → 전체 실행 후 최종 State 반환
# stream() → Node가 실행될 때마다 중간 결과를 하나씩 반환
print("==========")
for chunk in graph.stream(
    {
        "name":"김철수",
        "greeting":""
    }
):

    print(chunk)