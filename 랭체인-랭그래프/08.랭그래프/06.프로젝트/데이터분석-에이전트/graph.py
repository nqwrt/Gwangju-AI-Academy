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

    prompt = f"""
    당신은 데이터 분석 전문가입니다.

    아래 중 하나만 출력하세요.

    EDA
    GROUP
    FILTER
    PLOT
    STATISTICS
    ML

    질문

    {state["question"]}
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

    prompt = f"""
    질문

    {state["question"]}

    sklearn 코드 작성

    result 변수에 저장하세요.
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
        return match.group(1).strip()
    
    state["code"].strip()
    
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