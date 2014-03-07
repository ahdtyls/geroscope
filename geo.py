__author__ = 'maximk'

from Bio import Entrez
import os
from ftplib import FTP

Entrez.email = 'kuleshov.max.v@gmail.com'

def cel(ftp_adress):
    """
    Проверяет наличие CEL-файлов
    """
    ftp = FTP(ftp_adress)
    ftp.login()
    files_list = ftp.nlst()
    return None

def platform(gpl):
    """
    Возвращает название платформы
    """
    handle = Entrez.esummary(db="gds", id=''.join(['10000', str(gpl)]))
    summary = Entrez.read(handle)
    return summary[0]['title']

def retrieve_record(query):
    """
    Возвращает выбранные параметры для всех записией по данному запросу
    """
    handle = Entrez.esearch(db='gds', retmax=200, term='("bevacizumab"[All Fields] OR Bevacizumab[All Fields]) AND ("expression profiling by array"[DataSet Type] OR "expression profiling by high throughput sequencing"[DataSet Type]) AND "gse"[Filter]')

    record = Entrez.read(handle)
    for geo_id in record['IdList']:
            handle = Entrez.esummary(db='gds', id=geo_id)
            summary = Entrez.read(handle)
            #cel_presence = cel(summary[0]['FTPLink'])

            print('GEO Series ID: %s\nName: %s\nSamples: %s\nGEO Platform ID: GPL%s\nPlatform: %s' % (summary[0]['Accession'], summary[0]['title'], len(summary[0]['Samples']), summary[0]['GPL'], platform(summary[0]['GPL'])))
            print()

    return None

retrieve_record('')
#cel('ftp.debian.org')