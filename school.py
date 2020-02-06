import networkx as nx
import matplotlib.pyplot as plt
import community
import matplotlib as mpl
import numpy as np

G = nx.Graph()
name_dict = {}
size_dict = {}
node_attributes = {}

def create_nodes(doc, dept, flag):

    for index, row in doc.iterrows():
        node = row['Ime'].title() + " " + row['Prezime'].title()

        if dept and dept != row['Odsek']:
            continue

        G.add_node(node)

        size_dict[node] = 1

        if flag:
            if row['Odsek'] == 'Katedra za informacione sisteme':
                node_attributes[node] = 'FON_IS'
            elif row['Odsek'] == 'Katedra za softversko inzenjerstvo':
                node_attributes[node] = 'FON_SI'
            else:
                node_attributes[node] = 'FON_IT'

        key1 = row['Prezime'].title() + ', ' + row['Ime'][0].title() + '.'
        name_dict[key1] = node

        key2 = row['Prezime'].title() + ', ' + row['Ime'].title()
        name_dict[key2] = node

        if row['Srednje ime'] and not row['Srednje ime'] == 'N/A':
            key3 = row['Prezime'].title() + ', ' + row['Ime'][0].title() + '.' + str(row['Srednje ime'])[0].title() + '.'
            name_dict[key3] = node


def create_edges(doc):
    for index, row in doc.drop_duplicates('Naslov').iterrows():
        split_authors = row['Autori'].split(' and ')

        # for author in split_authors:
        #     if author in name_dict:
        #         size_dict[name_dict.get(author)] += 1

        authors = set()

        for i in range(0, len(split_authors) - 1):
            for j in range(i + 1, len(split_authors)):
                auth1 = split_authors[i]
                auth2 = split_authors[j]

                if auth1 in name_dict and auth2 in name_dict:
                    authors.add(auth1)
                    authors.add(auth2)
                    if G.has_edge(name_dict.get(auth1), name_dict.get(auth2)):
                        G[name_dict.get(auth1)][name_dict.get(auth2)]['weight'] += 0.1
                    else:
                        G.add_edge(name_dict.get(auth1), name_dict.get(auth2), weight = 0.1)

        for a in authors:
            size_dict[name_dict.get(a)] += 1

def create_graph(school, papers, color, dept = False, flag = False):
    global G
    global name_dict
    global size_dict

    G = nx.Graph()
    name_dict = {}
    size_dict = {}

    create_nodes(school, dept, flag)
    create_edges(papers)

    isolates = list(nx.isolates(G))
    G.remove_nodes_from(isolates)

    pos = nx.spring_layout(G, k = 1, iterations = 50, scale = 5)
    nx.draw_networkx_nodes(G, pos = pos, node_color = color, node_size = [v * 10 for v in size_dict.values()])

    edges = G.edges()
    weights = [G[u][v]['weight'] for u,v in edges]

    if node_attributes:
        nx.set_node_attributes(G, node_attributes, name='Katedre')

    nx.draw_networkx_edges(G, pos=pos, edge_color='darkslategrey', width=weights)
    nx.draw_networkx_labels(G, pos = pos, font_size = 7,font_family = 'sans-serif')
    plt.show()

    return G

