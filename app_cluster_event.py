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
import plot_utils as pu

# x = st.select_slider('x', [1, 2, 3])  # 👈 this is a widget
# y = st.button('y')
# z = st.selectbox('z', ["test1", "test2"])
# w = st.multiselect("w", ["test1", "test2"])
# st.write(x, 'squared is', x * x)

# Using object notation
import numpy as np
import plotly.figure_factory as ff

# Add histogram data
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
fig = ff.create_distplot(
        hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!
st.plotly_chart(fig, use_container_width=True)

from streamlit_plotly_events import plotly_events

# Writes a component similar to st.write()
fig = px.line(x=[1], y=[1])
selected_points = plotly_events(fig)

# Can write inside of things using with!
with st.beta_expander('Plot'):
    fig = px.line(x=[1], y=[1])
    selected_points = plotly_events(fig)

# Select other Plotly events by specifying kwargs
fig = px.line(x=[1], y=[1])
selected_points = plotly_events(fig, click_event=False, hover_event=True)

# 직무 = st.sidebar.multiselect(
#     "직무",
#     ("개발", "경영", "디자인", "마케팅", "영업", "리테일", "게임 제작", "HR", "미디어", "엔지니어링", "금융", "물류", "제조", "교육", "의료", "건설", "공공")
# )
# 기술_스택 = st.sidebar.multiselect(
#     "스킬셋",
#     ("C/C++", "Python", "AdobeXD", "반도체")
# )
# 경력 = st.sidebar.selectbox(
#     "경력", 
#     ("인턴", "신입", "경력 (1년 이상)", "경력 (2년 이상)", "경력 (5년 이상)")
# )

# 추가_필터 = st.sidebar.multiselect(
#     "태그로 필터링",
#     ('#연봉업계평균이상', '#연봉상위1%', '#연봉상위2~5%', '#연봉상위6~10%', '#연봉상위11~20%',
#     '#누적투자100억이상',
#     '#인원성장', '#인원급성장',
#     '#퇴사율5%이하', '#퇴사율 6~10%',
#     '#50명이하', '#51~300명', '#301~1,000명','#1,001~10,000명', '#10,001명이상',
#     '#설립3년이하', '#설립4~9년', '#설립10년이상',
#     '#야근없음','#유연근무','#주35시간', '#주4일근무','#육아휴직','#출산휴가','#리프레시휴가',
#     '#성과급','#상여금','#연말보너스','#스톡옵션',
#     '#수평적조직','#스타트업','#자율복장','#워크샵','#반려동물',
#     '#조식제공','#중식제공','#석식제공','#시리얼','#식비','#음료','#맥주','#커피','#와인','#샐러드','#과일','#간식',
#     '#사내카페','#사내식당','#주차','#수면실','#휴게실','#헬스장','#위워크','#수유실','#안마의자',
#     '#어린이집','#보육시설','#생일선물','#결혼기념일','#대출지원',
#     '#택시비','#차량지원','#원격근무','#셔틀버스','#기숙사','#사택','#재택근무',
#     '#건강검진','#단체보험','#의료비','#운동비','#문화비','#동호회','#복지포인트',
#     '#교육비','#직무교육','#세미나참가비','#컨퍼런스참가비','#자기계발','#도서구매비','#스터디지원','#어학교육','#해외연수',
#     '#산업기능요원','#전문연구요원','#인공지능','#IoT','#핀테크','#푸드테크','#Macbook','#iMac','#노트북','#통신비')
# )

# class 공고:
#     def __init__(self, 직무, 스택, 경력, 기업태그):
#         self.직무 = 직무
#         self.스택 = 스택
#         self.경력 = 경력
#         self.기업태그 = 기업태그

# ###############################
# # Uncomment below for example
# # import streamlit as st
# # import pandas as pd
# # import numpy as np

# # st.title('Uber pickups in NYC')

# # DATE_COLUMN = 'date/time'
# # DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
# #             'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# @st.cache
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data

# data_load_state = st.text('Loading data...')
# data = load_data(10000)
# data_load_state.text("Done! (using st.cache)")

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)

# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)

# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)