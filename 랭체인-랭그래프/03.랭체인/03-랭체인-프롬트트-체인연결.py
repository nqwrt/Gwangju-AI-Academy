
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini"
)

prompt = PromptTemplate.from_template(
"""
당신은 강사입니다.

주제:
{topic}

한줄로 요약
"""
)

# msg = prompt.invoke({
# "topic":"AI Agent"
# })

# print(msg)

chain = prompt | llm

result = chain.invoke({
    "topic":"AI Agent"
})

print(result)
# print(result.content)
# PromptTemplate
# ↓
# PromptValue
# ↓
# ChatOpenAI
# ↓
# AIMessage
