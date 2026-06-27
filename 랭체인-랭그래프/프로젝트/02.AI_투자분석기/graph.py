from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END

from tools import extract_company
from tools import get_finance
from tools import get_news

from llm_loader import init_custom_llm

# ------------------------------------------
# LLM
# ------------------------------------------

llm = init_custom_llm()

print("LLM 로드 완료")


# ------------------------------------------
# Graph State
# ------------------------------------------

class GraphState(TypedDict):

    question: str

    company: str

    finance: str

    news: str

    answer: str


# ------------------------------------------
# 회사명 추출
# ------------------------------------------

def company_node(state: GraphState):

    print("회사명 추출")

    company = extract_company(
        state["question"]
    )

    return {
        "company": company
    }


# ------------------------------------------
# 재무 조회
# ------------------------------------------

def finance_node(state: GraphState):

    print("재무정보 조회")

    finance = get_finance(
        state["company"]
    )

    return {
        "finance": finance
    }


# ------------------------------------------
# 뉴스 조회
# ------------------------------------------

def news_node(state: GraphState):

    print("뉴스 조회")

    news = get_news(
        state["company"]
    )

    return {
        "news": news
    }


# ------------------------------------------
# GPT 분석
# ------------------------------------------

def analyze_node(state: GraphState):

    print("GPT 분석")

    prompt = f"""
당신은 전문 투자 애널리스트입니다.

아래 정보를 참고하여

1. 기업 소개

2. 재무 상태

3. 최근 뉴스 요약

4. 투자 장점

5. 투자 위험성

6. 최종 투자 의견

을 작성하세요.

----------------------------

회사명

{state["company"]}

----------------------------

재무정보

{state["finance"]}

----------------------------

최근 뉴스

{state["news"]}

----------------------------

사용자 질문

{state["question"]}

"""

    response = llm.invoke(prompt)

    return {

        "answer": response.content

    }


# ------------------------------------------
# Graph 생성
# ------------------------------------------

builder = StateGraph(GraphState)

builder.add_node(
    "company",
    company_node
)

builder.add_node(
    "finance",
    finance_node
)

builder.add_node(
    "news",
    news_node
)

builder.add_node(
    "analyze",
    analyze_node
)

builder.add_edge(
    START,
    "company"
)

builder.add_edge(
    "company",
    "finance"
)

builder.add_edge(
    "finance",
    "news"
)

builder.add_edge(
    "news",
    "analyze"
)

builder.add_edge(
    "analyze",
    END
)

graph = builder.compile()


print("Graph 생성 완료")