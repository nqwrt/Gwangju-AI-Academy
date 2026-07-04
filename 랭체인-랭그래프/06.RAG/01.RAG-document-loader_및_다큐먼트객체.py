from langchain_community.document_loaders import PyPDFLoader
#from langchain_community.document_loaders import OnlinePDFLoader
#pip install pdfminer

# TextLoader
# CSVLoader
# PyPDFLoader
# Docx2txtLoader =>  Word
# WebBaseLoader

# 1) PDF 로드
# loader = PyPDFLoader("sample.pdf")
# # Transformers 논문을 로드
loader = PyPDFLoader("https://arxiv.org/pdf/1706.03762.pdf")
pages = loader.load()

# 2) 문서 로드
documents = loader.load()

print(documents)
# 3) 확인
print(len(documents))
#print(documents[0].page_content)

#########################
# 여러 개의 url 지정 가능
from langchain_community.document_loaders import WebBaseLoader

# https://en.wikipedia.org/wiki/Transformer_(machine_learning_model)
# https://docs.python.org/3/tutorial/introduction.html
# https://realpython.com/python-kwargs-and-args/

loader = WebBaseLoader("https://en.wikipedia.org/wiki/Transformer_(machine_learning_model)")
docs = loader.load()

print(docs[0].page_content[:500])

# page_content: 문서에서 실제로 추출된 텍스트 본문입니다. 이후 LLM이 읽고 답변의 근거로 삼을 핵심 데이터입니다.
# metadata: 파일 경로, 페이지 번호, 생성일자, 작성자 등의 부가 정보가 담긴 딕셔너리입니다.


# RAG는 결국 “Document를 잘 쪼개고, 잘 검색하는 구조”다
# https://wikidocs.net/331285
