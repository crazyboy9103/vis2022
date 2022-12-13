from turtle import width
import streamlit as st
import pandas as pd
import time
import altair as alt
import numpy as np 
import pydeck as pdk
from ipywidgets import HTML
from IPython.display import display
import utils
import streamlit_wordcloud as wordcloud
import glob,json
import streamlit.components.v1 as components
from utils import * 
import folium
from streamlit_folium import st_folium
from streamlit_plotly_events import plotly_events
import plotly.graph_objects as go
import pickle
from PIL import Image
from plot_utils.bubble_maker import BubbleMaker as BM

# from plot_packed_bbchart_ex import * 
from overview import * 


# Load preprocessed job posting data 
with open('./data/preprocessed_df.pickle', 'rb') as f:
    df = pickle.load(f)

직무리스트, 스킬셋리스트, 복지리스트 = set(), set(), set()

for a,b,c in zip(df.세부직무, df.스킬셋, df.복지):
    직무리스트 = 직무리스트.union(a)
    스킬셋리스트 = 스킬셋리스트.union(b)
    복지리스트 = 복지리스트.union(c)

# Using object notation
st.set_page_config(layout="wide")

with st.container():
    st.title("I got hired!😄")
    submitted = False
    sectors = None
    filtered_data = None

    with st.form("my_form"):
        st.header("Profile")
        col1, col2, col3, col4, col5, col6 = st.columns((1,0.7,0.8,1,1,1))
        with col1:
            세부직무 = st.multiselect(
                "세부 직무",
                직무리스트
            )

            가중치_세부직무 = st.slider('직무 가중치', min_value=1, max_value=10, \
                        value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  disabled=False, label_visibility="visible")
            

        with col2:
            경력 = st.number_input('경력 (신입은 0을 입력하세요)', 0, 100)
            가중치_경력 = st.slider('경력 가중치', min_value=1, max_value=10, \
                        value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  disabled=False, label_visibility="visible")
            
        with col3:
            학력 = st.multiselect(
                "학력",
                ("무관", "학사", "석사", "박사")
            )
            학력_dict = {"무관":0, "학사":1, "석사":2, "박사":3}
            if 학력:
                학력 = 학력_dict[학력[0]]
            
            가중치_학력 = st.slider('학력 가중치', min_value=1, max_value=10, \
                        value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  disabled=False, label_visibility="visible")
            
        

        with col4:

            전공 = st.multiselect(
                "전공",
                ('컴퓨터공학', '컴퓨터과학', '통계학', '응용통계학', '경영학', '데이터사이언스', '수학', '기계공학', '전자공학' )
            )

            가중치_전공 = st.slider('기업 정보 가중치', min_value=1, max_value=10, \
                        value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  disabled=False, label_visibility="visible")
            

        with col5:
            스킬셋 = st.multiselect(
                "스킬셋",
                스킬셋리스트
            )
            가중치_스킬셋 = st.slider('스킬셋 가중치', min_value=1, max_value=10, \
                        value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  disabled=False, label_visibility="visible")
            
        
        with col6:
            복지 = st.multiselect(
                "복지",
                복지리스트
            )

            가중치_복지 = st.slider('복지 가중치', min_value=1, max_value=10, \
                        value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  disabled=False, label_visibility="visible")        

        submitted = st.form_submit_button("Search🔎")


    if submitted:
        my_info =  {'경력':경력, 
                    '학력':학력, 
                    '전공':전공 + ['무관'], 
                    '스킬셋':스킬셋, 
                    '복지':복지,
                    '세부직무': 세부직무}

        weights = {'경력_score':가중치_경력, 
                    '학력_score':가중치_학력, 
                    '전공_score':가중치_전공, 
                    '스킬셋_score':가중치_스킬셋, 
                    '복지_score':가중치_복지,
                    '세부직무_score': 가중치_세부직무}
        overview = Overview(df, my_info, weights) 

        st.session_state['overview_my_info'] = my_info
        st.session_state['overview_weights'] = weights
        st.session_state['overview_obj'] = overview
        

    image = Image.open('colorbar.png')
    if 'overview_obj' in st.session_state:
        with st.container():
            overview = st.session_state['overview_obj']
            df_with_score = overview.df                  

            ### Draw circles 
            cluster_data = overview.cluster_data
            # st.write(cluster_data)
            col1, col2, col3, col4 = st.columns((0.8, 0.7, 1, 1.7), gap="medium")

            with col1:
                col1.subheader("Job Clusters")
                makers = BM()
                st.image(image)
                bubbles = makers.gen_bubble(cluster_data)
                # pop_a = mpatches.Patch(color='#5DC83F', label='Population Dataset 1')
                # pop_b = mpatches.Patch(color='#CE5D45', label='Population Dataset 2')
                # fig.legend(handles=[pop_a,pop_b])
                fig = go.Figure()
                # fig = st.plotly_chart(fig, use_container_width=True)
                fig.update_layout(width=270)
                print('width:',fig.layout.width)
                fig.update_layout(showlegend=True)
                if 'selected_cid' not in st.session_state:
                    st.session_state['selected_cid'] = -1
                cid = st.session_state['selected_cid']
                fig, map_dict = makers.plot_bubbles(bubbles, fig=fig, selected=cid)
                print(cid,cid)
                points = plotly_events(fig, )
                if points:
                    idx = points[0]['curveNumber']
                    st.session_state['selected_cid'] = map_dict[idx]
                    # fig, map_dict = makers.plot_bubbles(bubbles, fig=fig, selected=cid)
                # fig.update_layout(showlegend=True)
                

            with col2:
                col2.subheader("Fit Score")
                categories = ['경력','세부직무','학력','전공','스킬셋','복지']
               
                if 'selected_cid' in st.session_state:
                    cid = st.session_state['selected_cid']
                    for cluster in cluster_data:
                        if cluster['cid'] == cid:
                            data_cluster_member = cluster['c_members']
                            

                    data_cluster = df_with_score.loc[df_with_score['id'].isin(data_cluster_member)]
                    
                    st.session_state['data_cluster'] = data_cluster
                    st.session_state['cluster_member'] = data_cluster_member

                    # 클러스터 직무적합도 기준별 점수 * 10
                    c = list(data_cluster[['경력_score','세부직무_score','학력_score','전공_score','스킬셋_score','복지_score']].mean()*10)
                    c = list(map(lambda x: min(10, x), c))
                    #전체 직무적합도 기준별 점수          
                    o = list(df_with_score[['경력_score','세부직무_score','학력_score','전공_score','스킬셋_score','복지_score']].mean()*10)
                    # o = list(map(lambda x: min(10, x), o))
                    fig = go.Figure()

                    fig.add_trace(go.Scatterpolar(
                        r=c + [c[0]],
                        theta=categories + [categories[0]],
                        fill='toself',
                        name='클러스터',
                        hovertemplate = '<i>기준명</i>: %{theta}<br><i>적합도</i>: %{r}<br>'
                    ))
                    fig.add_trace(go.Scatterpolar(
                        r=o + [o[0]],
                        theta=categories + [categories[0]],
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
                        showlegend=True,
                        legend=dict(orientation="h", yanchor="top", y=1.1),
                        # showlegend=False,
                        width=220,
                        height=340,
                        margin=dict(l=30, r=30, t=20, b=0)
                    )
                    st.plotly_chart(fig)
                else:
                    data_cluster = df_with_score
                    o = list(df_with_score[['경력_score','세부직무_score','학력_score','전공_score','스킬셋_score','복지_score']].mean()*10)
                    fig = go.Figure()
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
                        showlegend=True,
                        legend=dict(orientation="h"),
                        # showlegend=False,
                        width=220,
                        height=340,
                        margin=dict(l=30, r=30, t=20, b=0)
                    )
                    st.plotly_chart(fig)

            with col3:
                if 'keywords' not in st.session_state:
                    st.session_state['keywords'] = set() 

                col3.subheader("Hot Kewords")
                kw_cat = st.radio("어떤 특성의 핵심 키워드를 보고 싶으신가요?",('기술스택', '복지', '업종', '기업정보' ), horizontal=True)
                
                w_words = utils.word_count(data_cluster, "복지")
                i_words = utils.word_count(data_cluster, "업종")
                s_words = utils.word_count(data_cluster, "스킬셋")
                c_words = utils.word_count(data_cluster, "기업정보")
                
                wc_width = 310#400
                wc_height = 230#300
                # Tag
                if kw_cat == '복지':
                    return_obj = wordcloud.visualize(w_words, tooltip_data_fields={
                        'text':'복지 종류', 'value':'관련 공고 수'
                    }, per_word_coloring=False, width = wc_width, height = wc_height, key="복지", max_words= 25)

                
                # No tag
                elif kw_cat == '업종':
                    return_obj = wordcloud.visualize(i_words, tooltip_data_fields={
                        'text':'업종', 'value':'관련 공고 수'
                    }, per_word_coloring=False, width = wc_width, height = wc_height, key="업종", max_words= 25)
                
                # No tag
                elif kw_cat == '기술스택':
                    return_obj = wordcloud.visualize(s_words, tooltip_data_fields={
                        'text':'기술스택 종류', 'value':'관련 공고 수'
                    }, per_word_coloring=False, width = wc_width, height = wc_height, key="기술스택", max_words= 25)

                # Tag
                else: 
                    return_obj = wordcloud.visualize(c_words, tooltip_data_fields={
                        'text':'기업 이미지 및 규모', 'value':'관련 공고 수'
                    }, per_word_coloring=False, width = wc_width, height = wc_height, key="기업정보", max_words= 25)
                
                if return_obj != None:
                    if return_obj['clicked'] != None and return_obj['hovered'] != None:
                        tag = return_obj['clicked']['text']
                        if return_obj["clicked"]['text'] == return_obj["hovered"]['text']:
                            st.session_state['keywords'].add(tag)                   

                

                md = ""
                for keyword in st.session_state['keywords']:
                    md = md + f"* {keyword}\n"
                my_md = st.markdown(md)
                # my_md = st.markdown(" \n\n")
                # if st.button("리셋"):
                #     st.session_state['keywords'] = set()
                #     my_md.empty()

                ###
        
        # comp_cont = st.container()
            with col4:
                full_comp_html = '''<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
                    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
                    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
                '''
                json_paths = glob.glob("./data/job_posting/json/*.json")
                keywords = st.session_state['keywords']
                if 'cluster_member' in st.session_state:
                    for idx, cid in enumerate(st.session_state['cluster_member']):
                        path = f'./data/job_posting/json/{cid}.json'
                        data = json.load(open(path, "r"))
                        tags = data.get("tags", [])
                        tags = set(map(lambda tag: tag.split("#")[1], tags))
                        

                        기술스택 = set(data.get("tools", []))
                        업종 = data.get("industry", None)

                        inter = tags & keywords
                        inter1 = 기술스택 & keywords
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
                        
                            full_comp_html += f'''
                            <div id="accordion">
                                <div class="card">
                                <div style="display:flex;" class="card-header" id="headingOne">
                                    <img style="width: 150px; height: 150px; align-self: center;" src="{thumb_img}"/>
                                    <div>
                                    <div style="margin: 0 0 0 20px;">
                                        <div style="display: flex;">
                                        <p style="text-decoration: underline; font-weight: bold; font-size:20px;">{name}</p> 
                                        <button class="btn btn-link" style="width:30px; height:10px;" data-toggle="collapse" data-target="#collapse{idx}" aria-expanded="true" aria-controls="collapse{idx}">
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
                else:
                    for idx, path in enumerate(json_paths):
                        data = json.load(open(path, "r"))
                        tags = data.get("tags", [])
                        tags = set(map(lambda tag: tag.split("#")[1], tags))
                        

                        기술스택 = set(data.get("tools", []))
                        업종 = data.get("industry", None)

                        inter = tags & keywords
                        inter1 = 기술스택 & keywords
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
                        
                            full_comp_html += f'''
                            <div id="accordion">
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

                components.html(full_comp_html,
                    # width=1400,
                    height=420,
                    scrolling=True
                )


    # if submitted:
    #     print('submitted')
    #     print(submitted)

    #     my_bar = st.progress(1)
    #     for percent_complete in range(100):
    #         time.sleep(0.1)
    #         my_bar.progress(percent_complete + 1)

        # success = st.success('100 jobs are waiting for you!', icon="😝")

    # 입력 정보 반영
    


        
        
        
        




class 공고:
    def __init__(self, 직무, 스택, 경력, 기업태그):
        self.직무 = 직무
        self.스택 = 스택
        self.경력 = 경력
        self.기업태그 = 기업태그