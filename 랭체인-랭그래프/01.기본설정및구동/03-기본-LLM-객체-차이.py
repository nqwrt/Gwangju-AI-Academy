# pip install dotenv

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI

load_dotenv()

# # 클라이언트 생성
# client = OpenAI()

# # 요청
# response = client.responses.create(
#     model="gpt-4o-mini",
#     input="AI Agent란?"
# )
# # 출력
# print(response.output_text)

# pip install langchain-openai

from langchain_openai import ChatOpenAI

# 실제로는 OpenAI()를 호출
llm = ChatOpenAI(
    model="gpt-4o-mini",
)

result = llm.invoke(
    "AI Agent란?"
)

print(result.content)

