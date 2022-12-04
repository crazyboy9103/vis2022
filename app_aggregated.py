from turtle import width
import streamlit as st
import pandas as pd
import time
import altair as alt
import numpy as np 
import pydeck as pdk
from ipywidgets import HTML
from IPython.display import display
from utils import * 
import folium
from streamlit_folium import st_folium
import pickle

from plot_packed_bbchart_ex import * 
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
        st.header("Search")
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            세부직무 = st.multiselect(
                "세부 직무",
                # ("개발", "경영", "디자인", "마케팅", "영업", "리테일", "게임 제작", "HR", "미디어", "엔지니어링", "금융", "물류", "제조", "교육", "의료", "건설", "공공")
                직무리스트
            )
        
        with col2:
            # 경력 = st.selectbox(
            #     "경력", 
            #     ("인턴", "신입", "경력 (1년 이상)", "경력 (2년 이상)", "경력 (5년 이상)")
            # )
            경력 = st.number_input('경력 (신입은 0을 입력하세요)', 0, 100)

        with col3:
            학력 = st.multiselect(
                "학력",
                ("무관", "학사", "석사", "박사")
            )
            학력_dict = {"무관":0, "학사":1, "석사":2, "박사":3}
            학력 = 학력_dict[학력]
        
        

        with col4:

            전공 = st.multiselect(
                "전공",
                ('컴퓨터공학', '컴퓨터과학', '통계학', '응용통계학', '경영학', '데이터사이언스', '수학', '기계공학', '전자공학' )
            )

        with col5:
            스킬셋 = st.multiselect(
                "스킬셋",
                # ("C/C++", "Python", "AdobeXD", "반도체")
                스킬셋리스트
            )
        
        with col6:
            복지 = st.multiselect(
                "복지",
                # ('#야근없음','#유연근무','#주35시간', '#주4일근무','#육아휴직','#출산휴가','#리프레시휴가',
                # '#성과급','#상여금','#연말보너스','#스톡옵션',
                # '#수평적조직','#스타트업','#자율복장','#워크샵','#반려동물',
                # '#조식제공','#중식제공','#석식제공','#시리얼','#식비','#음료','#맥주','#커피','#와인','#샐러드','#과일','#간식',
                # '#사내카페','#사내식당','#주차','#수면실','#휴게실','#헬스장','#위워크','#수유실','#안마의자',
                # '#어린이집','#보육시설','#생일선물','#결혼기념일','#대출지원',
                # '#택시비','#차량지원','#원격근무','#셔틀버스','#기숙사','#사택','#재택근무',
                # '#건강검진','#단체보험','#의료비','#운동비','#문화비','#동호회','#복지포인트',
                # '#교육비','#직무교육','#세미나참가비','#컨퍼런스참가비','#자기계발','#도서구매비','#스터디지원','#어학교육','#해외연수',
                # '#산업기능요원','#전문연구요원','#인공지능','#IoT','#핀테크','#푸드테크','#Macbook','#iMac','#노트북','#통신비')
                복지리스트
            )

        with col7:
            가중치_세부직무 = st.slider('직무 가중치', min_value=1, max_value=10, \
                        value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  disabled=False, label_visibility="visible")
            가중치_경력 = st.slider('경력 가중치', min_value=1, max_value=10, \
                        value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  disabled=False, label_visibility="visible")
            가중치_학력 = st.slider('학력 가중치', min_value=1, max_value=10, \
                        value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  disabled=False, label_visibility="visible")
            가중치_전공 = st.slider('기업 정보 가중치', min_value=1, max_value=10, \
                        value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  disabled=False, label_visibility="visible")
            가중치_스킬셋 = st.slider('스킬셋 가중치', min_value=1, max_value=10, \
                        value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  disabled=False, label_visibility="visible")
            가중치_복지 = st.slider('복지 가중치', min_value=1, max_value=10, \
                        value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  disabled=False, label_visibility="visible")


        submitted = st.form_submit_button("Search🔎")

        if submitted:
            with st.container():
                print('submitted')
                print(submitted)

                my_bar = st.progress(1)
                for percent_complete in range(100):
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1)

                # success = st.success('100 jobs are waiting for you!', icon="😝")

                # 입력 정보 반영
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

                overview, detail_view = st.columns(2)

                with overview:
                    
                    # Calculate Fit score 
                    df_with_score = Overview(df, my_info, weights)                   

                    ### Draw circles 
                    cluster_data = Overview.cluster_data
                    
                    makers = BubbleMaker()
                    bubbles = makers.gen_bubble(cluster_data)
                    fig = makers.plot_bubbles(bubbles)
                    # fig.show()
                   
                with detail_view:
                    st.write('detail view')

class 공고:
    def __init__(self, 직무, 스택, 경력, 기업태그):
        self.직무 = 직무
        self.스택 = 스택
        self.경력 = 경력
        self.기업태그 = 기업태그