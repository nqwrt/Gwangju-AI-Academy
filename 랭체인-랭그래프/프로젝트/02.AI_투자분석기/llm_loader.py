# llm_loader.py
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# 모듈이 로드될 때 .env를 자동으로 읽도록 설정
load_dotenv()

def init_custom_llm(temperature: float = 0.1, max_tokens: int = 1000):
    """지정된 환경변수 모델로 LLM을 초기화합니다."""
    model_name = os.getenv("LLM_AI_MODEL")
    
    if not model_name:
        raise ValueError("환경변수 'LLM_AI_MODEL'이 설정되지 않았습니다.")
        
    return init_chat_model(
        model_name,
        temperature=temperature,
        max_tokens=max_tokens
    )