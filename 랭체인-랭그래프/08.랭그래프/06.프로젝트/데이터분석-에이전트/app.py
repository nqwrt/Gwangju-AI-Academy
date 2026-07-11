from graph import graph

while True:

    question = input("\n질문(exit 종료): ")

    if question.lower() == "exit":
        break

    result = graph.invoke(
        {
            "question": question,
            "analysis_type": "",
            "code": "",
            "result": "",
            "dataframe": None,
            "error": ""
        }
    )
    print("\n============================")
    print(result["result"])