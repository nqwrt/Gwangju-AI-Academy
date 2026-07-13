from dotenv import load_dotenv

load_dotenv()

from graph import graph

# 대화 기록

#messages = []

print("=" * 50)
print("LangGraph Tool Calling Agent")
print("종료 : exit")
print("=" * 50)

while True:

    question = input("\n질문 : ")

    if question.lower() == "exit":
        break

    # 사용자 질문 추가
    # messages.append(
    #     (
    #         "user",
    #         question
    #     )
    # )

    # Agent 실행
    result = graph.invoke(
        {
            #"messages": messages
            "messages": question
        }
    )

    # 마지막 AI 답변
    answer = result["messages"][-1].content

    print(f"\nAI : {answer}")

    # 대화 기록 갱신
    #messages = result["messages"]