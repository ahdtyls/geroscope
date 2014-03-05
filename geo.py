__author__ = 'maximk'

from Bio import Entrez
import os
os.environ["http_proxy"] = "187.72.124.66:8080"

Entrez.email = 'kuleshov.max.v@gmail.com'

def retrieve_record(query):
    '''
    Возвращает выбранные параметры для всех записией по данному запросу
    '''
    handle = Entrez.esearch(db='gds', retmax=200, term='("bevacizumab"[All Fields] OR Bevacizumab[All Fields]) AND ("expression profiling by array"[DataSet Type] OR "expression profiling by high throughput sequencing"[DataSet Type]) AND "gse"[Filter]')

    record = Entrez.read(handle)
    for geo_id in record['IdList']:
            handle = Entrez.esummary(db="gds", id=geo_id)
            summary = Entrez.read(handle)
            print('GEO Series ID: %s\nName: %s\n%s samples\nGEO Platform ID: GPL%s' % (summary[0]['Accession'], summary[0]['title'], len(summary[0]['Samples']), summary[0]['GPL']))
            print()

    return None