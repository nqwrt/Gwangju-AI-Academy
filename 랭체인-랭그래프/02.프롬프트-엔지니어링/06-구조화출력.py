
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI

load_dotenv()

# 왜 이걸 알아야 하냐.
# 언어 모델은 주어진 예제들을 참고하여 더 정확하고 일관된 응답을 생성
# 이래야만 돈 한마디로 토큰을 아낄수 있음

client = OpenAI()

# 1. 📦 JSON 출력 강제하기 (가장 중요)
# ❌ 일반 출력
# 👉 결과가 자유 텍스트로 나옴 (파싱 불가능)
prompt = """
사용자 정보를 만들어줘.

이름: 김철수
나이: 25
직업: 개발자
"""



# JSON 구조화 출력
prompt = """
다음 정보를 JSON 형식으로 출력하세요.

조건:
- 반드시 JSON만 출력
- 설명 금지
- key는 영어로 작성

정보:
이름: 김철수
나이: 25
직업: 개발자
"""
# 실무형 JSON (강력 추천)
prompt = """
당신은 데이터 포맷터입니다.

다음 정보를 JSON으로 변환하세요.

[CONSTRAINT]
- 반드시 JSON만 출력
- 코드블록 사용 금지
- 추가 설명 금지
- null 금지

[DATA]
이름: 김철수
나이: 25
직업: 개발자
경력: 3년
"""

#2. 📊 Table 출력 (보고서용)
prompt = """
다음 데이터를 표 형식으로 정리하세요.

[DATA]
Python, 중급, 3년
Java, 초급, 1년
C++, 고급, 5년

[OUTPUT]
Markdown table 형식으로 출력
"""

# 3. 🧩 Schema 기반 출력 (실무 핵심)
prompt = """
다음 Schema에 맞게 출력하세요.

[SCHEMA]
{
  "name": "",
  "age": 0,
  "skills": []
}

[DATA]
이름: 김철수
나이: 25
기술: Python, Django, AI
"""

# 4. 🔥 API용 Strict Output (실전 필수)
prompt = """
당신은 API 응답 생성기입니다.

[RULES]
- JSON만 출력
- 설명 금지
- key는 snake_case 사용
- 배열은 반드시 list로 출력

[OUTPUT FORMAT]
{
  "user_name": "",
  "user_age": 0,
  "user_skills": []
}

[INPUT]
이름: 김철수
나이: 25
기술: Python, AI, ML
"""
# 5. 🧠 Multi-format Output (실무형)
prompt = """
다음 데이터를 3가지 형태로 출력하세요.

[DATA]
이름: 김철수
직업: 개발자
경력: 3년

[OUTPUT]
1. JSON
2. Markdown Table
3. 한 줄 요약
"""

# 6. ⚙️ Output Formatting 핵심 원칙
# ✔ 1. 구조를 강제해야 한다
# JSON
# Table
# Schema

# ✔ 2. 금지 조건이 중요하다
# "설명 금지"
# "JSON만 출력"
# "추가 텍스트 금지"

# ✔ 3. Role + Format 같이 써야 안정됨
# 당신은 데이터 포맷터입니다.
# JSON만 출력하세요.

res = client.responses.create(
    model="gpt-4o-mini",
    input=prompt
)

print(res.output_text)