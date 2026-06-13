
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
)

# res = llm.invoke(
#     "파이썬 설명"
# )

# print(res.content)


topics=[
"Python",
"Django",
"React"
]

for t in topics:
    print(
        llm.invoke(
            f"{t} 3줄로 설명해줘"
        ).content
    )

