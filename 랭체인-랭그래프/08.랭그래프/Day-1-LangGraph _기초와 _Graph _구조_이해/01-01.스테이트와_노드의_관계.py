#pip install grandalf
"""
=========================================================
02_input.py

2교시
주제 : Node의 입력(State)

학습목표
---------------------------------------------------------
1. Node의 입력은 항상 State이다.
2. State는 Dictionary이다.
3. Node는 State를 읽어서 필요한 작업을 한다.
4. Node는 입력받은 State를 변경하여 반환한다.
=========================================================
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# =====================================================
# State 정의
# =====================================================

class State(TypedDict):
    name: str
    age: int
    score: int


# =====================================================
# Node
# =====================================================

def print_student(state: State):

    print("=" * 60)
    print("Node 실행")
    print("=" * 60)

    print("\n① Node가 받은 State")
    print(state)

    print("\n② State 타입")
    print(type(state))

    print("\n③ 값 읽기")
    print("이름 :", state["name"])
    print("나이 :", state["age"])
    print("점수 :", state["score"])

    print("\n④ 점수 10점 추가")

    new_score = state["score"] + 10

    print("기존 점수 :", state["score"])
    print("변경 점수 :", new_score)

    print("\n⑤ 새로운 State 반환")

    return {
        "name": state["name"],
        "age": state["age"],
        "score": new_score
    }


# =====================================================
# Graph 생성
# =====================================================

builder = StateGraph(State)

builder.add_node("student", print_student)
builder.add_edge(START, "student")
builder.add_edge("student", END)

graph = builder.compile()


# =====================================================
# Graph 구조 출력
# =====================================================

print("=" * 60)
print("Graph 구조")
print("=" * 60)

print(graph.get_graph().draw_ascii())


# =====================================================
# 실행
# =====================================================

print("\n")
print("=" * 60)
print("Graph 실행")
print("=" * 60)

result = graph.invoke(
    {
        "name": "홍길동",
        "age": 20,
        "score": 90
    }
)

print("\n")
print("=" * 60)
print("최종 결과")
print("=" * 60)

print(result)

# 실습 문제
# 문제 1

# 학생 이름을 자신의 이름으로 변경하세요.

# "name": "홍길동"

# ↓

# "name": "김철수"
# 문제 2

# 점수를 30점 증가시키세요.

# new_score = state["score"] + 30
# 문제 3

# 나이도 1살 증가시키세요.

# 문제 4

# 이름을 대문자로 출력하세요.

# 문제 5

# 새로운 State에 "grade"를 추가하여 점수가 90점 이상이면 "A"를 저장하고, 그렇지 않으면 "B"를 저장하도록 수정해 보세요.

# 이 2교시를 마치면 학생들은 다음을 명확히 이해하게 됩니다.

# Node는 입력을 하나(State)만 받는다.
# State는 딕셔너리(dict) 이다.
# Node는 State를 읽고 필요한 작업을 수행한다.
# Node는 변경된 State를 반환하여 다음 Node로 전달한다.