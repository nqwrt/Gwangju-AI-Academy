from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3"
)

texts = [
    "고양이는 생선을 좋아합니다.",
    "강아지는 사람을 잘 따릅니다.",
    "자동차는 바퀴가 네 개입니다.",
    "호랑이는 고양이과 동물입니다.",
    "사자는 초원의 왕입니다."
]

db = Chroma.from_texts(
    texts=texts,
    embedding=embedding
)

print("저장 완료!")

# Retriever 생성
retriever = db.as_retriever()

#검색하기
question = "고양이는 어떤 동물인가요?"
docs = retriever.invoke(question)
for doc in docs:
    print("=" * 50)
    print(doc.page_content)