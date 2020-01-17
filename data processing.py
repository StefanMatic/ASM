import pandas as pd
import networkx as nx

authors = pd.ExcelFile('authors.xlsx')
papers = pd.read_excel('papers.xlsx')

matf = pd.read_excel(authors, 'matematicki fakultet')
etf = pd.read_excel(authors, 'elektrotehnicki fakultet')
fon = pd.read_excel(authors, 'fakultet organizacionih nauka')

G = nx.Graph();
dict = {}


for index, row in matf.iterrows():
    print(row['Ime'], row['Prezime'], row['Srednje ime'])
    #napravi cvor

    key = row['Prezime'] + ', ' + row['Ime'][0] + '.'
    #dodaj u dict

    if not row['Srednje ime'] or row['Srednje ime'] == 'N/A':
        #ako postoji srednje ime
        key = row['Prezime'] + ', ' + row['Ime'][0] + '.' + row['Srednje ime'][0] + '.'
        #dodaj u dict




