
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI

load_dotenv()

# 왜 이걸 알아야 하냐.
# 언어 모델은 주어진 예제들을 참고하여 더 정확하고 일관된 응답을 생성
# 이래야만 돈 한마디로 토큰을 아낄수 있음

client = OpenAI()

# 2. 🧩 Prompt 변수화 (Template 구조)
topic = "딥러닝"

# 💡 문제점
# 코드와 Prompt가 섞임
# 재사용 어려움
prompt = f"""
당신은 AI 강사입니다.

다음 주제를 설명하세요:
{topic}

조건:
- 초보자 대상
- 예제 포함
- 5줄 이내
"""

from langchain_core.prompts import PromptTemplate
#3. 🧠 LangChain PromptTemplate
# 👉 Prompt를 “객체화”해서 관리

prompt = PromptTemplate.from_template("""
당신은 데이터 분석 전문가입니다.

주제: {topic}

다음 조건으로 설명하세요:
- 초보자도 이해 가능
- 핵심만 설명
- 예제 포함
""")

result = prompt.invoke({"topic": "머신러닝"})
print(result)

from llm_loader import init_custom_llm

llm = init_custom_llm()

formatted_prompt = prompt.format(topic="반복문")


response = llm.invoke(formatted_prompt)
print(response.content)

# res = client.responses.create(
#     model="gpt-4o-mini",
#     input=prompt
# )

# print(res.output_text)