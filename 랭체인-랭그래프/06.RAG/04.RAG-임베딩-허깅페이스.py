# pip install langchain-huggingface
# pip install sentence-transformers

# ✅ API 비용이 없음
# ✅ 인터넷이 없어도(모델 다운로드 후) 사용할 수 있습니다.
# ✅ 학생들이 직접 실행해 볼 수 있습니다.
# ✅ RAG 실습에 가장 많이 사용됩니다.

# 문장 전체를 하나의 의미 단위로 보고 하나의 벡터를 생성
# RAG에서는 "문서를 Chunk로 나누고, Chunk 하나를 벡터 하나로 변환하여 Vector DB에 저장한다.

from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3"
)

text = "대한민국의 수도는 서울입니다."

vector = embedding.embed_query(text)

print("벡터 길이 :", len(vector))
print(vector[:10])

#============================================
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3"
)

documents = [
    "고양이는 귀여운 동물입니다.",
    "강아지는 충성심이 강합니다.",
    "자동차는 빠르게 달립니다."
]

vectors = embedding.embed_documents(documents)

print("문서 개수 :", len(vectors))
print("첫 번째 벡터 길이 :", len(vectors[0]))



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

for i in range(len(sentences)):
    print("=" * 50)
    print(sentences[i])
    print("벡터 길이 :", len(vectors[i]))
    print("앞의 5개 값 :", vectors[i][:5])