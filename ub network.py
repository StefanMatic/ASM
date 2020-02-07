import pandas as pd
import departments_quantitative
import departments_qualitative
import magazines
import school
import util

authors = pd.ExcelFile('authors.xlsx')
papers = pd.read_excel('papers.xlsx')

etf = pd.read_excel(authors, 'elektrotehnicki fakultet')
matf = pd.read_excel(authors, 'matematicki fakultet')
fon = pd.read_excel(authors, 'fakultet organizacionih nauka')


dept_G, name_dict = departments_quantitative.create_graph([(matf, 'matf'), (etf, 'etf'), (fon, 'fon')], papers)
dept_qual_G = departments_qualitative.create_graph([(matf, 'matf'), (etf, 'etf'), (fon, 'fon')], papers)

mag_G = magazines.create_graph(papers, name_dict)

etf_G = school.create_graph('etf', etf, papers, 'crimson')
matf_G = school.create_graph('matf', matf, papers, 'skyblue')
fon_G = school.create_graph('fon', fon, papers, 'teal', flag = True)
fon_is_G = school.create_graph('fon is', fon, papers, 'teal', 'Katedra za informacione sisteme')
fon_si_G = school.create_graph('fon si', fon, papers, 'lightseagreen', 'Katedra za softversko inzenjerstvo')
fon_it_G = school.create_graph('fon it', fon, papers, 'cadetblue', 'Katedra za informacione tehnologije')

util.analysis(dept_G, 'dept', True)
util.analysis(dept_qual_G, 'dept_qual', True)
util.analysis(mag_G, 'mag', False)
util.analysis(etf_G, 'etf', False)
util.analysis(matf_G, 'matf', False)
util.analysis(fon_G, 'fon', True)
util.analysis(fon_is_G, 'fon_is', False)
util.analysis(fon_si_G, 'fon_si', False)
util.analysis(fon_it_G, ' fon_it', False)
