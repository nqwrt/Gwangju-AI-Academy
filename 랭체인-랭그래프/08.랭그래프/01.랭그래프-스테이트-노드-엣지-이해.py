from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import os
from langgraph.graph import StateGraph

load_dotenv()

LLM_MODEL = os.getenv("LLM_AI_MODEL")

# OpenAI 모델 초기화 (OPENAI_API_KEY 환경변수 필요)
llm = init_chat_model(
    LLM_MODEL,
    temperature=0.1,
    max_tokens=1000
    )

# 분기 어렵다
# 반복 어렵다
# 상태 관리 어렵다

# State
#  ↓
# Node
#  ↓
# Edge
#  ↓
# 조건 분기
#  ↓
# Loop

from typing import TypedDict

# TypedDict 클래스를 상속받아 새로운 타입을 정의하는 문법
# TypedDict를 사용하면:

# 데이터 구조를 명확히 정의하여 타입 체크 가능
# IDE의 자동 완성 기능 활용 가능
# 런타임 오류를 사전에 방지
# 코드의 가독성과 유지보수성 향상
from typing import TypedDict


class State(TypedDict):
    value:int

def add_one(state):
    state["value"] += 1
    print("node1 실행")
    return state

def multiply_two(state):
    state["value"] = state["value"] * 2
    print("node2 실행")
    return state

# 직접 실행
state = {"value":10}
state = add_one(state)
print(state)

state = multiply_two(state)
print(state)
############################################
# 위의 내용을 자동연결
from langgraph.graph import StateGraph,START,END


builder = StateGraph(State)
builder.add_node("add",add_one)
builder.add_node("multiply",multiply_two)

builder.add_edge(START,"add")
builder.add_edge("add","multiply")
builder.add_edge("multiply",END)

graph = builder.compile()
result = graph.invoke({"value":10})

print(result)
############################################
# from langgraph.graph import (
#     StateGraph,
#     START,
#     END
# )


# class State(TypedDict):
#     question:str
#     answer:str

# def chatbot(state):
#     state["answer"]="안녕하세요"
#     return state


# builder = StateGraph(State)
# builder.add_node("chat",chatbot)


# builder.add_edge(START,"chat")
# builder.add_edge("chat",END)


# graph = builder.compile()
# result = graph.invoke({"question":"안녕" })
# print(result)

# 마지막 실습 문제

# 문제:

# START
#  ↓
# plus10
#  ↓
# minus5
#  ↓
# END

# 초기값:

# 100

# 결과:

# 105

from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)


# ==========================
# State
# ==========================

class State(TypedDict):
    value: int


# ==========================
# Node1
# ==========================

def plus10(state):
    print("\nplus10 실행")
    state["value"] += 10
    return state


# ==========================
# Node2
# ==========================

def minus5(state):
    print("\nminus5 실행")
    state["value"] -= 5
    return state


# ==========================
# Graph 생성
# ==========================

builder = StateGraph(State)


# Node 등록
builder.add_node("plus10",plus10)
builder.add_node("minus5",minus5)


# 연결
builder.add_edge(START,"plus10")
builder.add_edge("plus10","minus5")
builder.add_edge("minus5",END)

# 컴파일
graph = builder.compile()

# ==========================
# 실행
# ==========================

result = graph.invoke({"value":100})

print("\n최종 결과")
print(result)

# # 시각화
# print(graph.get_graph().draw_mermaid())
# from IPython.display import Image, display
# # 🔥 바로 그림 출력
# display(
#     Image(
#         graph
#         .get_graph()
#         .draw_mermaid_png()
#     )
# )

# import os

# with open(
#     "graph.png",
#     "wb"
# ) as f:

#     f.write(
#         graph
#         .get_graph()
#         .draw_mermaid_png()
#     )


# os.startfile(
#     "graph.png"
# )