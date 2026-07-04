
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI
import sys
from pathlib import Path

# 현재 파일 기준으로 3단계 위 폴더를 import 경로에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))
from llm_loader import init_custom_llm


# 왜 이걸 알아야 하냐.
# 언어 모델은 주어진 예제들을 참고하여 더 정확하고 일관된 응답을 생성
# 이래야만 돈 한마디로 토큰을 아낄수 있음


# 2. 🧩 Prompt 변수화 (Template 구조)
topic = "딥러닝"

# 💡 문제점
# 코드와 Prompt가 섞임
# 재사용 어려움
prompt = f"""
당신은 AI 강사입니다.

다음 주제를 설명하세요:
{topic}

조건:
- 초보자 대상
- 예제 포함
- 5줄 이내
"""

from langchain_core.prompts import PromptTemplate
#3. 🧠 LangChain PromptTemplate
# 👉 Prompt를 “객체화”해서 관리

prompt = PromptTemplate.from_template("""
당신은 데이터 분석 전문가입니다.

주제: {topic}

다음 조건으로 설명하세요:
- 초보자도 이해 가능
- 핵심만 설명
- 예제 포함
""")

result = prompt.invoke({"topic": "머신러닝"})
# formatted_prompt = prompt.format(topic="반복문")
print(result)


messages = ChatPromptTemplate.from_messages([
    ("system", "당신은 Python 강사입니다."),
    ("human", "{topic}을 설명하세요.")
])

print(messages)
result = messages.invoke({"topic": "머신러닝"})

llm = init_custom_llm()
response = llm.invoke(result)
print(response.content)

##################################### 메세지 홀더 ###############################

# PromptTemplate → 문자열 변수를 넣는다.
# ChatPromptTemplate → 역할(System/Human/AI)을 가진 메시지를 만든다.
# MessagesPlaceholder → 이전 대화 메시지 리스트를 해당 위치에 그대로 삽입한다.

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import *

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 AI입니다."),
    MessagesPlaceholder("history"),
    ("human", "{question}")
])

messages = prompt.invoke({
    "history":[
        HumanMessage(content="안녕"),
        AIMessage(content="안녕하세요.")
    ],
    "question":"내 이름 기억해?"
})

print(messages)