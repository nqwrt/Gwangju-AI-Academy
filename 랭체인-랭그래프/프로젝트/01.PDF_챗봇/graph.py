from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from llm_loader import init_custom_llm

# 깔끔하게 LLM 초기화 완료!
llm = init_custom_llm()

# 이후에 체인(Chain)을 구성하거나 llm.invoke() 등을 사용하시면 됩니다.
print(f"LLM 모델 로드 완료")

from pathlib import Path
import os

from pathlib import Path
import os

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "chroma_db"

print("=" * 50)
print("현재 작업폴더 :", os.getcwd())
print("graph.py 위치 :", BASE_DIR.resolve())
print("DB 위치 :", DB_PATH.resolve())
print("=" * 50)


embedding = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding
)

retriever = vector_db.as_retriever(
    search_kwargs={
        "k":3 # 가장 비슷한 Chunk 3개
    }
)

class GraphState(TypedDict):
    question:str
    context:str
    answer:str


def retrieve(state:GraphState):

    #사용자의 질문과 가장 관련 있는 문서를 VectorDB에서 찾아오는 것

    docs = retriever.invoke(
        state["question"]
    )

    #     docs = [
    #     Document(page_content="Transformer는 딥러닝 모델입니다."),
    #     Document(page_content="Attention 메커니즘을 사용합니다."),
    #     Document(page_content="자연어 처리에서 많이 사용됩니다.")
    # ]

    context = ""

    for doc in docs:
        context += doc.page_content
        context += "\n\n"

    #print("컨텍스트",context)

    return {
        "context":context
    }


def generate(state:GraphState):

    prompt = f"""
    당신은 PDF 문서를 분석하는 AI입니다.

    문서
    {state["context"]}

    질문
    {state["question"]}

    답변
    """

    response = llm.invoke(
        prompt
    )

    return {
        "answer":response.content
    }


builder = StateGraph(GraphState)

builder.add_node("retrieve",retrieve)
builder.add_node("generate",generate)

builder.add_edge(START,"retrieve")
builder.add_edge("retrieve","generate")
builder.add_edge("generate",END)

graph = builder.compile()


# START
#    │
#    ▼
# Retrieve
#    │
#    ▼
# 관련 문서가 있는가?
#    │
#  ┌─┴──────────┐
#  │             │
#  ▼             ▼
# Generate    Rewrite Query
#  │             │
#  └──────┬──────┘
#         ▼
#       Generate
#         │
#         ▼
#        END