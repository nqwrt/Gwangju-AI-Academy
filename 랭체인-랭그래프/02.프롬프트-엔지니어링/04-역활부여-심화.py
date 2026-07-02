
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI

load_dotenv()

from openai import OpenAI

client = OpenAI()

# 🧠 기본 Role Prompt (역할 부여)
prompt = """
당신은 20년 경력의 Python 교육 전문가입니다.

당신의 역할:
- 초보자도 이해할 수 있게 설명
- 반드시 예제를 포함
- 어려운 개념은 비유로 설명

질문:
파이썬의 반복문을 설명해주세요.
"""

#2.👨‍🏫 Persona Prompt (인물 설정)
# 👉 “AI의 성격 + 경력 + 말투”를 지정
prompt = """
당신은 다음 특징을 가진 AI입니다.

[Persona]
- 10년차 데이터 사이언티스트
- 삼성전자 AI 연구원 출신
- 친절하고 쉽게 설명하는 스타일

[Task]
머신러닝이 무엇인지 설명하세요.

[Constraint]
- 5줄 이내
- 비유 1개 포함
- 초보자 대상
"""

# 🧩 3. Prompt 4요소 설계법 (실전 템플릿)

prompt = """
다음 질문에 대해 서로 다른 Role로 답변하세요.

질문: AI란 무엇인가?

Role 1: AI 연구원
Role 2: 초등학교 선생님
Role 3: 비유를 많이 쓰는 유튜버

각 Role별로 답변을 구분해서 작성하세요.
"""

# 🧩 5. Role + Tone 조합 실전
# 👉 실무에서 가장 많이 쓰는 형태
prompt = """
당신은 친절한 스타트업 CTO입니다.

스타트업에서 AI를 도입해야 하는 이유를 설명하세요.

조건:
- 말투: 친근하고 현실적
- 예시 포함
- 투자자 설득용 느낌
"""

response = client.responses.create(
    model="gpt-4o-mini",
    input=prompt
)

print(response.output_text)