
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

prompt = PromptTemplate.from_template(
"""
당신은 강사입니다.

주제:
{topic}

쉬운 예제 포함
"""
)

msg = prompt.invoke({
"topic":"AI Agent"
})

print(msg)


# ==========================
prompt = PromptTemplate.from_template(
"""
당신은 {job} 입니다.

주제:
{topic}

설명 수준:
{level}
"""
)

msg = prompt.invoke({
    "job":"파이썬 강사",
    "topic":"리스트",
    "level":"초급"
})

print(msg)

# ==========================================================
# 블로그 작성 프롬프트

prompt = PromptTemplate.from_template(
"""
블로그 작성

제목:
{title}

톤:
{tone}

분량:
{length}
"""
)

msg = prompt.invoke({
    "title":"AI Agent",
    "tone":"친절",
    "length":"300자"
})

print(msg)
# =============================================================================
# SQL 생성기

prompt = PromptTemplate.from_template(
"""
테이블:
{table}

조건:
{condition}

SQL 작성
"""
)

msg = prompt.invoke({
    "table":"users",
    "condition":"나이 20 이상"
})

print(msg)
# ===========================================================

# 번역기 프롬프트

prompt = PromptTemplate.from_template(
"""
다음 문장을
{language} 로 번역

문장:
{text}
"""
)

msg = prompt.invoke({
    "language":"영어",
    "text":"안녕하세요"
})

print(msg)

# ========================================================
# Chain-of-Thought 스타일

prompt = PromptTemplate.from_template(
"""
Q: 고양이
A: 동물

Q: 자동차
A: 탈것

Q: {question}
A:
"""
)

msg = prompt.invoke({
    "question":"사과"
})

print(msg)
# ================================================================
prompt = PromptTemplate.from_template(
"""
문제를 단계별로 설명.

문제:
{question}
"""
)

msg = prompt.invoke({
    "question":"25 × 12"
})

print(msg)

# ================================================================
# JSON 출력 강제

prompt = PromptTemplate.from_template(
"""
문제를 단계별로 설명.

문제:
{question}
"""
)

msg = prompt.invoke({
    "question":"25 × 12"
})

print(msg)
# ===============================================