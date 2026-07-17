# Planner(LLM)가 무엇을 해야 하는지 한 번만 판단
# Supervisor는 State만 보고 다음 노드를 결정
# Researcher/Coder는 작업 후 State를 업데이트
# 무한 루프가 발생하지 않음

from typing import TypedDict, Annotated

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langgraph.graph.message import add_messages

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage

import sys
from pathlib import Path
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages

sys.path.append(
    str(Path(__file__).resolve().parent.parent.parent.parent)
)
from llm_loader import init_custom_llm

llm = init_custom_llm()

# ----------------------------------
# State
# ----------------------------------

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    need_research: bool
    need_code: bool
    research_done: bool
    code_done: bool
    next: str

# ----------------------------------
# Planner (LLM)
# ----------------------------------

def planner(state: AgentState):

    question = state["messages"][0].content

    prompt = f"""
당신은 작업 계획 전문가입니다.

사용자의 질문을 보고

검색이 필요한지,
코드 작성이 필요한지를 판단하세요.

반드시 아래 형식만 출력하세요.

research=True
code=True

또는

research=True
code=False

질문

{question}
"""

    result = llm.invoke(prompt)

    text = result.content.lower()

    need_research = "research=true" in text
    need_code = "code=true" in text

    print("Planner")
    print(text)

    return {
        "need_research": need_research,
        "need_code": need_code
    }

# ----------------------------------
# Supervisor (Python)
# ----------------------------------

def supervisor(state: AgentState):
    print("\nSupervisor")

    if state["need_research"] and not state["research_done"]:
        print("-> Researcher")

        return {
            "next":"Researcher"
        }

    if state["need_code"] and not state["code_done"]:

        print("-> Coder")

        return {
            "next":"Coder"
        }

    print("-> FINISH")

    return {
        "next":"FINISH"
    }

# ----------------------------------
# Researcher
# ----------------------------------

def researcher(state: AgentState):

    print("\nResearcher")

    question = state["messages"][0].content

    result = llm.invoke(

        f"""
질문을 조사하세요.

{question}

설명만 하세요.
코드는 작성하지 마세요.
"""

    )

    return {

        "messages":[

            AIMessage(

                content=result.content,

                name="Researcher"

            )

        ],

        "research_done":True

    }

# ----------------------------------
# Coder
# ----------------------------------

def coder(state: AgentState):

    print("\nCoder")

    result = llm.invoke(

        state["messages"]

        +

        [

            HumanMessage(
                content="""
Research 결과를 참고하여
Python 코드만 작성하세요.
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
        "code_done":True
    }

# ----------------------------------
# Router
# ----------------------------------

def router(state):
    return state["next"]

# ----------------------------------
# Graph
# ----------------------------------

builder = StateGraph(AgentState)
builder.add_node("Planner", planner)
builder.add_node("Supervisor", supervisor)
builder.add_node("Researcher", researcher)
builder.add_node("Coder", coder)

builder.add_edge(
    START,
    "Planner"
)

builder.add_edge(
    "Planner",
    "Supervisor"

)

builder.add_conditional_edges(
    "Supervisor",
    router,
    {
        "Researcher":"Researcher",
        "Coder":"Coder",
        "FINISH":END
    }

)

builder.add_edge(
    "Researcher",
    "Supervisor"
)

builder.add_edge(
    "Coder",
    "Supervisor"
)

graph = builder.compile()

# ----------------------------------
# 실행
# ----------------------------------

result = graph.invoke(

    {
        "messages":[
            HumanMessage(
                content="파이썬으로 퀵정렬을 구현해줘."
            )
        ],
        "need_research":False,
        "need_code":False,
        "research_done":False,
        "code_done":False,
        "next":""
    }
)

sys.path.append(
    str(Path(__file__).resolve().parent.parent.parent)
)

from util import show_graph
show_graph(graph)

print("\n===========================")

for m in result["messages"]:
    print()
    print(m.name if hasattr(m,"name") else "User")
    print("--------------------------------")
    print(m.content)