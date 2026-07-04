from langchain_openai import OpenAIEmbeddings
import sys
from pathlib import Path
from pydantic import BaseModel

sys.path.append(str(Path(__file__).resolve().parent.parent))
from llm_loader import init_custom_llm

llm = init_custom_llm()
# 문장
# ↓
# Embedding
# ↓
# 숫자(Vector)
# ↓
# 비슷한 숫자 찾기
# ↓
# 비슷한 문장 찾기
# ↓
# GPT에게 전달

# Embedding은 "문장을 숫자로 바꾸는 기술"이 아니라, "문장의 의미를 숫자로 표현하는 기술"입니다.


embedding = OpenAIEmbeddings()

text = "대한민국의 수도는 서울입니다."

vector = embedding.embed_query(text)

print("=" * 50)
print("원본 문장")
print(text)

print("\n벡터 길이")
print(len(vector))

print("\n앞의 10개 숫자")
print(vector[:10])

# ==================================================
# 원본 문장
# 대한민국의 수도는 서울입니다.

# 벡터 길이
# 1536

# 앞의 10개 숫자
# [0.009820127859711647, -0.016796590760350227, 0.011121895164251328, -0.01673339679837227, -0.028942205011844635, 0.012821775861084461, -0.04054436460137367, 0.010142410174012184, -0.014433187432587147, 0.0035798600874841213]