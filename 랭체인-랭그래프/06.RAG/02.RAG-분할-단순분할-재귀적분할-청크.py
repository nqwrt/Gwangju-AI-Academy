# 왜 Split 하는가?
# GPT에게 책 한 권을 한 번에 보내면 될까요?
# 긴 문서
# ↓
# 작은 조각
# ↓
# 검색하기 쉬움


# 청킹에서 중요한 개념 (오버랩의 실무적 중요성)
# 청크를 나눌 때 칼로 자르듯 나누면, 하필 그 경계선에 중요한 문맥이나 
# 핵심 단어가 걸쳐 있을 때 의미가 단절되는 '경계 문제'가 발생합니다.
# 이를 방지하기 위해 앞뒤 청크가 일정 부분 겹치도록(Sliding Window 방식) 설정하여 문맥의 연속성을 보장해야 합니다. 
# 일반적으로 chunk_overlap은 전체 chunk_size의 10~20% 수준으로 설정하는 것이 권장

# "RAG의 성능은 Split에서 절반 이상 결정
# 문서를 얼마나 잘 나누느냐가 검색 품질과 답변 품질에 큰 영향을 줌

text = """
인공지능(AI)은 인간의 학습 능력과 추론 능력을 컴퓨터가 수행하도록 만드는 기술입니다.
머신러닝은 AI의 한 분야이며 데이터를 이용하여 스스로 학습합니다.
딥러닝은 머신러닝의 한 종류이며 신경망을 이용하여 학습합니다.
RAG는 Retrieval-Augmented Generation의 약자이며 검색과 생성 모델을 결합한 기술입니다.
LangChain은 LLM 애플리케이션을 쉽게 만들기 위한 프레임워크입니다.
"""
from langchain_text_splitters import CharacterTextSplitter

# 한 Chunk에 최대 100글자(Character) 정도를 넣겠다."는 의미. CharacterTextSplitter에서는 chunk_size의 기준이 글자(Character)
splitter = CharacterTextSplitter(
    separator="\n", # "\n" 기준으로 자르려고 먼저 시도합니다.
    chunk_size=100,  
    chunk_overlap=0
)

# 처럼 100을 넘지 않는 범위에서 자연스럽게 잘립니다.
# 즉, 항상 정확히 100글자는 아닙니다.

chunks = splitter.split_text(text)

print(chunks)

for i, chunk in enumerate(chunks):
    print("="*40)
    print("Chunk", i+1)
    print(chunk)

# 7. Overlap 설명

# 이 부분을 그림으로 설명합니다.
# Overlap이 없으면

# Chunk1

# 안녕하세요.
# 제 이름은 홍길동입니다.
# 저는

# --------------------
# Chunk2
# 개발자입니다.


# 학생들에게 질문
# "저는" 다음 내용이 어디 있나요?
# ↓
# Chunk2
# 맥락이 끊깁니다.

#===================================================================================

RecursiveCharacterTextSplitter

# 이름 그대로
# Recursive(재귀적으로)
# 여러 기준을 순서대로 사용합니다.

# 기본 순서는
# 문단
# ↓
# 줄바꿈
# ↓
# 공백
# ↓
# 문자
# 입니다.

# 예를 들어
# 문단1
# 문단2
# 문단3

# 라면

# 먼저

# 문단 기준

# 으로 자릅니다.

# 문단이 너무 크면?

# ↓

# 줄바꿈

# 줄바꿈도 너무 크면?

# ↓

# 공백

# 공백도 없으면?

# ↓

# 문자 단위

# 즉

# 문단

# ↓

# 줄바꿈

# ↓

# 공백

# ↓

# 문자

# 순으로

# 계속 시도합니다.

from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
인공지능(AI)은 인간의 학습 능력과 추론 능력을 컴퓨터가 수행하도록 만드는 기술입니다.
머신러닝은 AI의 한 분야이며 데이터를 이용하여 스스로 학습합니다.
딥러닝은 머신러닝의 한 종류이며 신경망을 이용하여 학습합니다.
RAG는 Retrieval-Augmented Generation의 약자이며 검색과 생성 모델을 결합한 기술입니다.
LangChain은 LLM 애플리케이션을 쉽게 만들기 위한 프레임워크입니다.
"""

#**90% 이상 RecursiveCharacterTextSplitter**를 사용
splitter = RecursiveCharacterTextSplitter(
    chunk_size=80,
    chunk_overlap=20
)

chunks = splitter.split_text(text)

print("="*50)
print("Chunk 개수 :", len(chunks))
print("="*50)

for i, chunk in enumerate(chunks):

    print(f"\nChunk {i+1}")
    print("-"*30)
    print(chunk)
    print(f"\n글자수 : {len(chunk)}")


# | 문서 종류  | 추천 chunk_size |
# | ------ | ------------: |
# | 짧은 FAQ |       200~400 |
# | 일반 PDF |      500~1000 |
# | 기술 문서  |      800~1500 |
# | 법률 문서  |     1000~2000 |
# | 논문     |     1000~1500 |
