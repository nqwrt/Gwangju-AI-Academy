from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import os

load_dotenv()

LLM_MODEL = os.getenv("LLM_AI_MODEL")

# OpenAI 모델 초기화 (OPENAI_API_KEY 환경변수 필요)
llm = init_chat_model(
    LLM_MODEL,
    temperature=0.1,
    max_tokens=1000
    )

# @tool 일반 파이썬 함수를 LLM이 호출 가능한 함수로 변환하는 데코레이터

# tool 이란, LLM이 "행동"할 수 있게 해주는 함수

# LLM
#  ↓
# Tool 선택 (multiply)
#  ↓
# 실행
#  ↓
# 결과 반환

from langchain.tools import tool
from datetime import datetime

# doc string이 중요함
# 왜 docstring 중요할까?
# LLM은 이 설명을 읽고: 계산할때 쓰는 함수인걸 알게 됨

@tool
def add(a,b):
    """
    두 수를 더한다
    """
    return a + b

print(add.invoke({"a":10,"b":20}))


# #LLM 은 현재 시각을 학습 하지 않았기 때문에, 시간을 알려줄수 없음
@tool
def get_time(city: str) -> str:
    """도시 이름을 받아 현재 시간을 알려준다"""
    now = datetime.now()
    return f"{city} 현재 시간: {now.strftime('%Y-%m-%d %H:%M:%S')}"

print(get_time)
print(type(get_time))

print(get_time.invoke({"city": "Seoul"}))


tools = [
    get_time,add
]

# ======================
# Tool 연결
# ======================

llm_with_tools = llm.bind_tools(
    tools
)

# ======================
# 실행
# ======================

while True:

    q = input("\n질문: ")
    res = llm_with_tools.invoke(q)

    print("\n응답:")
    #print(res.content)
    print(res)

    if res.tool_calls:
        for call in res.tool_calls:
            
            print("name",call["name"])

            if call["name"] == "get_time":                
                print("여길타나",call["args"])
                result = get_time.invoke(
                    call["args"]
                )

            if call["name"] == "add":
                result = add.invoke(
                    call["args"]
                )

            print("\nTool 결과:")
            print(result)
    else:
        print(res.content)