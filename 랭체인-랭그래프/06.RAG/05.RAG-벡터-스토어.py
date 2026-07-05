#pip install langchain-community faiss-cpu

# | 모델                                      | 특징                | 추천    |
# | ---------------------------------------- | ----------------- | ----- |
# | `BAAI/bge-m3`                            | 다국어 지원, 한국어 성능 우수 | ⭐⭐⭐⭐⭐ |
# | `BAAI/bge-small-en-v1.5`                 | 영어 전용, 가벼움        | ⭐⭐⭐   |
# | `sentence-transformers/all-MiniLM-L6-v2` | 매우 빠름, 영어 중심      | ⭐⭐⭐⭐  |
# | `intfloat/multilingual-e5-base`          | 다국어 지원, 한국어 성능 좋음 | ⭐⭐⭐⭐  |

from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3"
)

sentences = [
    "고양이",
    "강아지",
    "자동차"
]

vectors = embedding.embed_documents(sentences)

#====================================================
# from langchain_community.vectorstores import FAISS
# # FAISS 생성
# db = FAISS.from_texts(
#     texts=sentences,
#     embedding=embedding
# )


# print("문서 개수 :", db.index.ntotal)


# # 4. 점수까지 보기
# query = "고양이"

# docs = db.similarity_search_with_score(query)

# for doc, score in docs:
#     print("=" * 50)
#     print(doc.page_content)
#     print("거리 :", score)

# for i in range(len(sentences)):
#     print("=" * 50)
#     print(sentences[i])
#     print("벡터 길이 :", len(vectors[i]))
#     print("앞의 5개 값 :", vectors[i][:5])

# | Vector Store  | 메모리 저장 | 디스크 저장 | 서버 필요 | 실무 사용 |
# | ------------- | ------ | ------ | ----- | ----- |
# | FAISS         | ✅      | ✅      | ❌     | ⭐⭐⭐⭐⭐ |
# | Chroma        | ✅      | ✅      | ❌     | ⭐⭐⭐⭐⭐ |
# | Milvus        | ✅      | ✅      | ✅     | ⭐⭐⭐⭐⭐ |
# | Qdrant        | ✅      | ✅      | ✅     | ⭐⭐⭐⭐⭐ |
# | Pinecone      | 클라우드   | 클라우드   | 관리형   | ⭐⭐⭐⭐⭐ |
# | Weaviate      | ✅      | ✅      | ✅     | ⭐⭐⭐⭐  |
# | Redis         | ✅      | 일부     | ✅     | ⭐⭐⭐⭐  |
# | Elasticsearch | ✅      | ✅      | ✅     | ⭐⭐⭐⭐  |

# =========================================================================
# Chroma 생성
# pip install chromadb langchain-chroma langchain-huggingface
from langchain_chroma import Chroma
import os
# FAISS와 가장 큰 차이점은 이렇게 디스크에 자동으로 저장되어 프로그램을 종료해도 데이터가 유지된다는 점
#FAISS: "벡터를 빠르게 검색하는 라이브러리"에 가깝습니다.
#Chroma: "벡터 데이터베이스(Vector Database)"로, 벡터뿐 아니라 원본 문서와 메타데이터를 함께 저장하고 영구 저장(Persistence), 필터링, 관리 기능까지 제공하여 RAG 프로젝트에서 많이 사용됩니다.

persist_directory = "./chroma_db"

# DB가 이미 존재하는지 확인
if os.path.exists(persist_directory):
    print("기존 Chroma DB 불러오기")

    db = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding
    )

else:
    print("새로운 Chroma DB 생성")

    db = Chroma.from_texts(
        texts=sentences,
        embedding=embedding,
        persist_directory=persist_directory
    )


# db = Chroma.from_texts(
#     texts=sentences,
#     embedding=embedding,
#     persist_directory="./chroma_db" # DB 에 저장 없어도 되고 있어도 됨
# )


print(db)

docs = db.similarity_search_with_score("고양이")

for doc, score in docs:
    print("=" * 50)
    print(doc.page_content)
    print(score)