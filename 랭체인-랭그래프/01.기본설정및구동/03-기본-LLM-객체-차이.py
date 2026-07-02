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
import os
import sys
from langchain_openai import ChatOpenAI

import sys
from pathlib import Path

# 현재 파일 기준으로 3단계 위 폴더를 import 경로에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))
print(os.listdir(Path(__file__).resolve().parent.parent))

from llm_loader import init_custom_llm

print(init_custom_llm)

# 실제로는 OpenAI()를 호출
# llm = ChatOpenAI(
#     model="gpt-5-nano",
# )

llm = init_custom_llm()


try:
    result = llm.invoke("AI Agent란?")
    
    print(result)
    print(result.content)

except Exception as e:
    import traceback
    traceback.print_exc()

# result = llm.invoke(
#     "AI Agent란?"
# )

# print(result.content)


from pprint import pprint



print(type(result))
print()

print("=== content ===")
print(result.content)

print("\n=== response_metadata ===")
pprint(result.response_metadata)

print("\n=== usage_metadata ===")
pprint(result.usage_metadata)

print("\n=== model_dump ===")
pprint(result.model_dump())
