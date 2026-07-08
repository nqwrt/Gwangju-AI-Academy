import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
import sys
from pathlib import Path
# 현재 파일 기준으로 3단계 위 폴더를 import 경로에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from llm_loader import init_custom_llm

llm = init_custom_llm()

embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    # model_kwargs={"device": "cpu"},
    # encode_kwargs={"normalize_embeddings": True}
)

# 현재 rag.py가 있는 폴더
BASE_DIR = Path(__file__).resolve().parent

# chroma_db 폴더
DB_PATH = BASE_DIR / "chroma_db"

db = Chroma(
    persist_directory=str(DB_PATH),
    embedding_function=embedding
)

retriever = db.as_retriever(
    search_kwargs={
        "k":3
    }
)

def format_docs(docs):

    result = ""
    for doc in docs:
        result += doc.page_content
        result += "\n\n" # 문서와 문서 사이를 명확하게 구분 하기 위해서. LLM도 문서가 구분되어 있다는 것을 더 명확하게 인식
    return result

# result =

# 연차 규정

# 출장 규정

# 재택근무 규정

# def format_docs(docs):

#     return "\n\n".join(
#         doc.page_content
#         for doc in docs
#     )


prompt = ChatPromptTemplate.from_template(
"""
당신은 회사 규정을 알려주는 AI입니다.

아래 문서를 참고하여 답변하세요.

문서

{context}

질문

{question}
"""
)

chain = prompt | llm | StrOutputParser()


# question = input("질문 : ")
# docs = retriever.invoke(question)
# context = format_docs(docs)
# messages = prompt.invoke({
#     "context": context,
#     "question": question
# })

# response = llm.invoke(messages)
# print(response.content)


def ask(question):

    # 1. 관련 문서 검색
    docs = retriever.invoke(question)

    # 2. 문자열로 변환
    context = format_docs(docs)

    # 3. Chain 실행
    answer = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    return answer