
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI

load_dotenv()

from openai import OpenAI

client = OpenAI()

prompt = """
예시

질문:
집값 예측 절차

답변:

1. 데이터 수집
2. 결측치 처리
3. 전처리
4. 모델 학습
5. 평가


질문:
Titanic 생존 예측 절차

답변:
"""

prompts = {

"zero":
"""
Titanic 생존 예측 절차 설명
""",

"few":
"""
질문:
집값 예측 절차

답:
1 수집
2 전처리
3 학습

질문:
Titanic 생존 예측 절차

답:
""",

"cot":
"""
단계별로 생각해서 설명해.

Titanic 생존 예측 절차
"""
}

response = client.responses.create(
    model="gpt-4o-mini",
    input=prompt
)

print(response.output_text)