"""
======================================================
graph.py

LangGraph Tool Calling Agent

- GPT-5
- Tool Calling
- StateGraph
- ToolNode
- Streaming
======================================================
"""

from dotenv import load_dotenv

load_dotenv()

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langgraph.graph.message import add_messages

from langgraph.prebuilt import ToolNode

from langchain.chat_models import init_chat_model

from tools import TOOLS


# =====================================================
# State
# =====================================================

class AgentState(TypedDict):

    # 대화 저장
    messages: Annotated[list, add_messages]


# =====================================================
# LLM
# =====================================================

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from llm_loader import init_custom_llm

llm = init_custom_llm()

# Tool Binding
llm = llm.bind_tools(TOOLS)


# =====================================================
# Chatbot Node
# =====================================================

def chatbot(state: AgentState):

    response = llm.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# =====================================================
# Tool Node
# =====================================================

tool_node = ToolNode(TOOLS)


# =====================================================
# Conditional Edge
# =====================================================

def should_continue(state: AgentState):

    last_message = state["messages"][-1]

    # Tool 호출 여부 확인
    if getattr(last_message, "tool_calls", None):
        return "tools"

    return END


# =====================================================
# Graph Builder
# =====================================================

builder = StateGraph(AgentState)

builder.add_node(
    "chatbot",
    chatbot
)

builder.add_node(
    "tools",
    tool_node
)

# START → chatbot
builder.add_edge(
    START,
    "chatbot"
)

# chatbot → tools / END
builder.add_conditional_edges(
    "chatbot",
    should_continue
)

# tools → chatbot
builder.add_edge(
    "tools",
    "chatbot"
)

# Compile
graph = builder.compile()


# =====================================================
# Mermaid 출력
# =====================================================

def print_mermaid():
    print()
    print("=" * 60)
    print(graph.get_graph().draw_mermaid())
    print("=" * 60)
    print()


# =====================================================
# PNG 저장 (선택)
# =====================================================

def save_png(filename="graph.png"):

    try:

        png = graph.get_graph().draw_mermaid_png()

        with open(filename, "wb") as f:
            f.write(png)

        print(f"그래프 저장 완료 : {filename}")

    except Exception as e:
        print("PNG 저장 실패")
        print(e)


# =====================================================
# Invoke 테스트
# =====================================================

def invoke(question: str):
    result = graph.invoke(
        {
            "messages": [
                (
                    "user",
                    question
                )
            ]
        }
    )

    print()
    print("질문")
    print(question)
    print()
    print("답변")
    print(result["messages"][-1].content)
    print()

# =====================================================
# Streaming
# =====================================================

def stream(question: str):
    print()
    print("=" * 60)
    print("Streaming")
    print("=" * 60)

    for chunk in graph.stream(
        {
            "messages": [
                (
                    "user",
                    question
                )
            ]
        },
        stream_mode="updates"
    ):
        print()
        print(chunk)


# =====================================================
# Main
# =====================================================

if __name__ == "__main__":

    print_mermaid()
    # save_png()
    invoke("10 + 20 * 3 계산해줘.")
    invoke("오늘 날짜 알려줘.")
    invoke("현재 시간이 뭐야?")
    
    stream("삼성전자 오늘 주가는?")

    #stream("100 / 5 계산해줘.")

#            START
#              │
#              ▼
#       +---------------+
#       |   chatbot     |
#       +---------------+
#              │
#       tool_calls?
#       ┌──────┴──────┐
#       │             │
#       ▼             ▼
# +--------------+    END
# |   ToolNode   |
# +--------------+
#       │
#       ▼
# +---------------+
# |   chatbot     |
# +---------------+
#       │
#       ▼
#      END