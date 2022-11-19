import streamlit as st
import pandas as pd 
import altair as alt
import numpy as np 
import pydeck as pdk


# Data processing 
latlon = pd.read_csv('Seoul_latlong.csv', encoding='cp949')  ## 서울 위경도 데이터
latlon = latlon[['위도','경도']]

dummy = pd.DataFrame({'count': 10, 'lat':[latlon['위도'][0]], 'lon':[latlon['경도'][0]], '업종':'제조업'})

# multiselect box
sectors = st.multiselect(
    "업종 선택", list(dummy.업종), ['제조업']
)

if not sectors:
    st.error('업종을 선택하세요', icon="🚨")  ## 업종 선택 안될 경우 에러 메시지 출력 
else:
    # Interaction
    df = dummy[dummy['업종']==sectors] 

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

    map = st.pydeck_chart(r)
