# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 21:29:03 2018

@author: ariahKlages-Mundt
"""
import networkx as nx

def create_nx_graph(nodes, A):
    G = nx.Graph()
    for i in range(len(nodes)):
        G.add_node(i, label=nodes[i])
    for i in range(len(nodes)):
        for j in range(i+1,len(nodes)):
            if A[i,j] > 0:
                G.add_edge(i,j,weight=A[i,j])
    return G

G = create_nx_graph(list(data.columns), bayes_net)
nx.write_gexf(G,'bayes_net{}.gexf'.format(n))

#spectral clustering
partitions_spec = spec_clust(G,6)
partitions_spec = code2clust(partitions_spec)

#create dictionary of node->cluster
spec_clusters = {}
spec_clusters_nodeid = {}
for ind in G.nodes():
    node = G.nodes()[ind]['label']
    for i in range(len(partitions_spec)):
        if ind in partitions_spec[i]:
            spec_clusters[node] = i
            spec_clusters_nodeid[ind] = i
            break

#create cluster lists by ticker
partitions_tick = []
for part in partitions_spec:
    tickers = [G.nodes()[ind]['label'] for ind in part]
    partitions_tick.append(tickers)
    

nx.set_node_attributes(G,spec_clusters_nodeid,'spec_cluster')
nx.write_gexf(G,'bayes_net{}.gexf'.format(n))