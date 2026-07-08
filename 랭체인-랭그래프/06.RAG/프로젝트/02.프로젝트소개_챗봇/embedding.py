from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

import sys
from pathlib import Path
from pydantic import BaseModel

# sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
# from llm_loader import init_custom_llm

# llm = init_custom_llm()

from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    # model_kwargs={"device": "cpu"},
    # encode_kwargs={"normalize_embeddings": True}
)

print(os.getcwd())

# 현재 파이썬 파일이 있는 폴더
BASE_DIR = Path(__file__).resolve().parent #현재 실행 중인 파이썬 파일이 있는 폴더의 절대 경로를

documents = []

for pdf_file in BASE_DIR.glob("*.pdf"):
    loader = PyPDFLoader(str(pdf_file))
    documents.extend(loader.load())

print(len(documents))
print(f"PDF 페이지 수 : {len(documents)}")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100 # 앞뒤로 100글자 겹치게  #chunk_size의 10~20% 정도
)
docs = splitter.split_documents(documents)
print(f"Chunk 개수 : {len(docs)}")


# Chroma DB 저장 폴더
DB_PATH = BASE_DIR / "chroma_db"

db = Chroma.from_documents(
    documents=docs,
    embedding=embedding,
    persist_directory=str(DB_PATH)
)

print("Vector DB 저장 완료")