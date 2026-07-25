from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from llm_loader import init_custom_llm

llm = init_custom_llm()


class ChatState(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: ChatState):

    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }


builder = StateGraph(ChatState)

builder.add_node("ChatBot", chatbot)

builder.add_edge(START, "ChatBot")
builder.add_edge("ChatBot", END)

graph = builder.compile()