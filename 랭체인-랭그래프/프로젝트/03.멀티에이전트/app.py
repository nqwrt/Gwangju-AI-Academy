from graph import graph

while True:

    question = input("질문 : ")

    if question == "exit":
        break

    result = graph.invoke(
        {
            "question": question
        }
    )

    print()
    print("AI :", result["answer"])
    print()