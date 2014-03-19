__author__ = 'maximk'

import urllib
import pickle
import os.path
import re

from Bio import Entrez, Medline
from geo import platform
from copy import deepcopy

def get_id_list():
    """
    Возвращает список id, удовлетворяющих запросу
    """
    pattern = '"age"[All Fields] AND "Homo sapiens"[Organism] AND (expression profiling by array[DataSet Type] ' \
              'OR expression profiling by high throughput sequencing[DataSet Type]) AND ("gse"[Filter] AND "Homo sapiens"[Organism] ' \
              'AND "attribute name tissue"[Filter] AND ("20"[n_samples] : "500"[n_samples]))'
    handle = Entrez.esearch(db='gds', retmax=1000, term=pattern)
    record = Entrez.read(handle)
    return record['IdList']

def get_tissue(summary):
    """
    Возвращает название ткани или клеток
    """
    tissues = ['brain', 'skin', 'kidney', 'liver', 'intestine', 'overies', 'breast', 'vaginal',
                'glands', 'urethra','neuron']
    cells = ['muscle', 'nervous', 'epithelial', 'connective']
    tiss_set = set()
    cell_set = set()
    for tissue in tissues:
        if tissue in summary:
            tiss_set.add(tissue)

    for cell in cells:
        if cell in summary:
            cell_set.add(cell)

    words = re.split('\W+', summary)
    for pos in range(len(words)):
        if ('tissue' in words[pos]):
            tiss_set.add(words[pos-1])
        if ('cell' in words[pos]):
            cell_set.add(words[pos-1])
        if ('cyte' in words[pos])or('blast' in words[pos]):
            cell_set.add(words[pos])
    return [tiss_set, cell_set]

def retrieve_record(id):
    """
    Получает запись по id
    """
    handle = Entrez.esummary(db='gds', id=id)
    return Entrez.read(handle)

def get_paper(pmids):
    """
    Возвращает название статьи и список авторов
    """
    papers = []
    handle = Entrez.efetch(db="pubmed", id=[str(id) for id in pmids], rettype="medline", retmode="text")
    records = Medline.parse(handle)
    for record in records:
        papers.append('%s, %s, %s' % (record.get("TI", "?"), record.get("AU", "?"), record.get("SO", "?")))
    return '\n'.join(papers)

def get_summary(id):
    """
    Возвращает Title, текст Summary и текст Overall design
    """
    url = 'http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE%s&targ=self&form=text&view=brief' % id
    geo_xml = urllib.request.urlopen(url).read().decode('utf-8').split(sep='\n')
    overall_design = ' '.join(line for line in geo_xml if '!Series_overall_design' in line)
    summary = ' '.join(line for line in geo_xml if '!Series_summary' in line)
    title = ' '.join(line for line in geo_xml if '!Series_title' in line)
    return ' '.join([title, summary, overall_design])

if os.path.isfile('/home/maximk/Work/geroscope/tissues/id_list_unprocess.pickle'):
    with open('/home/maximk/Work/geroscope/tissues/id_list_unprocess.pickle', 'rb') as f:
        id_list = pickle.load(f)
elif os.path.isfile('/home/maximk/Work/geroscope/tissues/id_list.pickle'):
    with open('/home/maximk/Work/geroscope/tissues/id_list.pickle', 'rb') as f:
        id_list = pickle.load(f)
else:
    id_list = get_id_list()
    with open('/home/maximk/Work/geroscope/tissues/id_list.pickle', 'wb') as f:
        pickle.dump(id_list, f)

id_list_copy = deepcopy(id_list)

for id in id_list:
    record = retrieve_record(id)
    paper = get_paper(record[0]['PubMedIds'])
    ts = get_tissue(get_summary(record[0]['GSE']))
    #  Title, Tissue, Cell, GSE, DataSet type, Samples, GEO Platform ID, Array type, Papers
    print('%s;%s;%s;GSE%s;%s;%s;%s;%s;%s'
          % (record[0]['title'], ', '.join(ts[0]),','.join(ts[1]), record[0]['GSE'], record[0]['gdsType'],
             record[0]['n_samples'], record[0]['GPL'], ', '.join(platform(record[0]['GPL'])), paper))
    id_list_copy.remove(id)
    with open('/home/maximk/Work/geroscope/tissues/id_list_unprocess.pickle', 'wb') as f:
        pickle.dump(id_list_copy, f)
