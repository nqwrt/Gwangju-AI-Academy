from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)
import sys
from pathlib import Path
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages

sys.path.append(
    str(Path(__file__).resolve().parent.parent.parent)
)
from llm_loader import init_custom_llm

llm = init_custom_llm()


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):

    response = llm.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


builder = StateGraph(State)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

#memory = InMemorySaver()
#pip install langgraph-checkpoint-sqlite
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

DB_PATH = Path(__file__).parent / "chat.db"

conn = sqlite3.connect(
    DB_PATH,
    check_same_thread=False
)

memory = SqliteSaver(conn)

graph = builder.compile(
    checkpointer=memory
)

config = {
    "configurable": {
        "thread_id": "user1"
    }
}

while True:

    question = input("질문 : ")

    if question == "exit":
        break

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(question)
            ]
        },
        config=config
    )

    print(result["messages"][-1].content)

    
