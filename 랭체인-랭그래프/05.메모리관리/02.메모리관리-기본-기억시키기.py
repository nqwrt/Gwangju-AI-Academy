# LangGraph 기반 메모리 권장

# LangChain 1.0에서는 복잡한 상태 관리가 필요한 경우 LangGraph 기반 메모리(InMemorySaver, SqliteSaver 등)를 권장합니다. RunnableWithMessageHistory는 간단한 챗봇에서 계속 사용할 수 있으며 지원이 유지

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import (
    HumanMessage,
    AIMessage
)
from langchain_core.prompts import (
    MessagesPlaceholder
)
import os

load_dotenv()

LLM_MODEL = os.getenv("LLM_AI_MODEL")

# OpenAI 모델 초기화 (OPENAI_API_KEY 환경변수 필요)
llm = init_chat_model(
    LLM_MODEL,
    temperature=0.1,
    max_tokens=1000
    )

history = [] # 대화 기록 저장소 생성

# 이런식으로 채워짐

# [
#  HumanMessage("안녕"),
#  AIMessage("안녕하세요")
# ]

# 프롬프트 객체 생성

prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 친절한 비서입니다."), #LLM 규칙 지정.
    # ("placeholder","{history}"), ## history 자리에 이전 대화를 넣어라 => 가장 중요한 부분
    MessagesPlaceholder("history")

])

while True:

    q = input("질문: ")

    history.append(
        HumanMessage(q)
    )

    # {
    #   "history":[
    #   HumanMessage(
    #       "내 이름은 철수야"
    #       )
    #   ]
    # }

    chain = prompt | llm

    res = chain.invoke({
        "history": history
    })

    history.append(
        AIMessage(
            res.content
        )
    )
    # [
    # HumanMessage(
    # "내 이름은 철수야"
    # ),

    # AIMessage(
    # "알겠습니다."
    # )
    # ]

    print(
        "\nAI:",
        res.content
    )



