import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

authors = pd.ExcelFile('authors.xlsx')
papers = pd.read_excel('papers.xlsx')

matf = pd.read_excel(authors, 'matematicki fakultet')
etf = pd.read_excel(authors, 'elektrotehnicki fakultet')
fon = pd.read_excel(authors, 'fakultet organizacionih nauka')

G = nx.Graph()
name_dict = {}
networks = ['etf', 'matf', 'fon']
colors = ['red', 'blue', 'yellow']
color_map = dict(zip(networks, colors))

networks_list = []
nodes = []

def create_nodes(doc, name):

    for index, row in doc.iterrows():
        node = row['Ime'].title() + " " + row['Prezime'].title()
        # G.add_node(node)

        nodes.append(node)
        networks_list.append(name)

        key1 = row['Prezime'].title() + ', ' + row['Ime'][0].title() + '.'
        name_dict[key1] = node

        key2 = row['Prezime'].title() + ', ' + row['Ime'].title()
        name_dict[key2] = node

        if row['Srednje ime'] and not row['Srednje ime'] == 'N/A':
            key3 = row['Prezime'].title() + ', ' + row['Ime'][0].title() + '.' + str(row['Srednje ime'])[0].title() + '.'
            name_dict[key3] = node

def create_edges(doc):
    cnt = 0
    for index, row in doc.drop_duplicates('Naslov').iterrows():
        split_authors = row['Autori'].split(' and ')

        for i in range(0, len(split_authors) - 1):
            for j in range(i + 1, len(split_authors)):
                auth1 = split_authors[i]
                auth2 = split_authors[j]

                if auth1 in name_dict and auth2 in name_dict:
                    cnt += 1
                    G.add_edge(name_dict.get(auth1), name_dict.get(auth2))

    print(cnt)




create_nodes(matf, 'matf')
create_nodes(etf, 'etf')
create_nodes(fon, 'fon')
create_edges(papers)

node_network_map = dict(zip(nodes, networks_list))


nodes_by_color = {val: [node for node in G if color_map[node_network_map[node]] == val] for val in colors}

# pos = nx.spring_layout(G)

# OVDE POCINJE KOMENTAR

# pos = nx.circular_layout(G)
pos = nx.spring_layout(G, k=1, iterations=20)

angs = np.linspace(0, 2*np.pi, 1+len(colors))
repos = []
rad = 3.5

for ea in angs:
    if ea > 0:
        #print(rad*np.cos(ea), rad*np.sin(ea))  # location of each cluster
        repos.append(np.array([rad*np.cos(ea), rad*np.sin(ea)]))
for ea in pos.keys():
    #color = 'black'
    posx = 0
    if ea in nodes_by_color['red']:
        #color = 'red'
        posx = 0
    elif ea in nodes_by_color['blue']:
        #color = 'blue'
        posx = 1
    elif ea in nodes_by_color['yellow']:
        #color = 'yellow'
        posx = 2
    else:
        pass
    #print(ea, pos[ea], pos[ea]+repos[posx], color, posx)
    pos[ea] += repos[posx]

# KRAJ

# edges = G.edges()

# weights = [abs(G[u][v]['weight']) for u, v in edges]
# weights_n = [5*float(i)/max(weights) for i in weights]

plt.figure()
for color, node_names in nodes_by_color.items():
    nx.draw_networkx_nodes(G, pos=pos, nodelist=node_names, node_color=color)

nx.draw_networkx_edges(G, pos=pos)
nx.draw_networkx_labels(G, pos=pos)
plt.show()

# pos = nx.spring_layout(G, k=1, iterations=20)

# df = pd.DataFrame(index=G.nodes(), columns=G.nodes())
# for row, data in nx.shortest_path_length(G):
#     for col, dist in data.items():
#         df.loc[row,col] = dist
#
# df = df.fillna(df.max().max())
#
#
# nx.draw_kamada_kawai(G, dist=df.to_dict())


# nx.draw(G, pos)
# nx.draw_networkx_labels(G, nx.spring_layout(G))
# nx.draw_networkx_edges(G, nx.spring_layout(G))
# plt.show()
# plt.savefig("graph.png")