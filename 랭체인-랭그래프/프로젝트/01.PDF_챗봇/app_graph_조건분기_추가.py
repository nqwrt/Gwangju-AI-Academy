
from graph_조건분기_추가 import graph

while True:
    question = input("질문 : ")

    if question == "exit":
        break

    result = graph.invoke(
        {
            "question":question
        }
    )
    
    #print("나와라",result)
    
    print()
    print(result["answer"])
    print("-"*50)

#  사용자 질문
#       │
#       ▼
#  START
#       │
#       ▼
# Retrieve Node
#       │
#       ▼
# Generate Node
#       │
#       ▼
#  END
#       │
#       ▼
# 최종 답변