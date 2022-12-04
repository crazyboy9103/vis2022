import streamlit as st
import pandas as pd
import numpy as np
import json
import glob
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
import streamlit_wordcloud as wordcloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import utils
from konlpy.tag import * 
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
# with st.container():
#   st.header("클러스터 뷰")
#   tab1, tab2, tab3 = st.tabs(["상세 직무적합도", "핵심 키워드", "업종 비율"])

#   # metric 설계:
#   # 직무적합도 metric = 경력_가중치*(경력 유무(0,1))+희망직무_가중치*(희망직무 유무(0,1))+학위 및 전공 가중치*(학위 및 전공 부합 유무(0,1))+스킬셋_가중치*(스킬셋 부합 유무(0,1))+복지_가증치*(복지 부합 유무(0,1)) -> 한 공고 당 직무적합도 점수
#   # 자격요건은 전공이나 학위 등이 될 수 있을듯
#   # 클러스터별 직무적합도 = 공고 직무적합도의 클러스터별(산업별) 평균 - 기준(경력, 희망직무, 학위/전공, 스킬셋, 복지) 점수 별로 구하기

#   categories = ['경력','희망직무','자격요건',
#                 '스킬셋', '복지']
#   #가중치
#   expert_w, position_w, degree_w, skill_w, welfare_w = 5,4,3,2,1

#   # 클러스터 직무적합도 기준별 점수 * 10
#   c_e, c_p, c_d, c_s, c_w = 3.3,4.5,7.6,5.2,6.3
#   c = [c_e, c_p, c_d, c_s, c_w]
#   #전체 직무적합도 기준별 점수
#   o_e, o_p, o_d, o_s, o_w = 2,3,4,2.8,1.7
#   o = [o_e, o_p, o_d, o_s, o_w]

#   with tab1:
#     fig = go.Figure()

#     fig.add_trace(go.Scatterpolar(
#           r=c,
#           theta=categories,
#           fill='toself',
#           name='제조',
#           hovertemplate = '<i>기준명</i>: %{theta}<br><i>적합도</i>: %{r}<br>'
#     ))
#     fig.add_trace(go.Scatterpolar(
#           r=o,
#           theta=categories,
#           fill='toself',
#           name='전체',
#           hovertemplate = '<i>기준명</i>: %{theta}<br><i>적합도</i>: %{r}<br>'
#     ))

#     fig.update_layout(
#       polar=dict(
#         radialaxis=dict(
#           visible=True,
#           range=[0, 10]
#         )),
#       showlegend=False
#     )

#     st.plotly_chart(fig, use_container_width=True)


#   with tab2:
#     description= "라닉스는 반도체 소프트웨어 융합기술을 바탕으로 최첨단의 비메모리 반도체 칩을 설계/개발하는 80명 규모의 강소기업 입니다. 2003년 설립되어 자동차와 사물인터넷의 핵심 기술인 무선 통신과 보안용 반도체 및 S/W, H/W 솔루션 등의 기술을 융합하여 사업화 하는 혁신융합기술 기업입니다. 2019년 코스닥시장에 상장하였고, 21년에는 중국지사를 설립하여 해외 시장의 기회도 넓혀 나가고 있습니다. \n\n자율주행자동차를 완성하기 위한 필수 요소 중 하나인 V2X(Vehicle to Everyting) 통신 모뎀 기술을 국내 기업으로는 유일하게 개발하여 솔루션을 보유하고 있으며, IoT 산업의 발전을 위해 해결해야 하는 해킹 방어용 보안/인증 칩 솔루션을 선도적으로 개발 확보해 나가고 있습니다"
#     max_word = st.slider("Max words", 0, 50, 0)
#     # max_font = st.sidebar.slider("Max Font Size", 20, 50, 25)
#     # random = st.sidebar.slider("Random State", 30, 100, 42 )
#     wc = utils.cloud(description, max_word=max_word)
#     plt.figure(figsize=(10,10))
#     fig, ax = plt.subplots()
#     plt.imshow(wc, interpolation='bilinear')
#     plt.axis("off")
#     st.pyplot(fig)

  # metric 설계:
  # 직무적합도 metric = 경력_가중치*(경력 유무(0,1))+희망직무_가중치*(희망직무 유무(0,1))+학위 및 전공 가중치*(학위 및 전공 부합 유무(0,1))+스킬셋_가중치*(스킬셋 부합 유무(0,1))+복지_가증치*(복지 부합 유무(0,1)) -> 한 공고 당 직무적합도 점수
  # 자격요건은 전공이나 학위 등이 될 수 있을듯
  # 클러스터별 직무적합도 = 공고 직무적합도의 클러스터별(산업별) 평균 - 기준(경력, 희망직무, 학위/전공, 스킬셋, 복지) 점수 별로 구하기

categories = ['경력','희망직무','자격요건',
              '스킬셋', '복지']
#가중치
expert_w, position_w, degree_w, skill_w, welfare_w = 5,4,3,2,1

# 클러스터 직무적합도 기준별 점수 * 10
c_e, c_p, c_d, c_s, c_w = 3.3,4.5,7.6,5.2,6.3
c = [c_e, c_p, c_d, c_s, c_w]
#전체 직무적합도 기준별 점수
o_e, o_p, o_d, o_s, o_w = 2,3,4,2.8,1.7
o = [o_e, o_p, o_d, o_s, o_w]

st.header("클러스터 뷰")

with st.container():
  
  col1, col2, col3 = st.columns([1.2,1,1.2])
  with col1:
    col1.subheader("Fit Score")
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
          r=c,
          theta=categories,
          fill='toself',
          name='제조',
          hovertemplate = '<i>기준명</i>: %{theta}<br><i>적합도</i>: %{r}<br>'
    ))
    fig.add_trace(go.Scatterpolar(
          r=o,
          theta=categories,
          fill='toself',
          name='전체',
          hovertemplate = '<i>기준명</i>: %{theta}<br><i>적합도</i>: %{r}<br>'
    ))

    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 10]
        )),
      showlegend=False,
      width=1200,
      height=400

    )

    st.plotly_chart(fig, use_container_width=True)

  with col2:
    col2.subheader("Keyword")
    description= "라닉스는 반도체 소프트웨어 융합기술을 바탕으로 최첨단의 비메모리 반도체 칩을 설계/개발하는 80명 규모의 강소기업 입니다. 2003년 설립되어 자동차와 사물인터넷의 핵심 기술인 무선 통신과 보안용 반도체 및 S/W, H/W 솔루션 등의 기술을 융합하여 사업화 하는 혁신융합기술 기업입니다. 2019년 코스닥시장에 상장하였고, 21년에는 중국지사를 설립하여 해외 시장의 기회도 넓혀 나가고 있습니다. \n\n자율주행자동차를 완성하기 위한 필수 요소 중 하나인 V2X(Vehicle to Everyting) 통신 모뎀 기술을 국내 기업으로는 유일하게 개발하여 솔루션을 보유하고 있으며, IoT 산업의 발전을 위해 해결해야 하는 해킹 방어용 보안/인증 칩 솔루션을 선도적으로 개발 확보해 나가고 있습니다"
    # max_word = st.slider("Max words", 0, 50, 0)
    # # max_font = st.sidebar.slider("Max Font Size", 20, 50, 25)
    # # random = st.sidebar.slider("Random State", 30, 100, 42 )
    # wc = utils.cloud(description, max_word=max_word)
    # plt.figure(figsize=(10,10))
    # fig, ax = plt.subplots()
    # plt.imshow(wc, interpolation='bilinear')
    # plt.axis("off")
    # st.pyplot(fig)
    words = [
    dict(text="라닉스", value=16000, color="#b5de2b", country="US", industry="Cryptocurrency"),
    dict(text="Personio", value=8500, color="#b5de2b", country="DE", industry="Human Resources"),
    dict(text="Boohoo", value=6700, color="#b5de2b", country="UK", industry="Beauty"),
    dict(text="Deliveroo", value=13400, color="#b5de2b", country="UK", industry="Delivery"),
    dict(text="SumUp", value=8300, color="#b5de2b", country="UK", industry="Credit Cards"),
    dict(text="CureVac", value=12400, color="#b5de2b", country="DE", industry="BioPharma"),
    dict(text="Deezer", value=10300, color="#b5de2b", country="FR", industry="Music Streaming"),
    dict(text="Eurazeo", value=31, color="#b5de2b", country="FR", industry="Asset Management"),
    dict(text="Drift", value=6000, color="#b5de2b", country="US", industry="Marketing Automation"),
    dict(text="Twitch", value=4500, color="#b5de2b", country="US", industry="Social Media"),
    dict(text="Plaid", value=5600, color="#b5de2b", country="US", industry="FinTech"),
]
  return_obj = wordcloud.visualize(words, tooltip_data_fields={
      'text':'Company', 'value':'Mentions', 'country':'Country of Origin', 'industry':'Industry'
  }, per_word_coloring=False, width = 1000, height = 600)


with col3:
  col3.subheader("업종 별 공고 수")
  data_canada = px.data.gapminder().query("country == 'Canada'")
  fig = px.bar(data_canada, x='year', y='pop', color="year")
  fig.update(layout_coloraxis_showscale=False)
  fig.update_layout(
    autosize=False,
    width=1200,
    height=300)
  st.plotly_chart(fig, use_container_width=True)


with st.expander("업종 상세 필터"):
    st.multiselect("업종",["IT, 컨텐츠", "건설", "교육", "금융", "기타 서비스업", "물류, 운송", "보건, 사회복지", "부동산", "사업지원", "숙박, 음식점", "예술, 스포츠, 여가", "전기, 가스", "전문, 과학기술", "제조", "판매, 유통"])












