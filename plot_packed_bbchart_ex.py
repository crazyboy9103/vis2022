import random
from plot_utils.bubble_maker import BubbleMaker
from pprint import pprint as pp
import streamlit as st
from streamlit_plotly_events import plotly_events


import plotly.graph_objects as go

import numpy as np
import streamlit as st


import webbrowser
import dash
from dash.exceptions import PreventUpdate
from dash import dcc, html
from dash.dependencies import Input, Output


'''
#cluster data 1개 format
: {
  'score': fit-score(1~9, int),
  'cid': cluster-id(str),
  'c_members': list of notice ids of cluster members in cluster,
  'number' : cluster size
}
'''

app = dash.Dash(__name__)

def generate_cluster(number, score=1): #1 child = 1 cluster
  global cid
  cluster = {
      'score': score,
      'cid': f'c-{cid}',
      'number': number,
      'c_members': [f'n-{cid * 10 + nid}' for nid in range(number)] #ids of cluster members
      }
  cid += 1
  return cluster

# clusters generation
cid = 0
fn = lambda x, y, z: print(x,y,z)

point_list = []
random.seed(42)

if 'ipsum_data' not in st.session_state:
  st.session_state['ipsum_data'] = []

  for i in range(50):
    number = random.randrange(1,250)
    score = random.randrange(1,8)
    st.session_state['ipsum_data'].append(generate_cluster(number, score))
cluster_data = st.session_state['ipsum_data']

if 'temp_points' not in st.session_state:
  st.session_state['temp_points'] = []
point_list = st.session_state['temp_points']


makers = BubbleMaker()
bubbles = makers.gen_bubble(cluster_data)
# pp(bubbles)
fig, map_dict = makers.plot_bubbles(bubbles, fn=fn)
# selected_points = plotly_events(fig, click_event=True, hover_event=True)


# app.layout = html.Div(
#    [
#       dcc.Graph(
#          id="graph_interaction",
#          figure=fig,
#       ),
#       html.Pre(id='data')
#    ]
# )

# @app.callback(Output('data', 'children'), Input('graph_interaction', 'clickData'))
# def open_url(clickData):
#     if clickData:
#         print(clickData)
#         webbrowser.open(clickData["points"][0]["customdata"][0])
#     else:
#         raise PreventUpdate
#       # return json.dumps(clickData, indent=2)
      
# if __name__ == '__main__':
#     app.run_server(debug=True)


# points = st.plotly_chart(fig, use_container_width=True)
points = plotly_events(fig, )
# hover_points = plotly_events(fig, hover_event=True)
# print(hover_points)

if points:
  idx = points[0]['curveNumber']
  points[0]['cid'] = map_dict[idx]
  point_list.append(points)

st.session_state['temp_points'] = point_list


st.write(point_list)

