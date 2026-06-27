"""
tools.py

AI 투자 분석기에서 사용하는 Tool 함수 모음

1. 회사명 추출
2. Yahoo Finance 재무정보 조회
3. Yahoo Finance 뉴스 조회
"""

import yfinance as yf


# =====================================================
# 회사명 → Yahoo Finance Symbol
# =====================================================

TICKER_MAP = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "LG에너지솔루션": "373220.KS",
    "NAVER": "035420.KS",
    "카카오": "035720.KS",
    "현대차": "005380.KS",
    "기아": "000270.KS",
    "애플": "AAPL",
    "마이크로소프트": "MSFT",
    "엔비디아": "NVDA",
    "테슬라": "TSLA",
    "구글": "GOOGL",
    "아마존": "AMZN",
    "메타": "META",
}


# =====================================================
# 회사명 추출
# =====================================================

def extract_company(question: str) -> str:
    """
    사용자의 질문에서 회사명을 추출한다.
    """

    for company in TICKER_MAP.keys():

        if company in question:
            return company

    return ""


# =====================================================
# Yahoo Finance 객체 반환
# =====================================================

def get_stock(company: str):

    ticker = TICKER_MAP.get(company)

    if ticker is None:
        return None

    return yf.Ticker(ticker)


# =====================================================
# 재무정보 조회
# =====================================================

def get_finance(company: str) -> str:

    stock = get_stock(company)

    if stock is None:
        return "재무정보를 찾을 수 없습니다."

    info = stock.info

    result = f"""
        회사명 : {company}
        현재가 : {info.get("currentPrice")}
        시가총액 : {info.get("marketCap")}
        PER : {info.get("trailingPE")}
        PBR : {info.get("priceToBook")}
        ROE : {info.get("returnOnEquity")}
        배당수익률 : {info.get("dividendYield")}
        52주 최고가 : {info.get("fiftyTwoWeekHigh")}
        52주 최저가 : {info.get("fiftyTwoWeekLow")}
        """
    return result


# =====================================================
# 최근 뉴스 조회
# =====================================================

# def get_news(company: str) -> str:

#     stock = get_stock(company)

#     if stock is None:
#         return "뉴스를 찾을 수 없습니다."

#     news = stock.news

#     if len(news) == 0:
#         return "최근 뉴스가 없습니다."

#     result = ""

#     for i, item in enumerate(news[:5], start=1):
#         title = item.get("title", "")
#         publisher = item.get("publisher", "")
#         result += f"{i}. {title}\n"
#         result += f"   ({publisher})\n\n"
#     return result

import feedparser


def get_news(company):

    url = (
        f"https://news.google.com/rss/search?"
        f"q={company}&hl=ko&gl=KR&ceid=KR:ko"
    )

    feed = feedparser.parse(url)

    if len(feed.entries)==0:

        return "뉴스가 없습니다."

    result=""

    for i,item in enumerate(feed.entries[:5],1):

        result += f"{i}. {item.title}\n"
        result += f"{item.link}\n\n"

    return result
# =====================================================
# Tool 테스트
# =====================================================

if __name__ == "__main__":

    question = input("질문 : ")
    company = extract_company(question)

    print("=" * 60)
    print("회사명")
    print(company)
    print("=" * 60)
    print("재무정보")
    print(get_finance(company))
    print("=" * 60)
    print("뉴스")
    print(get_news(company))