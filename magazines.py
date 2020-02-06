import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

magazines = []
magazine_authors = {}
sizes = {}
ub_authors = {}

G = nx.Graph()
def create_nodes(doc):
    for index, row in doc.drop_duplicates('Naslov').iterrows():
        if row['Tip rada'] == 'Article':
            if row['Ime dokumenta'] in magazines:
                sizes[row['Ime dokumenta']] += 1
            else:
                G.add_node(row['Ime dokumenta'])
                magazines.append(row['Ime dokumenta'])
                sizes[row['Ime dokumenta']] = 1


def create_edges(doc):
    for magazine in magazines:
        magazine_authors.setdefault(magazine, set())

    for index, row in doc.drop_duplicates('Naslov').iterrows():
        if row['Tip rada'] == 'Article':
            split_authors = row['Autori'].split(' and ')

            for author in split_authors:
                if author in ub_authors and row['Ime dokumenta'] in magazine_authors:
                    magazine_authors[row['Ime dokumenta']].add(author)


    for i in range(0, len(magazines) - 1):
        for j in range(i + 1, len(magazines)):

            for author in magazine_authors[magazines[i]]:
                if author in magazine_authors[magazines[j]]:
                    if G.has_edge(magazines[i], magazines[j]):
                        G[magazines[i]][magazines[j]]['weight'] += 0.1
                    else:
                        G.add_edge(magazines[i], magazines[j], weight=0.1)


def create_graph(papers, name_dict):
    global ub_authors
    ub_authors = name_dict

    create_nodes(papers)
    create_edges(papers)

    pos = nx.spring_layout(G, k = 1, iterations = 50, scale = 5)

    edges = G.edges()
    weights = [G[u][v]['weight'] for u,v in edges]


    nx.draw_networkx_nodes(G, pos = pos, node_color = 'peru', node_size = [v * 10 for v in sizes.values()])
    nx.draw_networkx_edges(G, pos=pos, edge_color='darkslategrey', width=weights)
    #nx.draw_networkx_labels(G, pos = pos, font_size = 7,font_family = 'sans-serif')
    plt.show()

    return G