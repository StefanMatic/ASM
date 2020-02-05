import pandas as pd
import departments_quantitative

authors = pd.ExcelFile('authors.xlsx')
papers = pd.read_excel('papers.xlsx')

matf = pd.read_excel(authors, 'matematicki fakultet')
etf = pd.read_excel(authors, 'elektrotehnicki fakultet')
fon = pd.read_excel(authors, 'fakultet organizacionih nauka')

departments_quantitative.create_graph([(matf, 'matf'), (etf, 'etf'), (fon, 'fon')], papers)
departments_quantitative.analysis()