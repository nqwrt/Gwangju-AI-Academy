from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

from llm_loader import init_custom_llm

# 깔끔하게 LLM 초기화 완료!
llm = init_custom_llm()

# 이후에 체인(Chain)을 구성하거나 llm.invoke() 등을 사용하시면 됩니다.
print(f"LLM 모델 로드 완료")

embedding = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding
)

retriever = vector_db.as_retriever(
    search_kwargs={"k":3}
)



PROMPT = """
당신은 PDF 문서를 분석하는 AI입니다.

문서
{context}

질문
{question}

답변
"""

def ask(question):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = PROMPT.format(
        context=context,
        question=question
    )

    response = llm.invoke(prompt)

    return response.content