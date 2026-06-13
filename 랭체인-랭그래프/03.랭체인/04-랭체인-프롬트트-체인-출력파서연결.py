
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import (
XMLOutputParser
)   

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

prompt = ChatPromptTemplate.from_template(
"""
JSON 출력

{{
"title":"",
"content":""
}}

질문:
{topic}
"""
)

# msg = prompt.invoke({
# "topic":"AI Agent"
# })

# print(msg)

output_parser = StrOutputParser()

# 주의 일반 자연어는 기본적으로 처리 에러 남
#output_parser = JsonOutputParser() #JSON으로 강제.
#output_parser = XMLOutputParser()


chain = prompt | llm | output_parser



result = chain.invoke({
    "topic":"AI Agent"
})

print(result)
# print(result.content)

