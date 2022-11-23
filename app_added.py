###############################
# Widgets
# st.title("Title")
# st.header("Header")
# st.subheader("subheader")

# Write text
# st.write("Write Something")

# Cache for performance 
# use @st.cache decorator 

# Button
# if st.button("click button"):
#     st.write("Button clicked..")

# Checkbox 
# if st.checkbox('check me'):
#     st.write('checked')

# Multiselect 
# multi_select = st.multiselect('Please select somethings in multi selectbox!',
#                             ['A', 'B', 'C', 'D'])
# st.write('You selected:', multi_select)

# Slider
# values = st.slider('Select a range of values', 0.0, 100.0, (25.0, 75.0))
# st.write('Values:', values)

# Charts 
# st.line_chart
# st.area_chart
# st.bar_chart
# st.pyplot
# st.altair_chart
# st.vega_lite_chart
# st.plotly_chart
# st.bokeh_chart
# st.pydeck_chart
# st.graphviz_chart
# st.map

# Messages
# st.success("Success")
# st.error("Error")
# st.warning("Warning")
# st.info("Info")
# import time

# with st.spinner('Wait for it...'):
#     time.sleep(5)
# st.success('Done!')

# For multipage app
# Create closures for pages

###############################
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

# x = st.select_slider('x', [1, 2, 3])  # 👈 this is a widget
# y = st.button('y')
# z = st.selectbox('z', ["test1", "test2"])
# w = st.multiselect("w", ["test1", "test2"])
# st.write(x, 'squared is', x * x)

# Using object notation

with st.form("my_form"):
    with st.sidebar:
        st.sidebar.header("I got hired!😄")
        직무 = st.sidebar.multiselect(
            "직무",
            ("개발", "경영", "디자인", "마케팅", "영업", "리테일", "게임 제작", "HR", "미디어", "엔지니어링", "금융", "물류", "제조", "교육", "의료", "건설", "공공")
        )
        기술_스택 = st.sidebar.multiselect(
            "스킬셋",
            ("C/C++", "Python", "AdobeXD", "반도체")
        )
        경력 = st.sidebar.selectbox(
            "경력", 
            ("인턴", "신입", "경력 (1년 이상)", "경력 (2년 이상)", "경력 (5년 이상)")
        )

        추가_필터 = st.sidebar.multiselect(
            "태그로 필터링",
            ('#연봉업계평균이상', '#연봉상위1%', '#연봉상위2~5%', '#연봉상위6~10%', '#연봉상위11~20%',
            '#누적투자100억이상',
            '#인원성장', '#인원급성장',
            '#퇴사율5%이하', '#퇴사율 6~10%',
            '#50명이하', '#51~300명', '#301~1,000명','#1,001~10,000명', '#10,001명이상',
            '#설립3년이하', '#설립4~9년', '#설립10년이상',
            '#야근없음','#유연근무','#주35시간', '#주4일근무','#육아휴직','#출산휴가','#리프레시휴가',
            '#성과급','#상여금','#연말보너스','#스톡옵션',
            '#수평적조직','#스타트업','#자율복장','#워크샵','#반려동물',
            '#조식제공','#중식제공','#석식제공','#시리얼','#식비','#음료','#맥주','#커피','#와인','#샐러드','#과일','#간식',
            '#사내카페','#사내식당','#주차','#수면실','#휴게실','#헬스장','#위워크','#수유실','#안마의자',
            '#어린이집','#보육시설','#생일선물','#결혼기념일','#대출지원',
            '#택시비','#차량지원','#원격근무','#셔틀버스','#기숙사','#사택','#재택근무',
            '#건강검진','#단체보험','#의료비','#운동비','#문화비','#동호회','#복지포인트',
            '#교육비','#직무교육','#세미나참가비','#컨퍼런스참가비','#자기계발','#도서구매비','#스터디지원','#어학교육','#해외연수',
            '#산업기능요원','#전문연구요원','#인공지능','#IoT','#핀테크','#푸드테크','#Macbook','#iMac','#노트북','#통신비')
        )

        submitted = st.form_submit_button("Search🔎")
    if submitted:
        st.write("직무:", 직무[0])
        st.write("스킬셋:", 기술_스택[0])
        st.write("경력:", 경력)
        st.write("추가 필터:", 추가_필터[0])

        my_bar = st.progress(0)

        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1)
        success = st.success('100 jobs are waiting for you!', icon="😝")

        # Data processing 
        latlon = pd.read_csv('./data/Seoul_latlong_utf8.csv')  ## 서울 위경도 데이터
        latlon = latlon[['위도','경도']]

        dummy = pd.DataFrame({'count': 10, 'lat':[latlon['위도'][0]], 'lon':[latlon['경도'][0]], '업종':'제조업',
                            '직무':'개발', '기술_스택':"C/C++, Python", '경력':"인턴, 신입"})

        # 직무 적합도 계산 (직무 적합도: # of 나의 스킬셋 / # of 요구되는 스킬셋 + normalize?)
        my_기술_스택, my_경력, my_직무  = ['Python'], ['신입'], ['개발'] ## 내 스킬: 사용자로부터 받아오기

        mine = my_기술_스택 + my_경력 + my_직무
        col = ['직무', '기술_스택', '경력']  ## 직무 적합도 계산에 활용할 컬럼들 

        dummy['적합도'] = dummy.apply(lambda x: cal_index(x, mine, col), axis = 1)

        # Multiselect box (업종)
        sectors = st.multiselect(
            "업종 선택", list(dummy.업종), ['제조업']
        )

        # Slider (직무 적합도)
        job_idx = st.slider('직무 적합도', min_value=0, max_value=10, \
            value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  disabled=False, label_visibility="visible")

        # Map 
        if not sectors:
            st.error('업종을 선택하세요', icon="🚨")  ## 업종 선택 안될 경우 에러 메시지 출력 
        else:
            # Interaction
            df = dummy[(dummy['업종']==sectors) & (dummy['적합도'] >= job_idx)] 

            # Set viewport for the deckgl map
            view = pdk.ViewState(latitude=37.584009, longitude=126.970626, zoom=3,)
            
            m = folium.Map(location=[37.584009, 126.970626], zoom_start=16)
            folium.Marker(
                [37.584009, 126.970626], popup='<a href = "https://www.wanted.co.kr/wd/96351" target=_blink>파스토</a>', tooltip="<b>기업명:</b>파스토<br><b>직무:</b>AI Engineer"
            ).add_to(m)

            # call to render Folium map in Streamlit
            st_data = st_folium(m, width=725)

class 공고:
    def __init__(self, 직무, 스택, 경력, 기업태그):
        self.직무 = 직무
        self.스택 = 스택
        self.경력 = 경력
        self.기업태그 = 기업태그