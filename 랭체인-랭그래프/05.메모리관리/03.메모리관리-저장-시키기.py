#==================================================
# 예제 1. 리스트로 대화 저장하기 (Memory가 없을 때)
history = []

history.append("사용자 : 안녕하세요.")
history.append("AI : 안녕하세요!")

history.append("사용자 : 제 이름은 철수입니다.")
history.append("AI : 반갑습니다 철수님.")

print(history)

# 문자열만 저장하면 AI가 이해할 수 있을까요?"
# AI는 누가 말했는지(Human/AI)를 알아야 함

from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage

history = []

history.append(HumanMessage("안녕하세요."))
history.append(AIMessage("안녕하세요!"))

history.append(HumanMessage("제 이름은 철수입니다."))
history.append(AIMessage("반갑습니다 철수님."))

print(history)

# 이제 AI가
# 사람이 말한 것
# AI가 말한 것
# 을 구분

#=========================================================

import sys
from pathlib import Path
from pydantic import BaseModel

sys.path.append(str(Path(__file__).resolve().parent.parent))
from llm_loader import init_custom_llm

llm = init_custom_llm()

# 예제 3. ChatMessageHistory 등장
# 위의 코드를 좀더 쉽게 만듬
from langchain_community.chat_message_histories import ChatMessageHistory

history = ChatMessageHistory()

history.add_user_message("안녕하세요.")
history.add_ai_message("안녕하세요!")

history.add_user_message("제 이름은 철수입니다.")
history.add_ai_message("반갑습니다 철수님.")

print(history.messages)

# 예제 4. 하나씩 확인하기


history = ChatMessageHistory()

history.add_user_message("안녕하세요.")
history.add_ai_message("안녕하세요!")

for message in history.messages:
    print(type(message))
    print(message.content)
    print("-" * 30)

# 예제 6. 특정 대화만 꺼내기


history = ChatMessageHistory()

history.add_user_message("안녕하세요.")
history.add_ai_message("안녕하세요!")

history.add_user_message("제 이름은 철수입니다.")
history.add_ai_message("반갑습니다 철수님.")

print(history.messages[0].content)
print(history.messages[1].content)
print(history.messages[2].content)
print(history.messages[3].content)

# 예제 7. 메모리 비우기

history = ChatMessageHistory()

history.add_user_message("안녕하세요.")
history.add_ai_message("안녕하세요!")

print("초기 상태")
print(history.messages)

history.clear()

print("\n삭제 후")
print(history.messages)

#
# 예제 8. LLM과 연결하기 (가장 중요한 예제)
from langchain_core.chat_history import InMemoryChatMessageHistory

history = InMemoryChatMessageHistory()

# 첫 번째 질문
question = "내 이름은 철수야."

history.add_user_message(question)

response = llm.invoke(history.messages)
history.add_ai_message(response.content)
print(response.content)

# 두 번째 질문
question = "내 이름이 뭐야?"
history.add_user_message(question)
response = llm.invoke(history.messages)
history.add_ai_message(response.content)
print(response.content)

# ChatMessageHistory는 대화(Message)들을 저장하는 컨테이너이다.
# history.messages는 LLM에 그대로 전달할 수 있는 메시지 리스트이다.