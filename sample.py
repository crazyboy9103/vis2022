import plotly.graph_objects as go

import numpy as np
import streamlit as st
import webbrowser

import dash
from dash.exceptions import PreventUpdate
from dash import dcc, html
from dash.dependencies import Input, Output


app = dash.Dash(__name__)
np.random.seed(1)

x = np.random.rand(100)
y = np.random.rand(100)

f = go.FigureWidget([go.Scatter(x=x, y=y, mode='markers')])

scatter = f.data[0]
colors = ['#a3a7e4'] * 100
scatter.marker.color = colors
scatter.marker.size = [10] * 100
f.layout.hovermode = 'closest'


# create our callback function
def update_point(trace, points, selector):
    print('update called')
    c = list(scatter.marker.color)
    s = list(scatter.marker.size)
    for i in points.point_inds:
        c[i] = '#bae2be'
        s[i] = 20
        with f.batch_update():
            scatter.marker.color = c
            scatter.marker.size = s


scatter.on_click(update_point)

# st.plotly_chart(f)


app.layout = html.Div(
   [
      dcc.Graph(
         id="graph_interaction",
         figure=f,
      ),
      html.Pre(id='data')
   ]
)

@app.callback(Output('data', 'children'), Input('graph_interaction', 'clickData'))
def open_url(clickData):
    if clickData:
        print(clickData)
        webbrowser.open(clickData["points"][0]["customdata"][0])
    else:
        raise PreventUpdate
      # return json.dumps(clickData, indent=2)
      
if __name__ == '__main__':
    app.run_server(debug=True)