import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

comp = pd.read_csv('dataset/comp_info.tsv',index_col=0,sep='\t')
ingr_comp = pd.read_csv('dataset/ingr_comp.tsv',sep='\t')
ingr = pd.read_csv('dataset/ingr_info.tsv',index_col=0,sep='\t')
ingr_share = pd.read_csv('dataset/srep00196-s2.csv',skiprows=4,header=None)
ingr_share.columns = ['ingr1','ingr2','shared']
ingr_category = pd.merge(ingr_share,ingr, left_on='ingr1', right_on='ingredient name').drop('ingredient name',axis=1)
#print (df_category)
recipe = pd.read_csv('dataset/srep00196-s3.csv',skiprows=3,sep='\t')
recipe.columns=['recipes']

recipe['ingredients'] = recipe['recipes'].apply(lambda x: x.split(',')[1:])
all_ingredients = set()
recipe.ingredients.map(lambda x: [all_ingredients.add(i) for i in x])
len(all_ingredients)
ingr_subset = ingr_category[ingr_category['ingr1'].isin(all_ingredients)]
ingr_subset = ingr_subset[ingr_subset['ingr2'].isin(all_ingredients)]
#print(ingr_subset)
G1 = nx.Graph()
weights ={}
for i in range(ingr_subset.shape[0]):
    G1.add_edge(ingr_subset.iloc[i,0],ingr_subset.iloc[i,1])
    weights[ingr_subset.iloc[i,0],ingr_subset.iloc[i,1]] = ingr_subset.iloc[i,2]
    weights[ingr_subset.iloc[i,1],ingr_subset.iloc[i,0]] = ingr_subset.iloc[i,2]

#extract backbone of graph, using disparity filter
def extract_backbone(G, weights, alpha):
    keep_graph = nx.Graph()
    for n in G:
        k_n = len( G[n] )
        if k_n > 1:
            sum_w = sum( weights[n,nj] for nj in G[n] )
            for nj in G[n]:
                pij = 1.0*weights[n,nj]/sum_w
                if (1-pij)**(k_n-1) < alpha: # edge is significant
                    keep_graph.add_edge( n,nj )
    return keep_graph

alpha = 0.04
G1_backbone = extract_backbone(G1, weights, alpha)

#make weights into a list and include both directions
weights_subset = []
for (u,v) in G1_backbone.edges():
    weights_subset.append((u,v,weights[u,v]))
    weights_subset.append((v,u,weights[u,v]))

df_weights = pd.DataFrame(data=weights_subset)
print(df_weights)
df_backbone = pd.merge(df_weights,ingr, left_on=0, right_on='ingredient name').drop('ingredient name',axis=1)

#get prevalance of each ingredient from recipes
recipe_count = recipe.copy()
for item in all_ingredients:
    recipe_count[item] = recipe_count['ingredients'].apply(lambda x:item in x)

recipe_count1 = recipe_count.drop(['recipes','ingredients'],axis=1)
#print(recipe_count1)
recipe_count2 = recipe_count1.sum(axis=0)
#print(recipe_count2)
total = recipe_count2.sum()
print(total)
recipe_count3 = recipe_count2/float(total)
recipe_count4= recipe_count3/recipe_count3.max()
recipe_count5= pd.DataFrame(recipe_count4)

recipe_count5['ingredient name'] = recipe_count5.index
recipe_count5.columns = ['prevalence','ingredient name']
print(recipe_count5)
ingr_count = pd.merge(ingr,recipe_count5,on='ingredient name')


df_backbone = pd.merge(df_weights,ingr_count, left_on=0, right_on='ingredient name').drop('ingredient name',axis=1)

df_backbone.to_csv('output/flavourgraph.csv',index=False)





