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


# ==========================
# State
# ==========================

class State(TypedDict):
    question: str
    answer: str


# ==========================
# Node
# ==========================

def chatbot(state: State):

    print("\n[Chat Node 실행]")

    response = llm.invoke(
        state["question"]
    )

    return {
        "answer": response.content
    }

# ==========================
# Graph 생성
# ==========================

builder = StateGraph(State)


# Node 추가
builder.add_node(
    "chat",
    chatbot
)


# Edge 연결

builder.add_edge(
    START,
    "chat"
)


builder.add_edge(
    "chat",
    END
)


# Compile

graph = builder.compile()

from util import show_graph
show_graph(graph)
# ==========================
# 실행
# ==========================

while True:

    question = input(
        "\n질문(exit 종료) : "
    )


    if question == "exit":
        break


    result = graph.invoke(
        {
            "question": question
        }
    )


    print(
        "\n답변 : ",
        result["answer"]
    )