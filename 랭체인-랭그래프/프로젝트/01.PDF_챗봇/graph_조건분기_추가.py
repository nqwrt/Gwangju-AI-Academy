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

# 현재 

# Retriever
# ↓
# 관련 없는 Chunk
# ↓
# GPT
# ↓
# 억지로 답변

# 해결 방법

# 검색 결과가 없으면
# 죄송합니다.
# PDF 안에는 관련 내용이 없습니다.

    #           START
    #              │
    #              ▼
    #         Retrieve
    #              │
    #              ▼
    #      문서가 존재하는가?
    #        │           │
    #     Yes│           │No
    #        ▼           ▼
    #   Generate      No Context
    #        │           │
    #        └─────┬─────┘
    #              ▼
    #             END

class GraphState(TypedDict):
    question:str
    context:str
    answer:str
    has_context: bool


# def retrieve(state:GraphState):

#     #사용자의 질문과 가장 관련 있는 문서를 VectorDB에서 찾아오는 것

#     docs = retriever.invoke(
#         state["question"]
#     )

#     #     docs = [
#     #     Document(page_content="Transformer는 딥러닝 모델입니다."),
#     #     Document(page_content="Attention 메커니즘을 사용합니다."),
#     #     Document(page_content="자연어 처리에서 많이 사용됩니다.")
#     # ]

#     context = ""

#     for doc in docs:
#         context += doc.page_content
#         context += "\n\n"

#     #print("컨텍스트",context)

#     return {
#         "context":context,
#          "has_context": len(docs) > 0
#     }

def retrieve(state):
    print("retrieve 실행")
    
    results = vector_db.similarity_search_with_score(
        state["question"],
        k=3
    )

    #threshold = 0.6
    threshold = 1.5    
    docs = []
    context = ""
    
    print("retrieve 실행",results)

    for doc,score in results:
        print(score)

        if score < threshold:
            docs.append(doc)
            context += doc.page_content
            context += "\n\n"

    return {
        "context":context,
        "has_context":len(docs)>0
    }


def no_context(state: GraphState):
    
    print("[No Context Node 실행]")

    return {
        "answer": "죄송합니다.\nPDF 안에서 관련 내용을 찾지 못했습니다."
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

# LangGraph는
# Node가 아니라
# 함수가 판단함
def router(state: GraphState):
    
    if state["has_context"]:
        return "generate"
    
    return "no_context"

builder = StateGraph(GraphState)

builder.add_node("retrieve",retrieve)
builder.add_node("generate",generate)
builder.add_node("no_context",no_context)

builder.add_edge(START,"retrieve")
builder.add_conditional_edges(
    "retrieve",
    router,
    {
        "generate": "generate",
        "no_context": "no_context"
    }
)
builder.add_edge("generate",END)
builder.add_edge("no_context",END)

graph = builder.compile()


#              START
#                 │
#                 ▼
#            Retrieve
#                 │
#                 ▼
#           route(state)
#          ┌──────┴──────┐
#          ▼             ▼
#    Generate      No Context
#          │             │
#          └──────┬──────┘
#                 ▼
#                END