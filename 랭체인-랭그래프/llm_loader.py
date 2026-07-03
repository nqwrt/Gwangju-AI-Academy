# llm_loader.py
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pathlib import Path
from dotenv import load_dotenv
import langchain
import langchain_openai

# print(langchain.__version__)
# print(langchain_openai.__version__)

env_path = Path(__file__).resolve().parent / ".env"

#print(env_path)
# print("llm_loader 위치:", Path(__file__).resolve())
# print(".env 위치:", Path(__file__).resolve().parent / ".env")

load_dotenv(env_path)

# print("API KEY :", os.getenv("LANGSMITH_API_KEY"))
# print("TRACING :", os.getenv("LANGSMITH_TRACING"))
# print("PROJECT :", os.getenv("LANGCHAIN_PROJECT"))
# print("ENDPOINT:", os.getenv("LANGSMITH_ENDPOINT"))

from langsmith import Client
import os

# client = Client(
#     api_key=os.environ["LANGSMITH_API_KEY"]
# )

# print(client)
# print(list(client.list_projects()))
# print(os.environ["LANGSMITH_API_KEY"][:12])

# 모듈이 로드될 때 .env를 자동으로 읽도록 설정
#load_dotenv()

def init_custom_llm(temperature: float = 0.1, max_tokens: int = 1000):
    """지정된 환경변수 모델로 LLM을 초기화합니다."""
    model_name = os.getenv("LLM_AI_MODEL")
    
    print("모델이름",model_name)
    #print("OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))

    if not model_name:
        raise ValueError("환경변수 'LLM_AI_MODEL'이 설정되지 않았습니다.")
        
    return init_chat_model(
        model_name,
        temperature=temperature,
        max_tokens=max_tokens
    )