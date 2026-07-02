
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from llm_loader import init_custom_llm

llm = init_custom_llm()

res = llm.invoke(
    "파이썬 설명"
)

# print(res.content)


topics=[
"Python",
"Django",
"React"
]

for t in topics:
    print(
        llm.invoke(
            f"{t} 3줄로 설명해줘"
        ).content
    )

# 좀더 구조화 
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("""
당신은 Python 강사입니다.
주제: {topic}
초보자도 이해할 수 있게 설명하세요.
""")

# Prompt 1개 → 여러 문제 처리

formatted = prompt.format(topic="반복문")

response = llm.invoke(formatted)
print(response.content)

topics = ["반복문", "조건문", "함수"]

for topic in topics:
    formatted = prompt.format(topic=topic)
    response = llm.invoke(formatted)
    print("====")
    print(response.content)