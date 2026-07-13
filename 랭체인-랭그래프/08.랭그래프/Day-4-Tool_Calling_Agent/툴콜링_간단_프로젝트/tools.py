"""
====================================================
tools.py

LangGraph Tool Calling 예제
- Calculator
- Date / Time
- DuckDuckGo Search

====================================================
"""

from datetime import datetime

from langchain_core.tools import tool

# DuckDuckGo Search
from langchain_community.tools import DuckDuckGoSearchRun


# =====================================================
# 계산기 Tool
# =====================================================

@tool
def calculator(expression: str) -> str:
    """
    수식을 계산합니다.

    예)
    10 + 20
    100 * 30
    (10 + 20) * 5
    """

    try:

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return f"계산 결과 : {result}"

    except Exception as e:

        return f"계산 오류 : {e}"


# =====================================================
# 현재 날짜 Tool
# =====================================================

@tool
def today() -> str:
    """
    오늘 날짜를 반환합니다.
    """

    return datetime.now().strftime("%Y-%m-%d")


# =====================================================
# 현재 시간 Tool
# =====================================================

@tool
def current_time() -> str:
    """
    현재 시간을 반환합니다.
    """

    return datetime.now().strftime("%H:%M:%S")


# =====================================================
# 현재 날짜 + 시간
# =====================================================

@tool
def now() -> str:
    """
    현재 날짜와 시간을 반환합니다.
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# =====================================================
# 웹 검색 Tool
# =====================================================
from langchain_community.tools import DuckDuckGoSearchResults
# search = DuckDuckGoSearchRun()

search = DuckDuckGoSearchResults(
    output_format="list",
    max_results=5,
    backend="text",
    region="kr-kr",
    safesearch="moderate",
    timelimit="d" # 하루
)

    # """
    # 인터넷에서 최신 정보를 검색하는 도구입니다.

    # 사용 조건:
    # - 오늘
    # - 현재
    # - 최신
    # - 뉴스
    # - 주가
    # - 환율
    # - 날씨
    # - 최근 발표
    # - 최근 출시
    # - 실시간 정보

    # 일반 지식 질문에는 사용하지 않습니다.
    # """
    # """
    # 인터넷 검색

    # 최신 정보 검색

    # 뉴스 검색

    # 주가 검색
    # """
@tool
def web_search(query: str) -> str:
    # """
    # 인터넷에서 최신 정보를 검색하는 도구입니다.

    # 사용 조건:
    # - 오늘
    # - 현재
    # - 최신
    # - 뉴스
    # - 주가
    # - 환율
    # - 날씨
    # - 최근 발표
    # - 최근 출시
    # - 실시간 정보

    # 일반 지식 질문에는 사용하지 않습니다.
    # """

    try:
        result = search.invoke(query)
        if result:
            return result

        return "검색 결과가 없습니다."

    except Exception as e:
        return f"검색 실패 : {e}"


# =====================================================
# Tool 목록
# =====================================================
# pip install geopy timezonefinder

# 이 방식은

# ✅ 뉴욕
# ✅ 룩셈부르크
# ✅ 광주
# ✅ 판교
# ✅ 도쿄
# ✅ 파리
# ✅ 리우데자네이루
# ✅ 케이프타운

# 처럼 거의 모든 도시를 지원합니다.

from datetime import datetime
from zoneinfo import ZoneInfo

from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

from langchain_core.tools import tool
# Geocoder
geolocator = Nominatim(user_agent="langgraph-agent")

# Timezone Finder
tf = TimezoneFinder()

@tool
def world_time(city: str) -> str:
    """
    도시의 현재 시간을 알려줍니다.

    예:
    - 뉴욕
    - 룩셈부르크
    - 서울
    - 광주
    - Paris
    - Tokyo
    """

    try:

        # 도시 → 위도/경도
        location = geolocator.geocode(city)

        if location is None:
            return f"'{city}' 위치를 찾을 수 없습니다."

        # 위도/경도로 TimeZone 찾기
        timezone = tf.timezone_at(
            lat=location.latitude,
            lng=location.longitude
        )

        if timezone is None:
            return "시간대를 찾을 수 없습니다."

        # 현재 시간
        now = datetime.now(
            ZoneInfo(timezone)
        )

        return (
            f"도시 : {location.address}\n"
            f"시간대 : {timezone}\n"
            f"현재 시간 : {now.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    except Exception as e:

        return str(e)
    
TOOLS = [
    calculator,
    today,
    current_time,
    now,
    web_search,
    world_time
]


# =====================================================
# 테스트
# =====================================================

if __name__ == "__main__":

    print("=" * 60)

    print(calculator.invoke(
        {
            "expression": "(10 + 20) * 3"
        }
    ))

    print()

    print(today.invoke({}))

    print()

    print(current_time.invoke({}))

    print()

    print(now.invoke({}))

    print()

    print(web_search.invoke(
        {
            "query": "오늘 삼성전자 주가는?"
        }
    ))

    print("=" * 60)