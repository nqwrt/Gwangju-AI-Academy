# 4교시 실습: Node 만들기 (2시간)
# 학습 목표

# 이번 실습에서는 LangGraph의 핵심인 Node 함수를 이해합니다.

# 배울 내용:

# Node 함수 구조
# Node 입력 (State)
# Node 출력 (변경할 State)
# State 수정
# 여러 개의 Node 연결

# 최종 Workflow:

# START

#  ↓

# Question Node
# (질문 확인)

#  ↓

# Search Node
# (검색)

#  ↓

# Answer Node
# (답변 생성)

#  ↓

# Output Node
# (출력)

#  ↓

# END

# | Node 반환                    | 의미         |
# | -------------------------- | ---------- |
# | `return {}`                | 변경 없음      |
# | `return {"answer":"완료"}`   | answer만 변경 |
# | `return {"count":count+1}` | count 증가   |
# | `return None`              | 오류         |


from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)



# ==================================
# 1. State 정의
# ==================================
class State(TypedDict):
    question: str
    search_result: str
    answer: str

# ==================================
# 2. Question Node
# ==================================

def question_node(state: State):
    print("\n[Question Node]")
    print(
        "질문:",
        state["question"]
    )

    return {
        # 변경 없음
    }



# ==================================
# 3. Search Node
# ==================================

def search_node(state: State):

    print("\n[Search Node]")
    question = state["question"]

    print(
        f"{question} 검색 중..."
    )

    search_result = (
        "LangGraph는 "
        "LLM Workflow를 만드는 "
        "Graph 기반 Framework입니다."
    )


    return {
        "search_result":
        search_result
    }



# ==================================
# 4. Answer Node
# ==================================

def answer_node(state: State):

    print("\n[Answer Node]")
    question = state["question"]
    context = state["search_result"]

    answer = f"""
    질문:
    {question}

    검색 결과:
    {context}

    답변:
    LangGraph는 Node와 Edge를 이용하여 
    Agent Workflow를 만드는 기술입니다.
    """

    return {
        "answer":answer
    }



# ==================================
# 5. Output Node
# ==================================

def output_node(state: State):

    print("\n[Output Node]")

    print("===================")
    print(state["answer"])
    print("===================")

    return {}



# ==================================
# 6. Graph Builder
# ==================================

builder = StateGraph(State)



# Node 등록

builder.add_node(
    "question",
    question_node
)


builder.add_node(
    "search",
    search_node
)


builder.add_node(
    "answer",
    answer_node
)


builder.add_node(
    "output",
    output_node
)



# Edge 연결

builder.add_edge(
    START,
    "question"
)


builder.add_edge(
    "question",
    "search"
)


builder.add_edge(
    "search",
    "answer"
)


builder.add_edge(
    "answer",
    "output"
)


builder.add_edge(
    "output",
    END
)



# Compile

graph = builder.compile()



# ==================================
# 7. 실행
# ==================================

result = graph.invoke(

    {
        "question":
        "LangGraph란 무엇인가?",

        "search_result":
        "",

        "answer":
        ""

    }

)



print("\n최종 State")

print(result)

from IPython.display import Image, display


display(
    Image(
        graph.get_graph()
        .draw_mermaid_png()
    )
)