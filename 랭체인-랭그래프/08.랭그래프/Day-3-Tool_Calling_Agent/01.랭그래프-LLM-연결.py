from dotenv import load_dotenv
from typing import TypedDict
from langchain.chat_models import (
    init_chat_model
)

from langgraph.graph import (
    StateGraph,
    START,
    END
)

import os

# ==========================
# 환경변수
# ==========================

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from llm_loader import init_custom_llm

llm = init_custom_llm()

# ==========================
# State
# ==========================

class State(TypedDict):
    question:str
    answer:str

# ==========================
# Node
# ==========================

def chatbot(state):

    print()
    print("LLM 실행")

    res = llm.invoke(state["question"])
    state["answer"] = (res.content)
    return state


# ==========================
# Graph
# ==========================

builder = StateGraph(State)
builder.add_node("chat",chatbot)

builder.add_edge(START,"chat")
builder.add_edge("chat",END)
graph = builder.compile()


# ==========================
# 실행
# ==========================

# result = graph.invoke(
#     {
#         "question":"파이썬 설명해줘"
#     }
# )

# print()
# print(result["answer"])

while True:

    question = input("질문 :")
    if question == "exit":
        break
    
    result = graph.invoke(
        {
            "question":question
        }
    )

    print()
    print(result["answer"])
