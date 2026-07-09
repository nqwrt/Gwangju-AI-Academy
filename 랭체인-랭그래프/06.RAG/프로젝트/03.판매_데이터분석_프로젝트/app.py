from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
import re
import pandas as pd
import matplotlib.pyplot as plt

from langchain_chroma import Chroma
import sys

import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Malgun Gothic"   # 맑은 고딕
plt.rcParams["axes.unicode_minus"] = False      # 마이너스(-) 깨짐 방지

# 현재 파일 기준으로 3단계 위 폴더를 import 경로에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from llm_loader import init_custom_llm

llm = init_custom_llm()

BASE_DIR = Path(__file__).resolve().parent
XLSX_PATH = BASE_DIR / "data" / "sales.xlsx"

df = pd.read_excel(XLSX_PATH)

# chroma_db 폴더
DB_PATH = BASE_DIR / "chroma_db"

embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3"
)

db = Chroma(
    persist_directory=str(DB_PATH),
    embedding_function=embedding
)

retriever = db.as_retriever(
    search_kwargs={"k":3}
)

###################################################
# Context 생성
###################################################

def make_context(question):
    docs = retriever.invoke(question)
    context = ""
    for doc in docs:
        context += doc.page_content
        context += "\n"
    return context

def make_code(question):

    context = make_context(question)

    prompt = f"""
    당신은 Pandas 전문가입니다.

    DataFrame 이름은 반드시 df 입니다.

    컬럼 정보

    {context}

    사용자 질문

    {question}

    규칙

    1. DataFrame 이름은 df입니다.
    2. 컬럼은 날짜, 지역, 상품, 수량, 매출만 존재합니다.
    3. 절대로 다른 컬럼명을 사용하지 마세요.
    4. inplace=True를 사용하지 마세요.
    5. set_index()를 사용하지 마세요.
    6. resample()을 사용하지 마세요.
    7. 월별 분석은 groupby()와 dt.to_period("M")을 사용하세요.
    8. 그래프는 matplotlib를 사용하세요.
    9. 마지막에는 반드시 plt.show()를 호출하세요.
    10. 코드만 출력하세요.
    1. DataFrame 이름은 df입니다.
    2. pd와 plt는 이미 import되어 있습니다.
    3. import 문은 작성하지 마세요.
    4. 날짜 컬럼은 반드시 먼저
    df["날짜"] = pd.to_datetime(df["날짜"])
    를 실행하세요.
    5. .dt를 사용할 때는 반드시 datetime으로 변환한 후 사용하세요.
    6. 결과는 result 변수에 저장하세요.
    7. 그래프가 필요하면 plt.show()를 반드시 호출하세요.
    8. 코드만 출력하세요.
    """
    
    response = llm.invoke(prompt)
    return response.content

###################################################
# 7. 코드 실행
###################################################
original_df  = pd.read_excel(XLSX_PATH)
while True:

    question = input("\n질문(exit 종료) : ")
    
    if question.lower() == "exit":
        break

    # 항상 새로운 DataFrame 사용
    df = original_df.copy()

    code = make_code(question)

    print("\n생성된 코드")
    print("=" * 60)
    print(code)

    # 혹시 코드블록이 포함되면 제거
    code = re.sub(r"```python", "", code)
    code = re.sub(r"```", "", code)
    
    print("\n실행 결과")
    print("=" * 60)

    try:
        exec(
            code,
            {
                "df": df,
                "pd": pd,
                "plt": plt
            }
        )

    except Exception as e:
        print("실행 오류")
        print(e)

# 이 방식이면 아래 질문들을 모두 처리할 수 있습니다.

# 지역별 매출을 막대그래프로 보여줘.
# 상품별 총매출을 알려줘.
# 서울의 총매출은 얼마인가?
# 가장 많이 판매된 상품은?
# 지역별 평균 매출을 계산해줘.
# 월별 매출 추이를 선그래프로 그려줘.
# 수량이 가장 많은 판매 건은?
# 노트북 매출만 분석해줘.
# 부산 지역 판매 현황을 표로 보여줘.
# 지역별 판매 건수를 원그래프로 그려줘.