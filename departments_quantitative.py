import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import community
import matplotlib as mpl
import util

G = nx.Graph()
name_dict = {}
size_dict = {}
node_attributes = {}
networks = ['etf', 'matf', 'fon-is', 'fon-si', 'fon-it']
colors = ['crimson', 'skyblue', 'teal', 'lightseagreen', 'cadetblue']
color_map = dict(zip(networks, colors))

networks_list = []
nodes = []

def create_nodes(doc, name):

    for index, row in doc.iterrows():
        node = row['Ime'].title() + " " + row['Prezime'].title()
        G.add_node(node)

        nodes.append(node)
        if name == 'fon':
            if row['Odsek'] == 'Katedra za informacione sisteme':
                networks_list.append('fon-is')
                node_attributes[node] = 'FON_IS'
            elif row['Odsek'] == 'Katedra za softversko inzenjerstvo':
                networks_list.append('fon-si')
                node_attributes[node] = 'FON_SI'
            else:
                networks_list.append('fon-it')
                node_attributes[node] = 'FON_IT'
        elif name == 'etf':
            networks_list.append(name)
            node_attributes[node] = 'ETF_RTI'
        else:
            networks_list.append(name)
            node_attributes[node] = 'MATF_RTI'

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

def create_graph(tuples, papers):
    for t in tuples:
        create_nodes(t[0], t[1])
    create_edges(papers)

    isolates = list(nx.isolates(G))
    G.remove_nodes_from(isolates)

    cnt = 0
    for node in nodes:
        if nodes[cnt] in isolates:
            del nodes[cnt]
            del networks_list[cnt]
        else:
            cnt += 1

    node_network_map = dict(zip(nodes, networks_list))

    nodes_by_color = {val: [node for node in G if color_map[node_network_map[node]] == val] for val in colors}

    pos = nx.spring_layout(G, k = 1, iterations = 50, scale = 5)

    angs = np.linspace(0, 2*np.pi, 1+len(colors))
    repos = []
    rad = 10

    for ea in angs:
        if ea > 0:
            repos.append(np.array([rad*np.cos(ea), rad*np.sin(ea)]))
    for ea in pos.keys():
        posx = 0
        if ea in nodes_by_color['crimson']:
            posx = 0
        elif ea in nodes_by_color['skyblue']:
            posx = 1
        elif ea in nodes_by_color['teal']:
            posx = 2
        elif ea in nodes_by_color['lightseagreen']:
            posx = 3
        elif ea in nodes_by_color['cadetblue']:
            posx = 4
        else:
            pass
        pos[ea] += repos[posx]


    for color, node_names in nodes_by_color.items():
        sizes = {}
        for name in node_names:
            sizes[name] = size_dict.get(name)
        nx.draw_networkx_nodes(G, pos = pos, nodelist = node_names, node_color = color, node_size = [v * 7 for v in sizes.values()])

    edges = G.edges()
    weights = [G[u][v]['weight'] for u,v in edges]

    nx.set_node_attributes(G, node_attributes, name = 'Katedre')

    nx.draw_networkx_edges(G, pos = pos, edge_color = 'darkslategrey', width = weights)
    # nx.draw_networkx_labels(G, pos = pos, font_size = 7,font_family = 'sans-serif')
    plt.show()

    part = community.best_partition(G)
    mod = community.modularity(part, G)

    print("dept modularity = " + str(mod))

    edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())
    values = [part.get(node) for node in G.nodes()]
    cmap = mpl.cm.Greys(np.linspace(0, 1, 20))
    cmap = mpl.colors.ListedColormap(cmap[10:, :-1])
    nx.draw_spring(G, cmap = plt.get_cmap('RdYlBu'), node_color = values, edgelist=edges, edge_color=weights, width = weights, edge_cmap=cmap, node_size = [v * 7 for v in sizes.values()], with_labels = False)
    plt.show()
    nx.draw_spring(G, cmap = plt.get_cmap('RdYlBu'), node_color = values, edgelist=edges, edge_color=weights, width = weights, edge_cmap=cmap, node_size = [v * 7 for v in sizes.values()], with_labels = True, font_size = 7,font_family = 'sans-serif')
    plt.show()

    sizes = []
    for n in G.nodes():
        sizes.append(size_dict[n])

    size_list = list(zip(G.nodes(), sizes))
    util.create_excel(G, sorted(size_list, key=lambda x: x[1], reverse = True), "Ime", "Velicina", "dept_node_size.xlsx", True)

    edges = G.edges()
    util.create_excel(G, sorted(list(zip(edges, weights)), key = lambda x: x[1], reverse = True), "Veza", "Tezina", "dept_edge_weight.xlsx", False)

    return G, name_dict

