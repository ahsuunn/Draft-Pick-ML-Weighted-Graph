import networkx as nx
import os
import json
import matplotlib.pyplot as plt


'''INITIALIZE GRAPH'''
counterGraph = nx.DiGraph()
compatibilityGraph = nx.DiGraph()

heroes = []
counterEdges = []
compatibilityEdges = []

with open("HeroData.json", "r") as f1, open("heroDictionary.json", "r") as f2:
    hero_data = json.load(f1)
    hero_dictionary = json.load(f2)

for idx in range(127):
    heroName = hero_data[idx]['heroName']
    baseRelation = hero_data[idx]['relationData']
    heroes.append(heroName)
    
    for i in range(5):
        counterId = baseRelation['counter'][i]['hero_id']
        counterWeight = baseRelation['counter'][i]['value']
        reverseRelationWeight = "-" + counterWeight # Menambah minus untuk relasi hero sebaliknya
        subheroNameCounter = hero_dictionary[counterId] 
        counterEdges.append((heroName, subheroNameCounter, counterWeight))
        if not counterGraph.has_edge(subheroNameCounter, heroName):
            counterEdges.append((subheroNameCounter, heroName, reverseRelationWeight))

        counteredId = baseRelation['countered'][i]['hero_id']
        counteredWeight = baseRelation['countered'][i]['value']
        reverseRelationWeight = counteredWeight[1:] # Menghapus minus untuk relasi hero sebaliknya
        subheroNameCountered = hero_dictionary[counteredId]
        counterEdges.append((heroName, subheroNameCountered, counteredWeight))
        if not counterGraph.has_edge(subheroNameCountered, heroName):
            counterEdges.append((subheroNameCountered, heroName, reverseRelationWeight))
        
        compatibleId = baseRelation['compatible'][i]['hero_id']
        compatibleWeight = baseRelation['compatible'][i]['value']
        subheroNameCompatible = hero_dictionary[compatibleId]
        compatibilityEdges.append((heroName, subheroNameCompatible, compatibleWeight))
        if not compatibilityGraph.has_edge(subheroNameCompatible, heroName):
            compatibilityEdges.append((subheroNameCompatible, heroName, compatibleWeight))
        
        incompatibleId = baseRelation['incompatible'][i]['hero_id']
        incompatibleWeight = baseRelation['incompatible'][i]['value']
        subheroNameIncompatible = hero_dictionary[incompatibleId]
        compatibilityEdges.append((heroName, subheroNameIncompatible, incompatibleWeight))
        if not compatibilityGraph.has_edge(subheroNameIncompatible, heroName):
            compatibilityEdges.append((subheroNameIncompatible, heroName, incompatibleWeight))

counterGraph.add_nodes_from(heroes)
counterGraph.add_weighted_edges_from(counterEdges)

compatibilityGraph.add_nodes_from(heroes)
compatibilityGraph.add_weighted_edges_from(compatibilityEdges)

def visualize_graph(graph, title, node_color="lightblue", edge_color="gray"):
    plt.figure(figsize=(12, 12))
    pos = nx.circular_layout(graph) 

    nx.draw_networkx_nodes(graph, pos, node_color=node_color, node_size=100)
    nx.draw_networkx_edges(graph, pos, edge_color=edge_color, arrowstyle='-|>', arrowsize=1)
    nx.draw_networkx_labels(graph, pos, font_size=5, font_color="black")

    # Draw edge labels (weights)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=5)

    # Set title
    plt.title(title, fontsize=10)
    plt.axis("off")
    plt.show()

# Visualize the Counter Graph
visualize_graph(counterGraph, "Counter Graph", node_color="salmon", edge_color="red")

# Visualize the Compatibility Graph
visualize_graph(compatibilityGraph, "Compatibility Graph", node_color="lightgreen", edge_color="green")