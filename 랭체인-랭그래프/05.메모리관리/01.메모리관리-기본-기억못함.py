# LangGraph 기반 메모리 권장

# LangChain 1.0에서는 복잡한 상태 관리가 필요한 경우 LangGraph 기반 메모리(InMemorySaver, SqliteSaver 등)를 권장합니다. RunnableWithMessageHistory는 간단한 챗봇에서 계속 사용할 수 있으며 지원이 유지

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()

LLM_MODEL = os.getenv("LLM_AI_MODEL")

# OpenAI 모델 초기화 (OPENAI_API_KEY 환경변수 필요)
llm = init_chat_model(
    LLM_MODEL,
    temperature=0.1,
    max_tokens=1000
    )
# 첫 번째 질문
response1 = llm.invoke("안녕하세요, 제 이름은 민수입니다.")
print("응답 1:", response1.content)

# 두 번째 질문
response2 = llm.invoke("제 이름이 뭐였죠?")
print("응답 2:", response2.content)

# 메모리의 역할
# 메모리 시스템은 다음과 같은 기능을 제공합니다:

# 대화 기록 저장: 이전 메시지들을 저장하고 관리
# 컨텍스트 유지: 대화의 흐름과 맥락 보존
# 개인화: 사용자별 대화 세션 관리
# 효율성: 토큰 사용량 최적화를 위한 메모리 관리