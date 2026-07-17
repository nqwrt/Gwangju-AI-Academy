from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langgraph.graph.message import add_messages

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

import sys
from pathlib import Path

# ----------------------------------------------------
# 프로젝트 경로
# ----------------------------------------------------

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent)
)

from llm_loader import init_custom_llm

llm = init_custom_llm()

# ----------------------------------------------------
# State
# ----------------------------------------------------

class DebugState(TypedDict):

    # 대화 내역
    messages: Annotated[list, add_messages]

    # Planner가 결정
    need_debug: bool

    # 각 Agent 완료 여부
    debug_done: bool
    fix_done: bool
    review_done: bool

    # Supervisor가 선택할 다음 노드
    next: str


# ----------------------------------------------------
# Planner
# ----------------------------------------------------

def planner(state: DebugState):

    print("\n========== Planner ==========")
    user_question = state["messages"][0].content

    prompt = f"""
당신은 Software Project Planner입니다.

사용자의 요청을 읽고

디버깅 작업인지 판단하세요.

오류를 분석하지 않고
코드를 수정하지 않고
리뷰도 하지 않습니다.

반드시 아래 형식만 출력하세요.

debug=True

또는

debug=False


----------------------

사용자 요청

{user_question}
"""

    result = llm.invoke(prompt)
    text = result.content.lower()
    need_debug = "debug=true" in text

    print(result.content)

    return {
        "need_debug": need_debug
    }


# ----------------------------------------------------
# Router
# ----------------------------------------------------

def router(state: DebugState):

    return state["next"]

# ----------------------------------------------------
# Debugger Agent
# ----------------------------------------------------

def debugger(state: DebugState):

    print("\n========== Debugger ==========")

    messages = state["messages"]

    result = llm.invoke(
        messages +
        [
            HumanMessage(content=
"""
당신은 Python Debugger 입니다.

역할

1. 코드를 분석하세요.

2. 오류의 원인을 찾으세요.

3. 왜 오류가 발생했는지 설명하세요.

4. 수정 방향만 제안하세요.

주의

- 절대로 코드를 수정하지 마세요.
- 수정 코드는 작성하지 마세요.
- 원인 분석만 수행하세요.

출력 형식

## 오류 원인

...

## 발생 이유

...

## 수정 방향

...
"""
            )
        ]
    )

    return {
        "messages":[
            AIMessage(
                content = result.content,
                name="Debugger"
            )
        ],
        "debug_done":True
    }


# ----------------------------------------------------
# Coder Agent
# ----------------------------------------------------

def coder(state: DebugState):

    print("\n========== Coder ==========")

    messages = state["messages"]

    result = llm.invoke(

        messages +

        [

            HumanMessage(

                content="""
당신은 Python Developer 입니다.

Debugger의 분석 결과를 참고하여

버그를 수정하세요.

조건

- 수정된 Python 코드만 작성하세요.

- 코드 설명은 작성하지 마세요.

- Markdown 설명도 작성하지 마세요.

- 실행 가능한 코드만 출력하세요.
"""

            )

        ]

    )

    return {

        "messages":[

            AIMessage(

                content=result.content,

                name="Coder"

            )

        ],

        "fix_done":True

    }


# ----------------------------------------------------
# Reviewer Agent
# ----------------------------------------------------

def reviewer(state: DebugState):

    print("\n========== Reviewer ==========")

    messages = state["messages"]

    result = llm.invoke(

        messages +

        [

            HumanMessage(

                content="""
당신은 Senior Python Reviewer 입니다.

아래 수정된 코드를 리뷰하세요.

검토 항목

1. 버그가 해결되었는가?

2. 코드 품질

3. 예외 처리

4. 성능

5. 가독성

6. PEP8 준수

출력 형식

## 리뷰 결과

PASS 또는 FAIL

## 장점

...

## 개선 사항

...
"""

            )

        ]

    )

    return {

        "messages":[
            AIMessage(
                content = result.content,
                name="Reviewer"
            )
        ],
        "review_done":True
    }

# ----------------------------------------------------
# Supervisor
# ----------------------------------------------------

def supervisor(state: DebugState):

    print("\n========== Supervisor ==========")

    # 1단계
    if not state["debug_done"]:

        print("Next -> Debugger")

        return {
            "next":"Debugger"
        }

    # 2단계
    if not state["fix_done"]:

        print("Next -> Coder")

        return {
            "next":"Coder"
        }

    # 3단계
    if not state["review_done"]:

        print("Next -> Reviewer")

        return {
            "next":"Reviewer"
        }

    print("Next -> END")

    return {
        "next":"FINISH"
    }


# ----------------------------------------------------
# Router
# ----------------------------------------------------

def router(state: DebugState):

    return state["next"]


# ----------------------------------------------------
# Graph Builder
# ----------------------------------------------------

builder = StateGraph(DebugState)

# Planner
builder.add_node(
    "Planner",
    planner
)

# Supervisor
builder.add_node(
    "Supervisor",
    supervisor
)

# Specialists
builder.add_node(
    "Debugger",
    debugger
)

builder.add_node(
    "Coder",
    coder
)

builder.add_node(
    "Reviewer",
    reviewer
)

# ----------------------------------------------------
# Edge
# ----------------------------------------------------

builder.add_edge(
    START,
    "Planner"
)

builder.add_edge(
    "Planner",
    "Supervisor"
)

# ----------------------------------------------------
# Conditional Routing
# ----------------------------------------------------

builder.add_conditional_edges(
    "Supervisor",
    router,
    {
        "Debugger":"Debugger",
        "Coder":"Coder",
        "Reviewer":"Reviewer",
        "FINISH":END
    }
)

# ----------------------------------------------------
# Back To Supervisor
# ----------------------------------------------------

builder.add_edge(
    "Debugger",
    "Supervisor"
)

builder.add_edge(
    "Coder",
    "Supervisor"
)

builder.add_edge(
    "Reviewer",
    "Supervisor"
)

# ----------------------------------------------------
# Compile
# ----------------------------------------------------

graph = builder.compile()

# ----------------------------------------------------
# (선택) Graph 시각화
# ----------------------------------------------------
try:
    sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
    from util import show_graph

    print("\n========== Graph Visualization ==========")
    show_graph(graph)

except Exception as e:
    print(f"Graph 시각화 생략: {e}")

# ----------------------------------------------------
# 실행 예제
# ----------------------------------------------------

input_code = '''
def average(nums):
    return sum(nums) / len(nums)

print(average([]))
'''

initial_state = {
    "messages": [
        HumanMessage(
            content=f"""
아래 Python 코드의 오류를 수정해주세요.

```python
{input_code}
```
"""
        )
    ],
    "need_debug": False,
    "debug_done": False,
    "fix_done": False,
    "review_done": False,
    "next": "",
}

# ----------------------------------------------------
# stream 실행 (과정 확인)
# ----------------------------------------------------

print("\n" + "=" * 60)
print("Supervisor Multi-Agent 실행")
print("=" * 60)

for chunk in graph.stream(initial_state):
    print("\n[STATE UPDATE]")
    print(chunk)

# ----------------------------------------------------
# 최종 결과
# ----------------------------------------------------

result = graph.invoke(initial_state)

print("\n" + "=" * 60)
print("최종 결과")
print("=" * 60)

for message in result["messages"]:

    name = getattr(message, "name", "User")

    print(f"\n[{name}]")
    print("-" * 50)
    print(message.content)

print("\n" + "=" * 60)
print("상태 정보")
print("=" * 60)

print(f"need_debug : {result['need_debug']}")
print(f"debug_done : {result['debug_done']}")
print(f"fix_done   : {result['fix_done']}")
print(f"review_done: {result['review_done']}")
print(f"next       : {result['next']}")