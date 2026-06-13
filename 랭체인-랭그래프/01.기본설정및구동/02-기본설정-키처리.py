# pip install dotenv

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI

load_dotenv()

# 클라이언트 생성
client = OpenAI()

# 요청
response = client.responses.create(
    model="gpt-4o-mini",
    input="AI Agent란?"
)
# 출력
print(response.output_text)


# 🧠 2️⃣ 토큰 감각 (중요)

# 대략 이렇게 생각하면 됨:

# 한글 1글자 ≈ 1~2 토큰
# 영어 1단어 ≈ 1 토큰
# 1문장 ≈ 10~30 토큰

# 👉 즉
# "2022년 월드컵 우승팀은 어디야?"
# ➡️ 약 15~25 토큰

# 💥 감각으로 보면
# 사용량	비용
# 1번 질문	거의 0원
# 1000번	몇 원
# 10만번	몇 천원

# 🧠 6️⃣ 비용 절약 꿀팁
# ✅ 1. 무조건 mini 사용
# model="gpt-4o-mini"
# ✅ 2. max_tokens 제한
# max_tokens=100
# ✅ 3. temperature 낮게
# temperature=0.1

# 👉 불필요한 길이 감소

#🚀 현실적인 추천 세팅
# response = client.chat.completions.create(
#   model="gpt-4o-mini",
#   temperature=0.2,
#   max_tokens=100,
#   messages=[
#     {"role": "user", "content": "질문"}
#   ]
# )