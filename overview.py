import streamlit as st
import pandas as pd 
import altair as alt
import numpy as np 
import pydeck as pdk
import os 
import re
import pickle

from sklearn.cluster import KMeans

from utils import * 
from plot_packed_bbchart_ex import * 


### 공고 데이터 불러오기 
with open('./data/wanted_preprocessed.pickle', 'rb') as f:
    wanted_df = pickle.load(f)



### User input data 
global my_info
my_info =  {'경력':1, 
            '학력':1, 
            '전공':['컴퓨터공학', '무관'], 
            '스킬셋':['Python', 'C'], 
            '복지':['건강검진', '재택근무'],
            '세부직무': ['데이터 사이언티스트']}

weights = {'경력':1, 
            '학력':1, 
            '전공':1, 
            '스킬셋':1, 
            '복지':1,
            '세부직무': 1}


### Fit score 계산 
# 1) 경력, 학력
def agg1(x):
    """
    x: df['경력'] or df['학력'](dtype: pd.Series)
    global my_info: 내 정보 
    
    요구하는 경력/학력이 내가 가진 경력/학력보다 낮거나 같으면 매치된 것으로 판단 
    """
    matched = x<=my_info[x.name]
         
    return matched
    
    
# 2) 전공, 스킬셋, 복지, 세부직무
def agg2(x):
    """
    x: df['전공'] or df['스킬셋'] or df['복지'] or df['세부직무] (dtype: pd.Series)
    global my_info: 내 정보 
    
    공고에 표시된 전공, 스킬셋, 복지 중
    내가 선택한 전공, 스킬셋, 복지가 포함되었는지 판단
    """
       
    matched = x.apply(lambda y: len(y.intersection(my_info[x.name])) > 0)
    return matched

# 사용자 input 반영할 DF 생성
wanted_df_modified = wanted_df.copy()

# 사용자 정보와 일치 여부 판단
wanted_df_modified['경력'] = agg1(wanted_df['경력'])
wanted_df_modified['학력'] = agg1(wanted_df['학력'])
wanted_df_modified['전공'] = agg2(wanted_df['전공'])
wanted_df_modified['스킬셋'] = agg2(wanted_df['스킬셋'])
wanted_df_modified['복지'] = agg2(wanted_df['복지'])
wanted_df_modified['세부직무'] = agg2(wanted_df['세부직무'])

# 사용자로부터 받은 가중치 반영 
for col in ['세부직무','경력','학력','전공','스킬셋','복지']:
    wanted_df_modified[col] = wanted_df_modified[col].apply(lambda x: x* weights[col] )

# 최종 Fit score = Sum(weight * similarity)
wanted_df_modified['적합도'] = wanted_df_modified.iloc[:, 1:].sum(axis = 1)

### Clustering 
wanted_df_modified['cluster'] = 0
cluster_data = []

N_CLUSTERS = 7  # number of clusters in same score range 

for i in range(7):
    df = wanted_df_modified.loc[wanted_df_modified['적합도']==i, ['세부직무','경력','학력','전공','스킬셋','복지']]
    
    if len(df)>=N_CLUSTERS:
        kmeans = KMeans(n_clusters=N_CLUSTERS).fit(df)
        df['cluster'] = kmeans.labels_
        # 필요하면 넣기 
#         wanted_df_modified.iloc[df.index, -1] = kmeans.labels_
        
        for j in range(max(kmeans.labels_)):
            df_cluster = df.loc[df['cluster']==j, :]
            cluster = {'score':i, 'cid':j, 'c_members':list(wanted_df_modified.iloc[df_cluster.index, 0]), 'number':len(df_cluster)}
            cluster_data.append(cluster)



### Draw circles 
makers = BubbleMaker()
bubbles = makers.gen_bubble(cluster_data)
# pp(bubbles)
fig = makers.plot_bubbles(bubbles)
fig.show()

# # Data processing 
# latlon = pd.read_csv('data/Seoul_latlong_utf8.csv', encoding='cp949')  ## 서울 위경도 데이터
# latlon = latlon[['위도','경도']]

# dummy = pd.DataFrame({'count': 10, 'lat':[latlon['위도'][0]], 'lon':[latlon['경도'][0]], '업종':'제조업',
#                     '직무':'개발', '기술_스택':"C/C++, Python", '경력':"인턴, 신입"})

# # 직무 적합도 계산 (직무 적합도: # of 나의 스킬셋 / # of 요구되는 스킬셋 + normalize?)
# my_기술_스택, my_경력, my_직무  = ['Python'], ['신입'], ['개발'] ## 내 스킬: 사용자로부터 받아오기

# mine = my_기술_스택 + my_경력 + my_직무
# col = ['직무', '기술_스택', '경력']  ## 직무 적합도 계산에 활용할 컬럼들 

# dummy['적합도'] = dummy.apply(lambda x: cal_index(x, mine, col), axis = 1)

# # Multiselect box (업종)
# sectors = st.multiselect(
#     "업종 선택", list(dummy.업종), ['제조업']
# )

# # Slider (직무 적합도)
# job_idx = st.slider('직무 적합도', min_value=0, max_value=10, \
#     value=None, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None,  disabled=False, label_visibility="visible")

# # Map 
# if not sectors:
#     st.error('업종을 선택하세요', icon="🚨")  ## 업종 선택 안될 경우 에러 메시지 출력 
# else:
#     # Interaction
#     df = dummy[(dummy['업종']==sectors) & (dummy['적합도'] >= job_idx)] 

#     # Set viewport for the deckgl map
#     view = pdk.ViewState(latitude=37.584009, longitude=126.970626, zoom=3,)

#     # Create the scatter plot layer
#     Layer = pdk.Layer(
#             "ScatterplotLayer",
#             data=df,
#             pickable=True,
#             opacity=0.3,
#             stroked=True,
#             filled=True,
#             radius_scale=10,
#             radius_min_pixels=5,
#             radius_max_pixels=60,
#             line_width_min_pixels=1,
#             get_position=["lon", "lat"],
#             get_radius=['count'],
#             get_fill_color=[252, 136, 3],
#             get_line_color=[255,0,0],
#             tooltip="test test",
#         )

#     r = pdk.Deck(
#         layers=[Layer],
#         initial_view_state=view,
#         map_style="mapbox://styles/mapbox/light-v10",
#     )

#     st.write(f'당신에게 적합한 job position: {len(df)}개')
#     map = st.pydeck_chart(r)
