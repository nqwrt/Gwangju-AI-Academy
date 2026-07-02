
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

import sys
from pathlib import Path
from pydantic import BaseModel

sys.path.append(str(Path(__file__).resolve().parent.parent))
from llm_loader import init_custom_llm

llm = init_custom_llm()

class UserInfo(BaseModel):
    name: str
    age: int
    job: str

structured_llm = llm.with_structured_output(UserInfo)

result = structured_llm.invoke("김철수는 25살 개발자야")
print(result)

#========================================================

# User Input
#    ↓
# LLM
#    ↓
# Structured Output Parser
#    ↓
# JSON / Object
#    ↓
# API / DB 저장

class Product(BaseModel):
    name: str
    price: int
    category: str

structured_llm = llm.with_structured_output(Product)

result = structured_llm.invoke("아이폰 15는 120만원 스마트폰")
print(result)