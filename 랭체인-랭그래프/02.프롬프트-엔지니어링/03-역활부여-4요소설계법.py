
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI

load_dotenv()

from openai import OpenAI

client = OpenAI()

# 🧠 1. Role Prompt (역할 부여)
prompt = """
당신은 20년 경력의 Python 교육 전문가입니다.

당신의 역할:
- 초보자도 이해할 수 있게 설명
- 반드시 예제를 포함
- 어려운 개념은 비유로 설명

질문:
파이썬의 반복문을 설명해주세요.
"""

#2. Task / Constraint / Output 구조
prompt = """
[ROLE]
당신은 데이터 분석 전문가입니다.

[TASK]
타이타닉 데이터를 분석해서 생존률을 설명하세요.

[CONSTRAINT]
- 10줄 이내
- 전문용어 최소화
- 숫자 기반 설명 포함
- 초보자 대상

[OUTPUT]
- Markdown 표 형식
- 마지막에 한 줄 요약 포함
"""

# 🧩 3. Prompt 4요소 설계법 (실전 템플릿)

prompt = """
# 1. ROLE (역할)
당신은 AI 데이터 분석가입니다.

# 2. TASK (할 일)
아래 데이터를 분석하고 인사이트를 도출하세요.

데이터: 삼성전자 주가 데이터

# 3. CONSTRAINT (제약 조건)
- 5가지 핵심 인사이트만 도출
- 불필요한 설명 금지
- 수치 기반 분석 포함
- 초보자도 이해 가능하게 설명

# 4. OUTPUT (출력 형식)
다음 형식으로 출력하세요:

1. 인사이트 제목
2. 설명
3. 근거 데이터
4. 한 줄 요약
"""

response = client.responses.create(
    model="gpt-4o-mini",
    input=prompt
)

print(response.output_text)