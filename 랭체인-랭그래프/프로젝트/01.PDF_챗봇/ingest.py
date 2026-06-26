# PDF → 작은 조각 → Embedding → Chroma 저장
from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

import os

print("현재 파이썬이 인식하는 위치:", os.getcwd())
print("거기에 ai.pdf가 실제로 있나요?:", os.path.exists("ai.pdf"))

loader = PyPDFLoader(r"D:\광주-인공사\Gwangju-AI-Academy\랭체인-랭그래프\프로젝트\01.PDF_챗봇\샘플_삼성냉장고.pdf")

#문서를 문서 객체로 변환
documents = loader.load()

print("문서 개수 :", len(documents))

# chunk_size
# chunk_size=500

# 의 의미는

# 500글자씩 잘라라

# 입니다.

# 예를 들어

# ABCDEFGHIJK...

# 1000글자라면

# Chunk1

# 1~500

# -------------

# Chunk2

# 501~1000

# 이 됩니다.

# chunk_overlap
# chunk_overlap=100

# 이 옵션은

# 앞의 100글자를 다음 Chunk에도 포함시키라는 의미입니다.

# 예를 들어

# 1000글자라면

# Chunk1

# 1 ~ 500

# 다음은

# Chunk2

# 401 ~ 900

# 입니다.

# 즉
# 100글자
# 겹침
# 이 생깁니다.
# 왜 겹칠까요?

# 예를 들어
# ...
# RAG는
# GPT와
# Vector DB를
# 이용한다.
# ...

# 라는 문장이
# 중간에서 잘려버리면
# Chunk1
# RAG는 GPT와
# Chunk2
# Vector DB를 이용한다.
# 이 되어 문맥이 끊어집니다.
# 그래서
# Chunk1
# RAG는 GPT와 Vector DB를 이용한다.
# Chunk2
# GPT와 Vector DB를 이용한다.
# 처럼 일부를 겹쳐 저장하는 것입니다.
# 이렇게 하면 문맥이 유지되어 검색 품질이 좋아집니다

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500, # 500자씩 짤라라
    chunk_overlap = 100 # 앞의 100글자를 다음 Chunk에도 포함시키라는 의미
)

#문서분활
chunks = splitter.split_documents(documents)

print("Chunk 개수 :", len(chunks))


embedding = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory="chroma_db"
)

print("저장 완료!")

# PDF 파일
#       ↓
# Document 객체(페이지 단위)
#       ↓
# Document 객체(Chunk 단위)
#       ↓
# Embedding
#       ↓
# Vector DB