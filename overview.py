import streamlit as st
import pandas as pd 
import altair as alt
import numpy as np 
import pydeck as pdk

from utils import * 


# Data processing 
latlon = pd.read_csv('Seoul_latlong.csv', encoding='cp949')  ## 서울 위경도 데이터
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

    # Create the scatter plot layer
    Layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            pickable=True,
            opacity=0.3,
            stroked=True,
            filled=True,
            radius_scale=10,
            radius_min_pixels=5,
            radius_max_pixels=60,
            line_width_min_pixels=1,
            get_position=["lon", "lat"],
            get_radius=['count'],
            get_fill_color=[252, 136, 3],
            get_line_color=[255,0,0],
            tooltip="test test",
        )

    r = pdk.Deck(
        layers=[Layer],
        initial_view_state=view,
        map_style="mapbox://styles/mapbox/light-v10",
    )

    st.write(f'당신에게 적합한 job position: {len(df)}개')
    map = st.pydeck_chart(r)
