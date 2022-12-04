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
import pickle

st.set_page_config(layout="wide")


  # metric 설계:
  # 직무적합도 metric = 경력_가중치*(경력 유무(0,1))+희망직무_가중치*(희망직무 유무(0,1))+학위 및 전공 가중치*(학위 및 전공 부합 유무(0,1))+스킬셋_가중치*(스킬셋 부합 유무(0,1))+복지_가증치*(복지 부합 유무(0,1)) -> 한 공고 당 직무적합도 점수
  # 자격요건은 전공이나 학위 등이 될 수 있을듯
  # 클러스터별 직무적합도 = 공고 직무적합도의 클러스터별(산업별) 평균 - 기준(경력, 희망직무, 학위/전공, 스킬셋, 복지) 점수 별로 구하기


categories = ['세부직무','경력','학력','전공','스킬셋','복지']
#가중치
position_w, expert_w, degree_w, major_w, skill_w, welfare_w = 5,4,3,3.5,2,1



st.header("Cluster View")

with st.container():


  cluster_filename =  "H:/황예진/대학원/2022-2/시각화/vis2022/data/cluster_data.pickle"
  with open(cluster_filename, 'rb') as f:
      cluster_dict = pickle.load(f)
  cluster_dict = cluster_dict[1]
  data_cluster_member = cluster_dict['c_members']

  whole_filename =  "H:/황예진/대학원/2022-2/시각화/vis2022/data/preprocessed_df.pickle"
  with open(whole_filename, 'rb') as f:
    data_all = pickle.load(f)

  data_cluster = data_all.loc[data_all['id'].isin(data_cluster_member)]
  
  json_file_path = "H:/황예진/대학원/2022-2/시각화/vis2022/data/job_posting/json"
  file_list = glob.glob(json_file_path + "/*")
  data_dict = dict()

  for filename in file_list:
    with open(filename, 'r') as file:
        json_data = json.load(file)
        data_dict[json_data['id']] = json_data

  col1, col2 = st.columns((0.5,1))
  with col1:
    col1.subheader("Score Explanation view")
    
    # 클러스터 직무적합도 기준별 점수 * 10
    
    c = list(data_cluster[['세부직무_score','경력_score','학력_score','전공_score','스킬셋_score','복지_score']].mean()*10)

    #전체 직무적합도 기준별 점수

    
    o = list(data_all[['세부직무_score','경력_score','학력_score','전공_score','스킬셋_score','복지_score']].mean()*10)

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
          r=c,
          theta=categories,
          fill='toself',
          name='클러스터',
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

    st.plotly_chart(fig)

  with col2:
    col2.subheader("Feature Explanation View")
    kw_cat = st.radio("어떤 특성의 핵심 키워드를 보고 싶으신가요?",('기술스택', '복지', '업종', '기업정보' ), horizontal=True)
    # description= "라닉스는 반도체 소프트웨어 융합기술을 바탕으로 최첨단의 비메모리 반도체 칩을 설계/개발하는 80명 규모의 강소기업 입니다. 2003년 설립되어 자동차와 사물인터넷의 핵심 기술인 무선 통신과 보안용 반도체 및 S/W, H/W 솔루션 등의 기술을 융합하여 사업화 하는 혁신융합기술 기업입니다. 2019년 코스닥시장에 상장하였고, 21년에는 중국지사를 설립하여 해외 시장의 기회도 넓혀 나가고 있습니다. \n\n자율주행자동차를 완성하기 위한 필수 요소 중 하나인 V2X(Vehicle to Everyting) 통신 모뎀 기술을 국내 기업으로는 유일하게 개발하여 솔루션을 보유하고 있으며, IoT 산업의 발전을 위해 해결해야 하는 해킹 방어용 보안/인증 칩 솔루션을 선도적으로 개발 확보해 나가고 있습니다"
    # max_word = st.slider("Max words", 0, 50, 0)
    # # max_font = st.sidebar.slider("Max Font Size", 20, 50, 25)
    # # random = st.sidebar.slider("Random State", 30, 100, 42 )
    # wc = utils.cloud(description, max_word=max_word)
    # plt.figure(figsize=(10,10))
    # fig, ax = plt.subplots()
    # plt.imshow(wc, interpolation='bilinear')
    # plt.axis("off")
    # st.pyplot(fig)
    w_words = utils.word_count(data_cluster, "복지")
    i_words = utils.word_count(data_cluster, "업종")
    s_words = utils.word_count(data_cluster, "스킬셋")
    c_words = utils.word_count(data_cluster, "기업정보")

    if kw_cat == '복지':
      
      return_obj = wordcloud.visualize(w_words, tooltip_data_fields={
          'text':'복지 종류', 'value':'관련 공고 수'
      }, per_word_coloring=False, width = 800, height = 500)
      print(return_obj)

    elif kw_cat == '업종':

      return_obj = wordcloud.visualize(i_words, tooltip_data_fields={
          'text':'기술스택 종류', 'value':'관련 공고 수'
      }, per_word_coloring=False, width = 800, height = 500)

      print(return_obj)
      
    elif kw_cat == '기술스택':
      
      return_obj = wordcloud.visualize(s_words, tooltip_data_fields={
          'text':'기술스택 종류', 'value':'관련 공고 수'
      }, per_word_coloring=False, width = 800, height = 500)
      print(return_obj)

    else:
      
      return_obj = wordcloud.visualize(c_words, tooltip_data_fields={
          'text':'기업 이미지 및 규모', 'value':'관련 공고 수'
      }, per_word_coloring=False, width = 700, height = 400)
      print(return_obj)












