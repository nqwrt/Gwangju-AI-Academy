# | 항목        | PromptTemplate    | ChatPromptTemplate |
# | --------- | -----------------   | ------------------ |
# | 출력        | 문자열              | 메시지                |
# | 타입        | StringPromptValue | ChatPromptValue    |
# | role 지원   | ❌                 | ⭕                  |
# | system     | ❌                 | ⭕                  |
# | human      | ❌                 | ⭕                  |
# | assistant  | ❌                 | ⭕                  |
# | Agent 적합  | △                 | ⭕                  |
# | 추천 사용     | 단순 생성             | 대부분                |

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

from langchain_core.prompts import (
ChatPromptTemplate
)

# system = AI의 행동 규칙(설정)
# human =  사용자 질문

# 1. system

# 역할:
# AI가 어떻게 행동해야 하는지 정의
# 행동 규칙
# 출력 형식
# 말투
# 제약조건
# 역할

# 2. human

# 역할:
# 실제 사용자 입력
# human 여러 개 가능

prompt = ChatPromptTemplate.from_messages(
[
(
"system",
"너는 파이썬 강사"
),
(
"human",
"{question}"
)
]
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
        "system",
        "너는 수학 강사"
        ),
        (
        "human",
        "2+3"
        ),
        (
        "human",
        "설명도 해줘"
        )
    ]
)


llm = ChatOpenAI(
    model="gpt-4o-mini"
)

chain = prompt | llm 

result = chain.invoke({
    "input":"AI Agent"
})

print(result.content)

