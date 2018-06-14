import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

comp = pd.read_csv('dataset/comp_infoa.tsv',sep='\t')
ingr_comp = pd.read_csv('dataset/ingr_compa.tsv',sep='\t')
ingr = pd.read_csv('dataset/ingr_infoa.tsv',sep='\t')
ingr.columns = ['id', 'name', 'category']
comp.columns = ['id', 'name', 'csa']
ingr_comp.columns = ['id1','id2']
compounds = pd.merge(ingr_comp,ingr,left_on='id1',right_on='id').drop('id',axis=1)
compound1 = pd.merge(compounds,comp,left_on='id2',right_on='id').drop('id',axis=1)
compound1.drop(compound1.columns[[0,1,3,5]],axis=1, inplace=True)
#print (compound1)
B = nx.Graph()
B.add_nodes_from(compound1['name_x'], bipartite=0)
B.add_nodes_from(compound1['name_y'], bipartite=1)
B.add_weighted_edges_from(
    [(row['name_x'], row['name_y'], 1) for idx, row in compound1.iterrows()], 
    weight='1')
pos = {node:[0, i] for i,node in enumerate(compound1['name_x'])}
pos.update({node:[1, i] for i,node in enumerate(compound1['name_y'])})
nx.draw(B, pos,node_size=50,width=1,with_labels=False)
for p in pos:  # raise text positions
    pos[p][1] += 0.55
nx.draw_networkx_labels(B, pos,font_size=10)
#plt.savefig('a.pdf')
plt.show()
