import numpy as np
import pandas as pd
import networkx as nx
import pylab as plt
from matplotlib_venn import venn2, venn2_circles

comp = pd.read_csv('dataset/comp_info.tsv',index_col=0,sep='\t')
ingr_comp = pd.read_csv('dataset/ingr_comp.tsv',sep='\t')
ingr = pd.read_csv('dataset/ingr_info.tsv',index_col=0,sep='\t')

share = pd.read_csv('dataset/srep00196-s2.csv',skiprows=4,header=None)
share.columns = ['ingr1','ingr2','shared']

share_category = pd.merge(share,ingr, left_on='ingr1', right_on='ingredient name').drop('ingredient name',axis=1)

recipe = pd.read_csv('dataset/srep00196-s3.csv',skiprows=3,sep='\t')
recipe.columns=['recipes']

recipe['ingredients'] = recipe['recipes'].apply(lambda x: x.split(',')[1:])
all_ingredients = set()
recipe.ingredients.map(lambda x: [all_ingredients.add(i) for i in x])
len(all_ingredients) 

share_subset = share_category[share_category['ingr1'].isin(all_ingredients)]
share_subset = share_subset[share_subset['ingr2'].isin(all_ingredients)]
share_max = share.loc[share['shared'].idxmax()]
share_min = share.loc[share['shared'].idxmin()]

G = nx.Graph()
s = (
    2,  
    3,  
    1,  
)

v = venn2(subsets=s, set_labels=('A', 'B'))

v.get_label_by_id('10').set_text(share_max['ingr1'])
v.get_label_by_id('01').set_text(share_max['ingr2'])
v.get_label_by_id('11').set_text(share_max['shared'])
plt.title("Many shared Compounds")
plt.figure(0)
s1 = (
    2,  
    3,  
    1,  
)

v = venn2(subsets=s1, set_labels=('A', 'B'))

v.get_label_by_id('10').set_text(share_min['ingr1'])
v.get_label_by_id('01').set_text(share_min['ingr2'])
v.get_label_by_id('11').set_text(share_min['shared'])
nx.draw(G)
plt.title("Few shared Compounds")
plt.figure(1)
plt.show()
