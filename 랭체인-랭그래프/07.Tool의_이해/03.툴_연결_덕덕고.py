# pip install langchain
# pip install langchain-openai
# pip install langchain-community
# pip install -U ddgs


from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    ToolMessage
)


########################################################################
# 1. DuckDuckGo Tool 생성
########################################################################

duck = DuckDuckGoSearchRun()


@tool
def web_search(query: str):
    """
    인터넷에서 최신 정보를 검색하는 도구입니다.

    사용 조건:
    - 오늘
    - 현재
    - 최신
    - 뉴스
    - 주가
    - 환율
    - 날씨
    - 최근 발표
    - 최근 출시
    - 실시간 정보

    일반 지식 질문에는 사용하지 않습니다.
    """

    return duck.run(query)



tools = [
    web_search
]


########################################################################
# 2. GPT 생성
########################################################################

import sys
from pathlib import Path


sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from llm_loader import init_custom_llm


llm = init_custom_llm()

llm_with_tools = llm.bind_tools(
    tools
)



########################################################################
# 3. System Prompt
########################################################################


system = SystemMessage(
    content="""

당신은 AI Assistant입니다.

규칙:

1. 일반적인 지식 질문은 Tool을 사용하지 않습니다.

2. 최신 정보가 필요한 경우 반드시 web_search Tool을 사용합니다.


최신 정보 예:

- 오늘
- 현재
- 최신
- 뉴스
- 환율
- 주가
- 날씨
- 최근 발표
- 최근 출시
- 실시간 정보


검색 결과를 그대로 출력하지 말고
사용자가 이해하기 쉽게 요약합니다.

"""
)



########################################################################
# 4. 사용자 질문
########################################################################


question = input(
    "질문 : "
)


messages = [
    system,
    HumanMessage(
        content=question
    )
]



########################################################################
# 5. LLM 실행
########################################################################


response = llm_with_tools.invoke(
    messages
)



########################################################################
# 6. Tool 호출 확인
########################################################################


if response.tool_calls:


    print("\n[Tool 호출]")
    print(response.tool_calls)



    messages.append(
        response
    )


    for tool_call in response.tool_calls:


        if tool_call["name"] == "web_search":


            print(
                "\nDuckDuckGo 검색 중...\n"
            )


            ############################################################
            # 최신 LangChain 방식
            ############################################################

            query = tool_call["args"].get(
                "query"
            )


            result = web_search.invoke(
                {
                    "query": query
                }
            )


            print(result)



            messages.append(
                ToolMessage(
                    content=result,
                    tool_call_id=tool_call["id"]
                )
            )



    ####################################################################
    # 7. 검색 결과 포함 최종 답변
    ####################################################################


    final = llm_with_tools.invoke(
        messages
    )


    print(
        "\n=============================="
    )
    print(
        "최종 답변"
    )
    print(
        "=============================="
    )


    print(
        final.content
    )



########################################################################
# 8. Tool 필요 없는 질문
########################################################################


else:


    print(
        "\n=============================="
    )

    print(
        "Tool 사용 안 함"
    )

    print(
        "=============================="
    )


    print(
        response.content
    )