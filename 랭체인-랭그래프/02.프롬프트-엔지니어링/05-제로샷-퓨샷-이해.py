
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
# ❌ Zero-shot (예시 없음)
#👉 AI가 기준 없이 바로 답변 생성

prompt = """
다음 문장을 영어로 번역하세요.

나는 오늘 학교에 갔다.
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
# ❌ 일반 질문
prompt = """
다음 문제를 풀어라:

철수는 사과 5개를 가지고 있다.
3개를 먹었다. 몇 개 남았는가?
"""

#Chain of Thought 적용
prompt = """
다음 문제를 단계별로 생각해서 풀어라.

문제:
철수는 사과 5개를 가지고 있다.
3개를 먹었다. 몇 개 남았는가?

풀이 과정:
1. 전체 개수 확인
2. 소비한 개수 확인
3. 계산 과정 설명
4. 최종 답변
"""

# 5. 🔁 Few-shot + CoT 혼합 (실전)
# 👉 실무에서 가장 많이 쓰는 형태
prompt = """
[EXAMPLES]

예시 1:
문제: 2 + 2
풀이: 2 + 2 = 4
답: 4

예시 2:
문제: 5 + 3
풀이: 5 + 3 = 8
답: 8

[TASK]
문제: 7 + 6

[INSTRUCTION]
1. 단계별로 계산
2. 마지막에 답 출력
"""

#🚀 한 줄 정리
#"AI는 답을 주는 존재가 아니라, 생각 과정을 설계해야 제대로 작동한다

res = client.responses.create(
    model="gpt-4o-mini",
    input=prompt
)

print(res.output_text)