import networkx as nx
import matplotlib.pyplot as plt
import community
import matplotlib as mpl
import numpy as np
import util

conferences = []
conference_authors = {}
sizes = {}
ub_authors = {}

G = nx.Graph()
def create_nodes(doc):
    for index, row in doc.drop_duplicates('Naslov').iterrows():
        if row['Tip rada'] == 'Conference Paper':
            if row['Ime dokumenta'] in conferences:
                sizes[row['Ime dokumenta']] += 1
            else:
                G.add_node(row['Ime dokumenta'])
                conferences.append(row['Ime dokumenta'])
                sizes[row['Ime dokumenta']] = 1


def create_edges(doc):
    for conference in conferences:
        conference_authors.setdefault(conference, set())

    for index, row in doc.drop_duplicates('Naslov').iterrows():
        if row['Tip rada'] == 'Conference Paper':
            split_authors = row['Autori'].split(' and ')

            for author in split_authors:
                if author in ub_authors and row['Ime dokumenta'] in conference_authors:
                    conference_authors[row['Ime dokumenta']].add(author)


    for i in range(0, len(conferences) - 1):
        for j in range(i + 1, len(conferences)):

            for author in conference_authors[conferences[i]]:
                if author in conference_authors[conferences[j]]:
                    if G.has_edge(conferences[i], conferences[j]):
                        G[conferences[i]][conferences[j]]['weight'] += 0.1
                    else:
                        G.add_edge(conferences[i], conferences[j], weight=0.1)


def create_graph(papers, name_dict):
    global ub_authors
    ub_authors = name_dict

    create_nodes(papers)
    create_edges(papers)

    isolates = list(nx.isolates(G))
    G.remove_nodes_from(isolates)

    pos = nx.spring_layout(G, k = 1, iterations = 50, scale = 5)

    edges = G.edges()
    weights = [G[u][v]['weight'] for u,v in edges]

    colors = ['#668796', '#366f8a', '#1d6080', '#055378']
    node_colors = []
    for node in G.nodes:
        if sizes[node] < 3:
            node_colors.append(colors[0])
        elif sizes[node] < 5:
            node_colors.append(colors[1])
        elif sizes[node] < 10:
            node_colors.append(colors[2])
        else:
            node_colors.append(colors[3])

    nx.draw_networkx_nodes(G, pos = pos, node_color = node_colors, node_size = [v * 10 for v in sizes.values()])
    nx.draw_networkx_edges(G, pos = pos, edge_color = 'slategrey', width = weights)
    # nx.draw_networkx_labels(G, pos = pos, font_size = 7,font_family = 'sans-serif')
    plt.show()

    sizes_final = []
    for n in G.nodes():
        sizes_final.append(sizes[n])

    size_list = list(zip(G.nodes(), sizes_final))
    util.create_excel(G, sorted(size_list, key=lambda x: x[1], reverse=True), "Ime", "Velicina", "conf_node_size.xlsx",
                      False)

    edges = G.edges()
    util.create_excel(G, sorted(list(zip(edges, weights)), key=lambda x: x[1], reverse=True), "Veza", "Tezina",
                      "conf_edge_weight.xlsx", False)

    return G