from rag import ask

print("=" * 50)
print("프로젝트 소개 챗봇")
print("=" * 50)

while True:

    question = input("\n질문 : ")

    if question == "exit":
        break

    answer = ask(question)

    print()
    print(answer)