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
import glob, json
import streamlit.components.v1 as components

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
  cluster_filename =  "./data/cluster_data.pickle"
  with open(cluster_filename, 'rb') as f:
      cluster_dict = pickle.load(f)
  cluster_dict = cluster_dict[1]
  data_cluster_member = cluster_dict['c_members']

  whole_filename =  "./data/preprocessed_df.pickle"
  with open(whole_filename, 'rb') as f:
    data_all = pickle.load(f)

  data_cluster = data_all.loc[data_all['id'].isin(data_cluster_member)]
  
  json_file_path = "./data/job_posting/json"
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
    if 'keywords' not in st.session_state:
      st.session_state['keywords'] = set() 

    col2.subheader("Feature Explanation View")
    kw_cat = st.radio("어떤 특성의 핵심 키워드를 보고 싶으신가요?",('기술스택', '복지', '업종', '기업정보' ), horizontal=True)
  
    w_words = utils.word_count(data_cluster, "복지")
    i_words = utils.word_count(data_cluster, "업종")
    s_words = utils.word_count(data_cluster, "스킬셋")
    c_words = utils.word_count(data_cluster, "기업정보")

    # Tag
    if kw_cat == '복지':
      return_obj = wordcloud.visualize(w_words, tooltip_data_fields={
          'text':'복지 종류', 'value':'관련 공고 수'
      }, per_word_coloring=False, width = 800, height = 500, key="복지")

    
    # No tag
    elif kw_cat == '업종':
      return_obj = wordcloud.visualize(i_words, tooltip_data_fields={
          'text':'업종', 'value':'관련 공고 수'
      }, per_word_coloring=False, width = 800, height = 500, key="업종")
    
    # No tag
    elif kw_cat == '기술스택':
      return_obj = wordcloud.visualize(s_words, tooltip_data_fields={
          'text':'기술스택 종류', 'value':'관련 공고 수'
      }, per_word_coloring=False, width = 800, height = 500, key="기술스택")

    # Tag
    else: 
      return_obj = wordcloud.visualize(c_words, tooltip_data_fields={
          'text':'기업 이미지 및 규모', 'value':'관련 공고 수'
      }, per_word_coloring=False, width = 700, height = 400, key="기업정보")
    
    if return_obj != None and return_obj['clicked'] != None:
      tag = return_obj['clicked']['text']
      if tag in st.session_state['keywords']:
        st.session_state['keywords'].remove(tag)
      
      else:
        st.session_state['keywords'].add(tag)

    st.write(st.session_state['keywords'])


  full_comp_html = '''<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
      <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
  '''
  json_paths = glob.glob("./data/job_posting/json/*.json")
  keywords = st.session_state['keywords']

  for idx, path in enumerate(json_paths):
    data = json.load(open(path, "r"))
    tags = data.get("tags", [])
    tags = set(map(lambda tag: tag.split("#")[1], tags))
    

    기술스택 = data.get("tools", [])
    업종 = data.get("industry", None)

    inter = tags & keywords
    inter1 = set(기술스택) & keywords
    if len(inter) > 0 or len(inter1) > 0 or 업종 in keywords:
      name = data["company_name"]
      thumb_img = data["title_thumb_img"]
      main_tasks = data["main_tasks"]
      is_newbie = data["is_newbie"]
      location = data["location"]
      req = data["requirements"]
      
      sub_categories = data["sub_categories"]

      tasks_html = ''
      for task in main_tasks.split("\n"):
        if len(task.strip()) == 0:
          continue       
        tasks_html = tasks_html + f'<p>{task}</p>'

      req_html = ''
      for r in req.split("\n"):
        if len(r.strip()) == 0:
          continue
        req_html = req_html + f'<p>{r}</p>'

      content_html = f'''
    <div style="display: flex; margin: 10px 10px 10px 10px;">
    <img style="width: 300px; height: 300px;" src="{thumb_img}"/>
    <div style="margin-left: 20px;">
      <p style="text-decoration: underline; font-weight:bold;">주요업무</p>
      {tasks_html}
      <p style="text-decoration: underline; font-weight:bold;">자격요건</p>
      {req_html}
    </div>
    </div>
    '''
      
      full_comp_html += f'''<div id="accordion">
        <div class="card">
          <div style="display:flex;" class="card-header" id="headingOne">
            <img style="width: 150px; height: 150px; align-self: center;" src="{thumb_img}"/>
            <div>
              <div style="margin: 0 0 0 20px;">
                <div style="display: flex;">
                  <p style="text-decoration: underline; font-weight: bold; font-size:20px;">{name}</p> 
                  <button class="btn btn-link" style="width:10px; height:10px;" data-toggle="collapse" data-target="#collapse{idx}" aria-expanded="true" aria-controls="collapse{idx}">
                    자세히 보기
                  </button>
                </div>
                
                <p>{",".join(sub_categories)}</p> 
                <p>{' '.join(data.get("tags", []))}</p>
              </div>
        
              
            </div>
          </div>
          <div id="collapse{idx}" class="collapse" aria-labelledby="headingOne" data-parent="#accordion">
              {content_html}
            
          </div>
        </div>
      </div>'''      
      due = data["due_time"]
  components.html(full_comp_html,
    width=800,
    height=1200,
    scrolling=True
  )



  # for idx, path in enumerate(json_paths[:100]):
  #   data = json.load(open(path, "r"))
    
  #   name = data["company_name"]
  #   thumb_img = data["title_thumb_img"]
  #   main_tasks = data["main_tasks"]
  #   is_newbie = data["is_newbie"]
  #   location = data["location"]
  #   req = data["requirements"]
    
  #   sub_categories = data["sub_categories"]

  #   tasks_html = ''
  #   for task in main_tasks.split("\n"):
  #     if len(task.strip()) == 0:
  #       continue       
  #     tasks_html = tasks_html + f'<p>{task}</p>'

  #   req_html = ''
  #   for r in req.split("\n"):
  #     if len(r.strip()) == 0:
  #       continue
  #     req_html = req_html + f'<p>{r}</p>'

  #   content_html = f'''
  # <div style="display: flex; margin: 10px 10px 10px 10px;">
  # <img style="width: 300px; height: 300px;" src="{thumb_img}"/>
  # <div style="margin-left: 20px;">
  #   <p style="text-decoration: underline; font-weight:bold;">주요업무</p>
  #   {tasks_html}
  #   <p style="text-decoration: underline; font-weight:bold;">자격요건</p>
  #   {req_html}
  # </div>
  # </div>
  # '''
    
  #   full_comp_html += f'''<div id="accordion">
  #     <div class="card">
  #       <div style="display:flex;" class="card-header" id="headingOne">
  #         <img style="width: 150px; height: 150px; align-self: center;" src="{thumb_img}"/>
  #         <div>
  #           <div style="margin: 0 0 0 20px;">
  #             <div style="display: flex;">
  #               <p style="text-decoration: underline; font-weight: bold; font-size:20px;">{name}</p> 
  #               <button class="btn btn-link" style="width:10px; height:10px;" data-toggle="collapse" data-target="#collapse{idx}" aria-expanded="true" aria-controls="collapse{idx}">
  #                 자세히 보기
  #               </button>
  #             </div>
              
  #             <p>{",".join(sub_categories)}</p> 
  #             <p>{' '.join(data.get("tags", []))}</p>
  #           </div>
      
            
  #         </div>
  #       </div>
  #       <div id="collapse{idx}" class="collapse" aria-labelledby="headingOne" data-parent="#accordion">
  #           {content_html}
          
  #       </div>
  #     </div>
  #   </div>'''      
  #   due = data["due_time"]

  # components.html(full_comp_html,
  #   width=800,
  #   height=1200,
  #   scrolling=True
  # )