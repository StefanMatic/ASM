import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

authors = pd.ExcelFile('authors.xlsx')
papers = pd.read_excel('papers.xlsx')

matf = pd.read_excel(authors, 'matematicki fakultet')
etf = pd.read_excel(authors, 'elektrotehnicki fakultet')
fon = pd.read_excel(authors, 'fakultet organizacionih nauka')

G = nx.Graph()
dict = {}

def create_nodes(doc):
    for index, row in doc.iterrows():
        node = row['Ime'] + " " + row['Prezime']

        G.add_node(node);

        key = row['Prezime'] + ', ' + row['Ime'][0] + '.'
        dict.update({key: node});

        if not row['Srednje ime'] or row['Srednje ime'] == 'N/A':
            # ako postoji srednje ime
            key = row['Prezime'] + ', ' + row['Ime'][0] + '.' + row['Srednje ime'][0] + '.'
            dict.update({key: node})

def create_edges(doc):
    for index, row in doc.drop_duplicates('Naslov').iterrows():
        split_authors = row['Autori'].split(' and ')

        for i in range(0, len(split_authors) - 1):
            for j in range(i + 1, len(split_authors)):
                auth1 = split_authors[i]
                auth2 = split_authors[j]
                if auth1 in dict and auth2 in dict:
                    G.add_edge(dict.get(auth1), dict.get(auth2))




create_nodes(matf)
create_nodes(etf)
create_nodes(fon)
create_edges(papers)

pos = nx.spring_layout(G, k=1, iterations=20)
nx.draw(G, pos)
# nx.draw_networkx_labels(G, nx.spring_layout(G))
# nx.draw_networkx_edges(G, nx.spring_layout(G))
plt.show()
plt.savefig("graph.png")