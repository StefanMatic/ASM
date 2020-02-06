import networkx as nx
import pandas as pd

G = nx.Graph()

def analysis(graph, prefix, flag):
    global G
    G = graph
    degree_centrality = sorted(nx.degree_centrality(G).items(), key = lambda x:x[1], reverse = True)
    betweenness_centrality = sorted(nx.betweenness_centrality(G).items(), key = lambda x: x[1], reverse = True)
    closeness_centrality = sorted(nx.closeness_centrality(G).items(), key = lambda x: x[1], reverse = True)
    eigenvector_centrality = sorted(nx.eigenvector_centrality_numpy(G).items(), key=lambda x: x[1], reverse=True)
    clustering = [(k, v) for k, v in nx.clustering(G).items()]
    average_degree_connectivity = sorted( [ (k, v) for k, v in nx.average_degree_connectivity(G).items()])
    average_neighbor_degree = sorted(nx.average_neighbor_degree(G).items(), key = lambda x: x[1], reverse = True)


    print(prefix + " connected components = " + str(nx.number_connected_components(G)))
    print(prefix + " degree assortativity coefficient = " + str(nx.degree_assortativity_coefficient(G)))
    print(prefix + " density = " + str(nx.density(G)))

    cnt = 0
    for c in nx.connected_components(G):
        subG = nx.subgraph(G, c)
        print(c)
        eccentricity = sorted(nx.eccentricity(subG).items(), key = lambda x: x[1], reverse = True)
        create_excel(eccentricity, 'Ime', 'Ekscentricnost', prefix + '_comp' + str(cnt) + '_eccentricity.xlsx', flag)
        print(prefix + " comp" + str(cnt) + " diameter = " + str(nx.diameter(subG)))
        print(prefix + " comp" + str(cnt) + " radius = " + str(nx.radius(subG)))
        print(prefix + " comp" + str(cnt) + " center = " + str(nx.center(subG)))
        print(prefix + " comp" + str(cnt) + " average shortest path length = " + str(nx.average_shortest_path_length(subG)))
        cnt += 1

    create_excel(degree_centrality, 'Ime', 'Centralnost po stepenu', prefix + '_degree_centrality.xlsx', flag)
    create_excel(betweenness_centrality, 'Ime', 'Relaciona Centralnost', prefix + '_betweenness_centrality.xlsx', flag)
    create_excel(closeness_centrality, 'Ime', 'Centralnost po bliskosti', prefix + '_closeness_centrality.xlsx', flag)
    create_excel(eigenvector_centrality, 'Ime', 'Eigenvector centralnost', prefix + '_eigenvector_centrality.xlsx', flag)
    create_excel(clustering, 'Ime', 'Faktor klasterizacije', prefix + '_clustering.xlsx', flag)
    create_excel(average_degree_connectivity, 'Stepen', 'Prosecan stepen suseda', prefix + '_average_degree_connectivity.xlsx', False)
    create_excel(average_neighbor_degree, 'Ime', 'Stepen suseda', prefix + '_average_neighbor_degree.xlsx', flag)


def create_excel(data, first_col, second_col, file_name, flag):
    if flag:
        departments = nx.get_node_attributes(G, 'Katedre')
        sorted_departments = []

        for temp in data:
            sorted_departments.append(departments[temp[0]])

    df = pd.DataFrame(data, columns=[first_col, second_col])
    if flag:
        df['Katedra'] = sorted_departments
    df.to_excel('excel/' + file_name, index=None, header=True)
