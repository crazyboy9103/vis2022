import random
from plot_utils.bubble_maker import BubbleMaker

'''
#cluster data 1개 format
: {
  'score': fit-score(1~9, int),
  'cid': cluster-id(str),
  'c_members': list of notice ids of cluster members in cluster,
  'number' : cluster size
}
'''

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
cid =0
cluster_data = []
for i in range(50):
  number = random.randrange(1,250)
  score = random.randrange(1,8)
  cluster_data.append(generate_cluster(number, score))

makers = BubbleMaker()
bubbles = makers.gen_bubble(cluster_data)
# pp(bubbles)
fig = makers.plot_bubbles(bubbles)
fig.show()