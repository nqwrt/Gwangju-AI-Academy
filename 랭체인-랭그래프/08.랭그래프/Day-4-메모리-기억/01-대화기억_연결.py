# |            | 1단계              | 2단계        |
# | ---------- | ---------------- | ---------- |
# | State      | question, answer | messages   |
# | 기억         | ❌ 없음             | ✅ 있음       |
# | 입력         | 문자열              | Message 객체 |
# | LLM 호출     | 질문만 전달           | 전체 대화 전달   |
# | ChatGPT 형태 | ❌                | ✅          |

# LangGraph는 기억을 자동으로 해주는 것이 아님
# State에 무엇을 저장할지 개발자가 설계해야 함


from dotenv import load_dotenv
from typing import TypedDict

from langchain.chat_models import init_chat_model

from langgraph.graph import (
    StateGraph,
    START,
    END
)

import os


import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from llm_loader import init_custom_llm

llm = init_custom_llm()

from dotenv import load_dotenv
from typing import TypedDict

from langchain.chat_models import init_chat_model

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from langgraph.graph import (
    StateGraph,
    START,
    END
)


# ==========================
# State
# ==========================

class State(TypedDict):
    messages: list

# ==========================
# Node
# ==========================

def chatbot(state: State):
    print("\n[Chat Node 실행]")

    response = llm.invoke(
        state["messages"]
    )


    return {
        "messages":[
            AIMessage(
                content=response.content
            )
        ]
    }

# ==========================
# Graph
# ==========================

builder = StateGraph(State)


builder.add_node(
    "chat",
    chatbot
)


builder.add_edge(
    START,
    "chat"
)


builder.add_edge(
    "chat",
    END
)

graph = builder.compile()

from util import show_graph
show_graph(graph)
# ==========================
# Memory
# ==========================

messages = []

# ==========================
# 실행
# ==========================

while True:

    question = input(
        "\n사용자 : "
    )

    if question == "exit":
        break

    # 사용자 메시지 추가
    messages.append(
        HumanMessage(
            content=question
        )
    )

    result = graph.invoke(
        {
            "messages": messages
        }
    )

    # AI 답변
    answer = result["messages"][0].content

    print("AI : ",answer)

    # 대화 기억 추가
    messages.append(
        AIMessage(
            content=answer
        )
    )

