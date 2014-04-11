__author__ = 'maximk'

import urllib
import pickle
import os.path
import re
import time
from functools import wraps
from Bio import Entrez, Medline
from copy import deepcopy

from geo import platform


def retry(exceptiontocheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param exceptiontocheck: the exception to check. may be a tuple of exceptions to check
    :type exceptiontocheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    # noinspection PyArgumentList
                    return f(*args, **kwargs)
                except exceptiontocheck as e:
                    msg = '%s, Retrying in %d seconds...' % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            # noinspection PyArgumentList
            return f(*args, **kwargs)
        return f_retry  # true decorator
    return deco_retry


@retry(urllib.error.URLError)
def get_id_list():
    """

    :rtype: None
    Возвращает список id, удовлетворяющих запросу
    """
    pattern = '"age"[All Fields] AND "Homo sapiens"[Organism] AND (expression profiling by array[DataSet Type] ' \
              'OR expression profiling by high throughput sequencing[DataSet Type]) AND ("gse"[Filter] ' \
              'AND "Homo sapiens"[Organism] AND "attribute name tissue"[Filter]' \
              ' AND ("20"[n_samples] : "500"[n_samples]))'
    handle = Entrez.esearch(db='gds', retmax=1000, term=pattern)
    geo_record = Entrez.read(handle)
    return geo_record['IdList']


@retry(urllib.error.URLError)
def retrieve_record(geo_id):
    """

    :param geo_id: GEO id
    :type geo_id: str
    :rtype : object
    Получает запись по id
    """
    handle = Entrez.esummary(db='gds', id=geo_id)
    return Entrez.read(handle)


@retry(urllib.error.URLError)
def get_paper(pmids):
    """

    :param pmids: PubMed ids of papers
    :type pmids: list
    :rtype: str
    Возвращает название статьи и список авторов
    """
    papers = []
    handle = Entrez.efetch(db="pubmed", id=[str(pmid) for pmid in pmids], rettype="medline", retmode="text")
    records = Medline.parse(handle)

    for pm_record in records:
        authors = pm_record.get("AU", "?")
        if len(authors) > 2:
            authors = '%s, %s et al.' % (authors[0], authors[1])
        papers.append('%s, %s, %s' % (pm_record.get("TI", "?"), authors, pm_record.get("SO", "?")))
    return '\n'.join(papers)


def get_summary(geo_id):
    """

    :param geo_id: GEO id
    :type geo_id: str
    :rtype: str
    Возвращает Title, текст Summary и текст Overall design
    """
    url = 'http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE%s&targ=self&form=text&view=brief' % geo_id
    geo_xml = urllib.request.urlopen(url).read().decode('utf-8').split(sep='\n')
    overall_design = ' '.join(line for line in geo_xml if '!Series_overall_design' in line)
    summary = ' '.join(line for line in geo_xml if '!Series_summary' in line)
    title = ' '.join(line for line in geo_xml if '!Series_title' in line)
    return ' '.join([title, summary, overall_design])


def get_tissue(summary):
    """

    :param summary: title + summary + overall design
    :rtype: list
    Возвращает название ткани или клеток
    """
    tissues = ['brain', 'skin', 'kidney', 'liver', 'intestine', 'ovaries',
               'breast', 'vaginal', 'glands', 'urethra', 'neuron']
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
        if 'tissue' in words[pos]:
            tiss_set.add(words[pos - 1])
        if 'cell' in words[pos]:
            cell_set.add(words[pos - 1])
        if ('cyte' in words[pos]) or ('blast' in words[pos]):
            cell_set.add(words[pos])
    return [tiss_set, cell_set]


# Entrez.email = 'kuleshov.max.v@gmail.com'
#
# if os.path.isfile('/home/maximk/Work/geroscope/tissues/id_list_unprocess.pickle'):
#     with open('/home/maximk/Work/geroscope/tissues/id_list_unprocess.pickle', 'rb') as f:
#         id_list = pickle.load(f)
# elif os.path.isfile('/home/maximk/Work/geroscope/tissues/id_list.pickle'):
#     with open('/home/maximk/Work/geroscope/tissues/id_list.pickle', 'rb') as f:
#         id_list = pickle.load(f)
# else:
#     id_list = get_id_list()
#     with open('/home/maximk/Work/geroscope/tissues/id_list.pickle', 'wb') as f:
#         pickle.dump(id_list, f)
#
# id_list_copy = deepcopy(id_list)
#
# for geo_id in id_list:
#     record = retrieve_record(geo_id)
#     paper = get_paper(record[0]['PubMedIds'])
#     ts = get_tissue(get_summary(record[0]['GSE']))
#     #  Title, Tissue, Cell, GSE, DataSet type, Samples, GEO Platform ID, Array type, Papers
#     with open('/home/maximk/Work/geroscope/tissues/tissues.txt', 'a') as file:
#         file.write('%s;%s;%s;GSE%s;%s;%s;%s;%s;%s\n' %
#                    (record[0]['title'], ', '.join(ts[0]), ','.join(ts[1]), record[0]['GSE'],
#                     ', '.join(record[0]['gdsType'].split(sep=';')), record[0]['n_samples'],
#                     ', '.join('GPL' + geo_id for geo_id in record[0]['GPL'].split(sep=';')),
#                     ', '.join(platform(record[0]['GPL'])), paper))
#     id_list_copy.remove(geo_id)
#     print(len(id_list_copy))
#     with open('/home/maximk/Work/geroscope/tissues/id_list_unprocess.pickle', 'wb') as f:
#         pickle.dump(id_list_copy, f)
