########################################################################
# 1. Calculator Tool
########################################################################

from langchain_core.tools import tool


@tool
def calculator(a:int, b:int):
    """
    두 숫자를 더하는 계산 Tool입니다.
    """
    return a + b

tools = [
    calculator
]
########################################################################
# 2. LangChain Tool 생성
########################################################################
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from llm_loader import init_custom_llm

llm = init_custom_llm()
llm_with_tools = llm.bind_tools(
    tools
)
########################################################################
# 3. 사용자 질문
########################################################################
from langchain_core.messages import (
    HumanMessage,
    SystemMessage
)

messages = [
    SystemMessage(
        content="""
        당신은 AI Assistant입니다.

        계산이 필요하면
        반드시 calculator Tool을 사용하세요.
        """
    ),
    HumanMessage(
        content="123과 456을 더해주세요"
    )
]
########################################################################
# 4. 첫 번째 LLM 호출
########################################################################
response = llm_with_tools.invoke(
    messages
)

print(response)

# 예상 결과:

# AIMessage

# tool_calls=[
#  {
#   name:"calculator",
#   args:{
#        a:123,
#        b:456
#   },
#   id:"call_xxxx"
#  }
# ]
########################################################################
# 5. Tool Call 확인
########################################################################
if response.tool_calls:
    print("Tool 호출 발생")

    for call in response.tool_calls:
        print("================")
        print(
            "Tool 이름:",
            call["name"]
        )
        print(
            "입력값:",
            call["args"]
        )
        print(
            "ID:",
            call["id"]
        )
########################################################################
# 6. Tool 실행
########################################################################
tool_call = response.tool_calls[0]

tool_result = calculator.invoke(
    tool_call["args"]
)

print(tool_result)
########################################################################
# 7. Tool 결과 전달
# Tool 실행 결과를 LLM에게 다시 알려줍니다.
########################################################################
from langchain_core.messages import ToolMessage

messages.append(response)
messages.append(
    ToolMessage(
        content = str(tool_result),
        tool_call_id = tool_call["id"]
    )
)

########################################################################
# 8. 두 번째 LLM 호출
########################################################################
final_response = llm_with_tools.invoke(
    messages
)

print(final_response.content)

# 123과 456의 합은 579입니다.

########################################################################
# Agent Flow
# 전체 Agent 흐름 코드
########################################################################

response = llm_with_tools.invoke(
    messages
)

if response.tool_calls:
    messages.append(response)

    for tool_call in response.tool_calls:
        result = calculator.invoke(tool_call["args"])

        # LLM은 Tool의 실행 결과를 직접 알 수 없기 때문에 
        # ToolMessage를 통해 결과를 다시 알려줘야 함
        # LLM야.

        # 네가 요청했던 calculator Tool 실행했어.
        # 결과는
        # 579
        # 야.
        messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id = tool_call["id"]

            )
        )
    final = llm.invoke(
        messages
    )
    print(final.content)

        #         사용자

        #           |
        #           v

        #       HumanMessage

        #           |
        #           v

        #          LLM

        #           |
        #   Tool 필요 판단

        #           |
        #           v

        #      tool_calls

        #           |
        #           v

        #   +---------------+
        #   | Calculator    |
        #   +---------------+

        #           |
        #           v

        #       ToolMessage

        #           |
        #           v

        #          LLM

        #           |
        #           v

        #       최종 답변
