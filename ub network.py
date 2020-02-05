import pandas as pd
import departments_quantitative
import magazines
import school

authors = pd.ExcelFile('authors.xlsx')
papers = pd.read_excel('papers.xlsx')

etf = pd.read_excel(authors, 'elektrotehnicki fakultet')
matf = pd.read_excel(authors, 'matematicki fakultet')
fon = pd.read_excel(authors, 'fakultet organizacionih nauka')

name_dict = departments_quantitative.create_graph([(matf, 'matf'), (etf, 'etf'), (fon, 'fon')], papers)
departments_quantitative.analysis()

magazines.create_graph(papers, name_dict)

school.create_graph(etf, papers, 'crimson')
school.create_graph(matf, papers, 'skyblue')
school.create_graph(fon, papers, 'teal')
school.create_graph(fon, papers, 'teal', 'Katedra za informacione sisteme')
school.create_graph(fon, papers, 'lightseagreen', 'Katedra za softversko inzenjerstvo')
school.create_graph(fon, papers, 'cadetblue', 'Katedra za informacione tehnologije')