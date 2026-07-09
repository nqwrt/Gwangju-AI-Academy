########################################################################
# 1. 일반 Python 함수
########################################################################
def add(a, b):
    """
    두 숫자를 더하는 함수
    """
    return a + b

result = add(10, 20)

print("일반 함수 결과")
print(result)

########################################################################
# 2. LangChain Tool 생성
########################################################################
from langchain_core.tools import tool

@tool
def calculator(a:int, b:int):
    """
    두 숫자를 더하는 계산 Tool 입니다.
    
    입력:
    a : 첫 번째 숫자
    b : 두 번째 숫자
    
    출력:
    두 숫자의 합
    """

    return a + b

########################################################################
# 3. Tool 정보 확인
########################################################################
print("Tool 이름")
print(calculator.name)


print("\nTool 설명")
print(calculator.description)

# Tool 직접 실행
result = calculator.invoke(
    {
        "a":10,
        "b":20
    }
)
print(result)

########################################################################
# 4. 여러 Tool 생성
########################################################################


@tool
def multiply(a:int,b:int):
    """
    두 숫자를 곱하는 Tool
    """

    return a*b



@tool
def divide(a:int,b:int):
    """
    두 숫자를 나누는 Tool
    """

    return a/b



tools = [
    calculator,
    multiply,
    divide
]

print("\n등록된 Tool")

for t in tools:
    print(
        t.name
    )

########################################################################
# 5. LLM 연결
########################################################################
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from llm_loader import init_custom_llm

llm = init_custom_llm()

llm_with_tools = llm.bind_tools(
    tools
)

response = llm_with_tools.invoke(
    "10과 20을 더해주세요"
)

print(response)

########################################################################
# 6. Tool Call 확인
########################################################################

if response.tool_calls:
    print("\nTool 호출 발생")
    print(response.tool_calls)
else:
    print("Tool 사용하지 않음")

# 사용자 질문
# "10과 20을 더해줘"

#         |
#         v
#        LLM
#         |
#         |
#    Tool 필요 판단
#         |
#         v
#  calculator Tool
#         |
#         v
#        30
#         |
#         v
#  최종 답변