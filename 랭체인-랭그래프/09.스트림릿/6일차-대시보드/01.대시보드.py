# | 라이브러리                     | 활용              |
# | ------------------------- | --------------- |
# | pandas                    | 데이터 처리          |
# | matplotlib                | 기본 그래프          |
# | plotly                    | 인터랙티브 그래프       |
# | altair                    | Streamlit 기본 차트 |
# | requests                  | API 호출          |
# | yfinance                  | 주식 데이터          |
# | pydeck                    | 지도 시각화          |
# | folium + streamlit-folium | 지도 표시           |
# | streamlit-option-menu     | 메뉴 UI           |
# | streamlit-aggrid          | 고급 데이터 테이블      |

#https://docs.streamlit.io/develop/api-reference/charts

import streamlit as st
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "A": np.random.randn(20).cumsum(),
    "B": np.random.randn(20).cumsum()
})

st.line_chart(df)

import plotly.express as px

# Plotly에서 제공하는 iris 데이터셋
iris = px.data.iris()

fig = px.scatter(
    iris,
    x="sepal_length",
    y="petal_length",
    color="species"
)

st.plotly_chart(fig)

import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.DataFrame({
    "키":[170,175,180,165,172],
    "몸무게":[65,72,80,58,69],
    "성별":["남","남","남","여","여"]
})

fig = px.scatter(
    df,
    x="키",
    y="몸무게",
    color="성별"
)

st.plotly_chart(fig)


import pandas as pd
import plotly.express as px

df = pd.DataFrame({
    "과목":["국어","영어","수학","과학"],
    "점수":[90,75,82,88]
})

fig = px.bar(
    df,
    x="과목",
    y="점수",
    color="점수",
    title="학생 성적"
)

st.plotly_chart(fig, use_container_width=True)