from rag import ask

print("=" * 50)
print("회사 규정 AI")
print("=" * 50)

while True:

    question = input("\n질문 : ")

    if question == "exit":
        break

    answer = ask(question)

    print()
    print(answer)