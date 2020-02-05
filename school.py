import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
name_dict = {}
size_dict = {}


def create_nodes(doc, dept):

    for index, row in doc.iterrows():
        node = row['Ime'].title() + " " + row['Prezime'].title()

        if dept and dept != row['Odsek']:
            continue

        G.add_node(node)

        size_dict[node] = 1

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

        for author in split_authors:
            if author in name_dict:
                size_dict[name_dict.get(author)] += 1

        for i in range(0, len(split_authors) - 1):
            for j in range(i + 1, len(split_authors)):
                auth1 = split_authors[i]
                auth2 = split_authors[j]

                if auth1 in name_dict and auth2 in name_dict:
                    if G.has_edge(name_dict.get(auth1), name_dict.get(auth2)):
                        G[name_dict.get(auth1)][name_dict.get(auth2)]['weight'] += 0.2
                    else:
                        G.add_edge(name_dict.get(auth1), name_dict.get(auth2), weight = 0.5)


def create_graph(school, papers, color, dept = False):
    global G
    global name_dict
    global size_dict

    G = nx.Graph()
    name_dict = {}
    size_dict = {}

    create_nodes(school, dept)
    create_edges(papers)


    pos = nx.spring_layout(G, k = 1, iterations = 50, scale = 5)
    nx.draw_networkx_nodes(G, pos = pos, node_color = color, node_size = [v * 10 for v in size_dict.values()])

    edges = G.edges()
    weights = [G[u][v]['weight'] for u,v in edges]

    nx.draw_networkx_edges(G, pos=pos, edge_color='darkslategrey', width=weights)
    nx.draw_networkx_labels(G, pos = pos, font_size = 7,font_family = 'sans-serif')
    plt.show()

    return name_dict


def analysis():
    degree_centrality = sorted(nx.degree_centrality(G).items(), key = lambda x:x[1], reverse = True)
    betweenness_centrality = sorted(nx.betweenness_centrality(G).items(), key = lambda x: x[1], reverse = True)
    closeness_centrality = sorted(nx.closeness_centrality(G).items(), key = lambda x: x[1], reverse = True)
    clustering = [(k, v) for k, v in nx.clustering(G).items()]
    average_degree_connectivity = sorted( [ (k, v) for k, v in nx.average_degree_connectivity(G).items()])
    average_neighbor_degree = sorted(nx.average_neighbor_degree(G).items(), key = lambda x: x[1], reverse = True)

    create_excel(degree_centrality, 'Autor', 'Centralnost po stepenu', r'degree_centrality.xlsx', True)
    create_excel(betweenness_centrality, 'Autor', 'Relaciona Centralnost', r'betweenness_centrality.xlsx', True)
    create_excel(closeness_centrality, 'Autor', 'Centralnost po bliskosti', r'closeness_centrality.xlsx', True)
    create_excel(clustering, 'Autor', 'Faktor klasterizacije', r'clustering.xlsx', True)
    create_excel(average_degree_connectivity, 'Broj suseda', 'Procenat', r'average_degree_connectivity.xlsx', False)
    create_excel(average_neighbor_degree, 'Autor', 'Stepen suseda', r'average_neighbor_degree.xlsx', True)


def create_excel(data, first_col, second_col, file_name, flag):
    if flag:
        departments = nx.get_node_attributes(G, 'Katedre')
        sorted_departments = []

        for temp in data:
            sorted_departments.append(departments[temp[0]])

    df = pd.DataFrame(data, columns=[first_col, second_col])
    if flag:
        df['Katedra'] = sorted_departments
    df.to_excel('deptartments_quantitative/' + file_name, index=None, header=True)

