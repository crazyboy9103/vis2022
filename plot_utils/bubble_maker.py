from plotly.offline import plot
import plotly.graph_objects as go
import seaborn as sns
from pprint import pprint as pp
import circlify as circ
from collections import defaultdict
import math
import numpy as np

class BubbleMaker:
  palette = sns.color_palette("GnBu_d",10).as_hex()
  default_bubble_kwargs = {'type': 'circle', 'xref': 'x', 'yref': 'y' }
  padding = 0.01
  
  def __init__(self, palette=None):
    if palette:
      self.palette = palette
    self.fig = None
  
  def cluster_to_bubble(self, cluster):
    bubble_data = {
        'id': cluster['cid'],
        'datum': cluster['number'],
        'color': self.palette[cluster['score']],
    }
    return bubble_data

  def gen_bubble(self, cluster_data):
    '''
    :gnerate bubble data from cluster_data

    input:
    - cluster_data : list of clusters 
    - cluster: {'score':int, 'cid':string, 'number':int, 'c_members': list of nid(int)}

    output:
    - bubbles : list of bubble data for plotting (position info, radius, color, ...)
    '''

    #grouping as score
    children_info = defaultdict(list)
    for cluster in cluster_data:
      bubble = self.cluster_to_bubble(cluster)
      children_info[cluster['score']].append(bubble)

    #gen data as bubble format from cluster_data
    bubble_data = []
    for k, children in children_info.items():
      sc_bubble_data = {}
      sc_bubble_data['id'] = f'sc-{k}'
      sc_bubble_data['children'] = children
      sc_bubble_data['datum'] = sum([child['datum'] for child in children])
      bubble_data.append(sc_bubble_data)
      bubbles = circ.circlify(bubble_data, show_enclosure=False)
    return bubbles
  
  #draw packed bubble chart as plotly fig
  def plot_bubbles(self, bubbles, padding=None, fig=None):
    
    if fig:
      self.fig = fig
    elif not self.fig:
      self.fig = go.Figure()
      self.fig.update_layout(width=500, height=500)
    else:
      pass


    min_x = min([circle.x-circle.r for circle in bubbles])
    max_x = max([circle.x+circle.r for circle in bubbles])

    max_y = max([circle.y+circle.r for circle in bubbles])
    min_y = min([circle.y-circle.r for circle in bubbles])
    height = 2*max(abs(max_y),abs(min_y))
    width = max_x - min_x
    

    fig_width = self.fig.layout.width
    self.fig.update_layout(height=fig_width*height/width, margin=dict(l=10, r=10, b=10, t=10, pad=4))

    min_x = -min_x
    map_dict = dict()
    # padding
    if padding:
      self.padding = padding

    # print(bubbles)
    
    # points = [go.layout.Shape(x0=circle.x-(circle.r-self.padding)+min_x,
    #                       y0=circle.y-(circle.r-self.padding), 
    #                       x1=circle.x+(circle.r-self.padding)+min_x, 
    #                       y1=circle.y+(circle.r-self.padding), 
    #                       fillcolor=circle.ex['color'], 
    #                       line_color=circle.ex['color'],
    #                       **self.default_bubble_kwargs) for idx, circle in enumerate(bubbles) if circle.level==2]
    # self.fig.update_layout(shapes=points)
    
    i=0
    for _, circle in enumerate(bubbles):
      if circle.level == 2:
        self.fig.add_shape(type="circle",
          xref="x", yref="y",
          x0=circle.x-(circle.r-self.padding)+min_x,
          y0=circle.y-(circle.r-self.padding), 
          x1=circle.x+(circle.r-self.padding)+min_x, 
          y1=circle.y+(circle.r-self.padding), 
          opacity=1,
          fillcolor=circle.ex['color'], 
          line_color=circle.ex['color'])

        t = np.arange(0, 2 * np.pi, 0.01)
        x = (circle.r - self.padding) * np.cos(t) + circle.x+ min_x
        y = (circle.r - self.padding) * np.sin(t) + circle.y
        scatter = go.Scatter (
            x=x.tolist(),
            y=y.tolist(),
            fill='toself',
            mode='lines',
            name=f'{i}',
            text=f'{circle.ex["id"]}',
            opacity = 0,
        )
        map_dict[i] = circle.ex['id']
        i += 1
        self.fig.add_trace ( scatter)

    self.fig.update_xaxes(range=[0, width])
    self.fig.update_yaxes(range=[-height/2, height/2 ])

    self.fig.update_xaxes(visible=False)
    self.fig.update_yaxes(visible=False)

    self.fig.update_layout(showlegend=False)
    return self.fig, map_dict
