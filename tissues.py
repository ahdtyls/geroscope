__author__ = 'maximk'

#  Tissue, GSE, samples, array type, paper, dataset type

import urllib
import pickle
import re

from Bio import  Entrez
from geo import cel, platform

def get_id_list():
    """
    Возвращает список id, удовлетворяющих запросу
    """
    pattern = '"age"[All Fields] AND "Homo sapiens"[Organism] AND (expression profiling by array[DataSet Type] ' \
              'OR expression profiling by high throughput sequencing[DataSet Type]) AND ("gse"[Filter] AND "Homo sapiens"[Organism] ' \
              'AND "attribute name tissue"[Filter] AND ("20"[n_samples] : "500"[n_samples]))'
    handle = Entrez.esearch(db='gds', retmax=600, term=pattern)
    record = Entrez.read(handle)
    return record['IdList']

def get_tissue(summary):
    """
    Возвращает название ткани или клеток
    """
    tissues = ['brain', 'skin', 'kidney', 'liver', 'intestine', 'overies', 'breast', 'vaginal',
                'glands', 'urethra','neuron', 'muscle', 'nervous', 'epithelial', 'connective']
    tiss_set = set()
    for tissue in tissues:
        if tissue in summary:
            tiss_set.add(tissue)

    words = re.split('\W+', summary)
    for pos in range(len(words)):
        if ('cell' in words[pos])or('tissue' in words[pos]):
            tiss_set.add(words[pos-1])
        if ('cyte' in words[pos])or('blast' in words[pos]):
            tiss_set.add(words[pos])
    return tiss_set

def retrieve_record(id):
    """
    Получает запись по id
    """
    handle = Entrez.esummary(db='gds', id=id)
    return Entrez.read(handle)

def get_paper(pmid):
    """
    Возвращает название статьи и список авторов
    """
    return None

def get_summary(id):
    """
    Возвращает текст Summary и Overall design
    """
    url = 'http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE%s&targ=self&form=text&view=brief' % id
    geo_xml = urllib.request.urlopen(url).read().decode('utf-8').split(sep='\n')
    overall_design = ' '.join(line for line in geo_xml if '!Series_overall_design' in line)
    summary = ' '.join(line for line in geo_xml if '!Series_summary' in line)
    return ' '.join([summary, overall_design])

id_list = get_id_list()
for id in id_list:
    record = retrieve_record(id)
    print(get_tissue(get_summary(record[0]['GSE'])))
