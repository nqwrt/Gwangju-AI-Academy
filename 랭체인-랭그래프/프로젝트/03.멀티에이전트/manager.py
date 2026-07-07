# def manager(state):

#     question = state["question"]

#     if "번역" in question:
#         return "english"

#     elif any(op in question for op in ["+", "-", "*", "/"]):
#         return "math"

#     else:
#         return "general"

def manager(state):

    # 사용자가 입력한 질문 가져오기
    question = state["question"]

    # 번역 관련 질문인지 확인
    if "번역" in question:
        return "english"

    # 계산 관련 질문인지 확인
    elif "+" in question:
        return "math"

    elif "-" in question:
        return "math"

    elif "*" in question:
        return "math"

    elif "/" in question:
        return "math"

    # 위 조건에 해당하지 않으면 일반 질문
    else:
        return "general"