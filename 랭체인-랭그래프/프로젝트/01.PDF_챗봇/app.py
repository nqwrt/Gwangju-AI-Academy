from rag import ask

while True:

    question = input("질문 : ")

    if question == "exit":
        break

    answer = ask(question)

    print()
    print(answer)
    print("-"*50)


#   사용자 질문
#       │
#       ▼
# Retriever
#       │
#       ▼
# ChromaDB
#       │
#       ▼
# 관련 Chunk 3개
#       │
#       ▼
# Prompt 생성
#       │
#       ▼
# ChatOpenAI
#       │
#       ▼
# 최종 답변