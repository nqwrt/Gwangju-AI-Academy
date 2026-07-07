from langgraph.graph import StateGraph, END

from state import AgentState
from manager import manager
from agents import (
    math_agent,
    english_agent,
    general_agent
)

builder = StateGraph(AgentState)

builder.add_node("math", math_agent)
builder.add_node("english", english_agent)
builder.add_node("general", general_agent)

builder.set_conditional_entry_point(
    manager,
    {
        "math": "math",
        "english": "english",
        "general": "general"
    }
)

builder.add_edge("math", END)
builder.add_edge("english", END)
builder.add_edge("general", END)

graph = builder.compile()