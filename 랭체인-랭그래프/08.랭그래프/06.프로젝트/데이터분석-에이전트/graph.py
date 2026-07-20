import matplotlib.pyplot as plt

from langgraph.graph import StateGraph
from langgraph.graph import START, END

from langchain.chat_models import init_chat_model
from state import AnalysisState
from tools import *


# ----------------------
# LLM
# ----------------------
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent.parent.parent)
)

from llm_loader import init_custom_llm

llm = init_custom_llm()


import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


# ----------------------
# CSV
# ----------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sales.csv"

print(DATA_PATH)
df = load_csv(str(DATA_PATH))
#print(df)

# ----------------------
# Question
# ----------------------

def question_node(state: AnalysisState):
    
    print("=" * 60)
    print(state["question"])

    state["dataframe"] = df
    
    return state


# ----------------------
# Planner
# ----------------------

def planner_node(state):

    # prompt = f"""
    # 당신은 데이터 분석 전문가입니다.

    # 아래 중 하나만 출력하세요.

    # EDA
    # GROUP
    # FILTER
    # PLOT
    # STATISTICS
    # ML

    # 질문

    # {state["question"]}
    # """
    
    prompt = f"""
당신은 데이터 분석 작업을 분류하는 Planner Agent입니다.

사용자의 질문을 보고 가장 적합한 분석 작업 유형 하나만 선택하세요.

반드시 아래 단어 중 하나만 출력하세요.

EDA
GROUP
FILTER
PLOT
STATISTICS
ML


분석 유형 판단 기준:

1. EDA
- 데이터 전체 구조를 파악하는 질문
- 데이터 개수, 컬럼, 결측치, 기본 통계 확인
예)
"데이터를 분석해줘"
"컬럼 정보를 알려줘"
"결측치를 확인해줘"


2. GROUP
- 특정 기준으로 데이터를 묶어서 집계하는 질문
- "별", "마다", "단위로", "그룹별", "월별", "년도별", "지역별", "상품별"
- sum, count, average 같은 집계가 필요한 경우

예)
"월별 매출은?"
"지역별 판매량은?"
"상품별 매출 합계를 알려줘"
"년도별 평균 매출"


3. FILTER
- 특정 조건에 맞는 데이터 조회
- 조건 검색
- 특정 값 또는 범위 선택

예)
"서울 데이터만 보여줘"
"매출 100만원 이상만 보여줘"
"2025년 데이터만 조회"


4. PLOT
- 그래프 생성 요청

예)
"매출 그래프 보여줘"
"월별 추이를 차트로 만들어줘"


5. STATISTICS
- 통계 분석 요청
- 상관관계, 평균, 분산, 가설검정 등

예)
"매출 평균은?"
"상관관계를 분석해줘"
"두 그룹 차이가 유의미한가?"


6. ML
- 머신러닝 관련 요청

예)
"매출을 예측해줘"
"지역을 군집화해줘"


판단 규칙:

- "~별", "~마다", "~단위", "~별 합계"가 있으면 GROUP
- 날짜 기준(월, 년, 분기, 일)으로 집계하면 GROUP
- 그래프 요청이 있으면 PLOT
- 조건으로 데이터를 선택하면 FILTER
- 예측/분류/군집이면 ML


질문:
{state["question"]}


출력:
분석 유형 이름 하나만 출력하세요.
"""

    state["analysis_type"] = (
        llm.invoke(prompt)
        .content
        .strip()
        .upper()
    )

    print("분석 planner_node",state["analysis_type"])

    return state


# ----------------------
# Router
# ----------------------

def router(state):
    return state["analysis_type"]


# ----------------------
# EDA
# ----------------------

def eda_node(state):
    state["result"] = run_eda(state["dataframe"])
    return state


# ----------------------
# GROUP
# ----------------------

def group_node(state):

    prompt = f"""
    DataFrame 이름은 df 입니다.

    컬럼

    {list(df.columns)}

    질문

    {state["question"]}

    pandas 코드만 작성하세요.
    반드시 result 변수에 저장하세요.

    반드시 Python 코드만 출력하세요.
    설명하지 마세요.
    Markdown 코드 블록(```python)을 사용하지 마세요.

    예)
    result=df.groupby("상품")["매출"].sum()
    """

    state["code"] = llm.invoke(prompt).content
    return state


# ----------------------
# FILTER
# ----------------------

def filter_node(state):

    prompt = f"""
    DataFrame 이름은 df 입니다.

    컬럼

    {list(df.columns)}

    질문

    {state["question"]}

    result 변수에 저장하는 pandas 코드만 출력하세요.
    """

    state["code"] = llm.invoke(prompt).content

    return state


# ----------------------
# PLOT
# ----------------------

def plot_node(state):

    prompt = f"""
    DataFrame 이름은 df 입니다.

    컬럼

    {list(df.columns)}

    질문

    {state["question"]}

    matplotlib 코드 작성
    plt.show() 포함

    """

    state["code"] = llm.invoke(prompt).content
    return state


# ----------------------
# Statistics
# ----------------------

def statistics_node(state):

    prompt = f"""
    질문

    {state["question"]}

    result 변수에 저장하는 코드만 작성하세요.
    """

    state["code"] = llm.invoke(prompt).content

    return state


# ----------------------
# ML
# ----------------------

def ml_node(state):

    # prompt = f"""
    # 질문

    # {state["question"]}

    # sklearn 코드 작성

    # result 변수에 저장하세요.
    # """

    prompt = f"""
    당신은 머신러닝 전문가입니다.

    현재 DataFrame(df)가 이미 존재합니다.

    컬럼

    {list(df.columns)}

    사용자 질문

    {state["question"]}

    규칙

    - 반드시 기존 df만 사용하세요.
    - 절대로 새로운 데이터를 생성하지 마세요.
    - np.random 사용 금지
    - pd.DataFrame 생성 금지
    - CSV 읽기 금지
    - 예제 데이터 생성 금지
    - 가능한 기존 컬럼을 이용하세요.
    - 머신러닝 입력(X)은 df의 컬럼으로 만드세요.
    - 숫자가 아닌 컬럼은 LabelEncoder 또는 OneHotEncoder를 사용하세요.
    - 결과는 result 변수에 저장하세요.
    - 실행 가능한 Python 코드만 출력하세요.
    - 설명은 출력하지 마세요.
    - ```python 코드블록도 출력하지 마세요.
    """

    state["code"] = llm.invoke(prompt).content

    return state


# ----------------------
# Execute
# ----------------------

def execute_node(state):
    
    #print("*******************",state)
    #print(state["dataframe"])
    print("execute_node 엑셔큐트 코드",state["code"])
    
    try:

        state["result"] = execute_python(
            state["dataframe"],
            state["code"]
        )

    except Exception as e:
        state["error"] = str(e)
        state["result"] = "실패"

    return state


# ----------------------
# Summary
# ----------------------

def summary_node(state):

    prompt = f"""
    질문

    {state["question"]}

    결과

    {state["result"]}

    사용자에게 설명하세요.
    """

    state["result"] = llm.invoke(prompt).content
    return state

import re


def extract_python_code_node(state):

    pattern = r"```(?:python)?\s*(.*?)```"

    match = re.search(
        pattern,
        state["code"],
        re.DOTALL
    )

    if match:
        state["code"] = match.group(1).strip()
    else:
        state["code"] = state["code"].strip()
    
    return state

# ----------------------
# Graph
# ----------------------

builder = StateGraph(AnalysisState)
builder.add_node("question", question_node)
builder.add_node("planner", planner_node)
builder.add_node("eda", eda_node)
builder.add_node("group", group_node)
builder.add_node("filter", filter_node)
builder.add_node("plot", plot_node)
builder.add_node("statistics", statistics_node)
builder.add_node("ml", ml_node)

builder.add_node("extract_python_code", extract_python_code_node)

builder.add_node("execute", execute_node)
builder.add_node("summary", summary_node)

builder.add_edge(START, "question")
builder.add_edge("question", "planner")

builder.add_conditional_edges(
    "planner",
    router,
    {
        "EDA": "eda",
        "GROUP": "group",
        "FILTER": "filter",
        "PLOT": "plot",
        "STATISTICS": "statistics",
        "ML": "ml",
    }

)

builder.add_edge("eda", "summary")
# builder.add_edge("group", "execute")
# builder.add_edge("filter", "execute")
# builder.add_edge("plot", "execute")
# builder.add_edge("statistics", "execute")
# builder.add_edge("ml", "execute")

builder.add_edge("group", "extract_python_code")
builder.add_edge("filter", "extract_python_code")
builder.add_edge("plot", "extract_python_code")
builder.add_edge("statistics", "extract_python_code")
builder.add_edge("ml", "extract_python_code")
builder.add_edge(
    "extract_python_code",
    "execute"
)

builder.add_edge("execute", "summary")
builder.add_edge("summary", END)

graph = builder.compile()