from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()

LLM_MODEL = os.getenv("LLM_AI_MODEL")

# OpenAI 모델 초기화 (OPENAI_API_KEY 환경변수 필요)
llm = init_chat_model(
    LLM_MODEL,
    temperature=0.1,
    max_tokens=1000
    )

# 1. RAG를 쓰는 이유 (핵심 3가지)
# ❌ LLM의 한계

# 1. 최신 정보 모름
# 2. 회사 내부 데이터 모름
# 3. hallucination (그럴듯한 거짓말)

# 2. RAG 구조 (가장 중요)
# User Query
#    ↓
# Retriever (검색)
#    ↓
# Vector DB (문서 검색)
#    ↓
# Relevant Context
#    ↓
# LLM
#    ↓
# Answer

# 3. 전체 그림 (실무 구조)

#             ┌──────────────┐
# User ─────▶ │  Query       │
#             └─────┬────────┘
#                   ↓
#         ┌────────────────────┐
#         │ Vector DB 검색     │
#         │ (FAISS / Chroma)   │
#         └────────┬───────────┘
#                  ↓
#         관련 문서(Context)
#                  ↓
#         ┌──────────────────┐
#         │     LLM          │
#         │ + Context        │
#         └──────────────────┘
#                  ↓
#               Answer

# pip install -U langchain langchain-community langchain-openai langchain-text-splitters langchain-core
# pip install langchain-faiss

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
from langchain_faiss import FAISS

# 🔥 문서
docs = [
    Document(page_content="Django는 Python 웹 프레임워크이다."),
    Document(page_content="React는 프론트엔드 라이브러리이다."),
    Document(page_content="LangChain은 LLM 애플리케이션 프레임워크이다.")
]


# 문서(Docs)
#    ↓
# Chunking (잘게 나눔)
#    ↓
# Embedding (숫자로 변환)
#    ↓
# FAISS(Vector DB 저장)
#    ↓
# Retriever (검색기)
#    ↓
# 질문 → 유사 문서 찾기


# 🔥 Chunking
splitter = CharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=10
)

split_docs = splitter.split_documents(docs)


# 🔥 Embedding (중요: API KEY 필요)
emb = OpenAIEmbeddings()


# 🔥 FAISS DB 생성
db = FAISS.from_documents(split_docs, emb)


# 🔥 Retriever 생성
retriever = db.as_retriever()


# =========================
# 🔥 테스트 코드 (핵심)
# =========================

query = "LangChain이 뭐야?"

results = retriever.invoke(query)

print("\n=== 검색 결과 ===\n")

for i, doc in enumerate(results):
    print(f"[{i}] {doc.page_content}")