# 지원 프로바이더 목록
# init_chat_model이 지원하는 주요 프로바이더는 다음과 같습니다.

# 프로바이더	패키지	환경변수	예시
# OpenAI	langchain-openai	OPENAI_API_KEY	gpt-4.1, gpt-4.1-mini
# Anthropic	langchain-anthropic	ANTHROPIC_API_KEY	claude-sonnet-4-5-20250929
# Google	langchain-google-genai	GOOGLE_API_KEY	google_genai:gemini-2.5-flash-lite
# AWS Bedrock	langchain-aws	AWS 자격증명	bedrock_converse:anthropic.claude-3-5-sonnet
# Azure OpenAI	langchain-openai	AZURE_OPENAI_API_KEY	azure_openai:gpt-4

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
model = init_chat_model(
    LLM_MODEL,
    temperature=0.1,
    max_tokens=1000
    )

# 모델 호출
response = model.invoke("안녕하세요, 한국의 수도는 어디인가요?")
print(response.content)

# 다양한 프로바이더 사용하기
# from langchain.chat_models import init_chat_model

# # OpenAI (기본적으로 gpt- 접두사는 OpenAI로 인식)
# openai_model = init_chat_model("gpt-4.1")

# # Anthropic Claude
# claude_model = init_chat_model("claude-sonnet-4-5-20250929")

# # Google Gemini (프로바이더:모델명 형식)
# gemini_model = init_chat_model("google_genai:gemini-2.5-flash-lite")

# # AWS Bedrock (model_provider 파라미터 사용)
# bedrock_model = init_chat_model(
#     "anthropic.claude-3-5-sonnet-20240620-v1:0",
#     model_provider="bedrock_converse"
# )