
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI

load_dotenv()


# 왜 이걸 알아야 하냐.
# 언어 모델은 주어진 예제들을 참고하여 더 정확하고 일관된 응답을 생성
# 이래야만 돈 한마디로 토큰을 아낄수 있음

client = OpenAI()

# 제로샷
# 예시 없음
# ↓
# 모델이 바로 답변
prompt = """
사과를 설명해줘.
"""

# Few-shot
# 예제 제공
# ↓
# 패턴 학습
# ↓
# 새 입력 예측
prompt = """
Q: 고양이
A: 동물

Q: 자동차
A: 탈것

Q: 사과
A:
"""

# Chain-of-Thought (CoT)
# 개념

# 중간 추론 과정을 거치기
prompt = """
단계별로 계산해.

12 × 13
"""

# 여러가지 기능(객체)이 들어가 있음
# client
# ├── responses
# ├── files
# ├── models
# ├── images
# └── embeddings

res = client.responses.create(
    model="gpt-4o-mini",
    input=prompt
)

print(res.output_text)