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


from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
)

# 현재 파이썬 파일이 있는 폴더
BASE_DIR = Path(__file__).resolve().parent #현재 실행 중인 파이썬 파일이 있는 폴더의 절대 경로를

documents = [
    "날짜 : 판매일",
    "지역 : 판매지역",
    "상품 : 상품명",
    "수량 : 판매수량",
    "매출 : 판매금액"
]

# Chroma DB 저장 폴더
DB_PATH = BASE_DIR / "chroma_db"

db = Chroma.from_texts(
    texts=documents,
    embedding=embedding,
    persist_directory=str(DB_PATH)
)

print("Vector DB 저장 완료")