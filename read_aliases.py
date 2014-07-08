__author__ = 'maximk'

import pickle
import os.path
import sys

from copy import deepcopy
from Bio import Entrez
from geo import retrieve_record


Entrez.email = 'kuleshov.max.v@gmail.com'


def makedic(file):
    """
    Превращает список лекарств и альясов к ним в словарь-шаблон
    """
    al_dict = {}
    for line in file:
        name = line.strip().split(sep='\t')
        al_dict[name[0]] = dict()
        al_dict[name[0]][name[0]] = dict()
        if len(name) > 1:
            al_list = name[1].split(sep=';')
            for al in al_list:
                al_dict[name[0]][al] = dict()
    return al_dict


def set_id_list(geroprot):
    """
    Для каждого алиаса устанавливает список id в базе GEO
    """
    for drug in geroprot.keys():
        for alias in geroprot[drug].keys():
            pattern = '((expression profiling by array[DataSet Type])OR(expression profiling by high throughput ' \
                      'sequencing[DataSet Type]))AND (gse[Filter])AND((%s[Description])OR(%s[Title]))' \
                      'AND(homo sapiens[Organism])' % (alias, alias)
            handle = Entrez.esearch(db='gds', retmax=500, term=pattern)
            record = Entrez.read(handle)
            geroprot[drug][alias] = record['IdList']

    # Удаление пустых алиасов
    geroprot_copy = deepcopy(geroprot)
    for drug in geroprot.keys():
        for alias in geroprot[drug].keys():
            if (drug != alias) and (not (geroprot[drug][alias])):
                geroprot_copy[drug].pop(alias)
    geroprot = geroprot_copy

    # Удаление дублирующихся id
    for drug in geroprot.keys():
        id_set = set()
        for alias in geroprot[drug].keys():
            diff_alias = id_set.intersection(set(geroprot[drug][alias]))
            if diff_alias:
                for id_drug in diff_alias:
                    geroprot[drug][alias].remove(id_drug)

            diff_drug = set(geroprot[drug][drug]).intersection(set(geroprot[drug][alias]))
            if alias != drug:
                id_set = id_set.union(set(geroprot[drug][alias]))
                if diff_drug:
                    for id_drug in diff_drug:
                        geroprot[drug][drug].remove(id_drug)

    return geroprot_copy

def main():
    if len(sys.argv) == 1:
        argv = None
        path = '/home/maximk/Work/geroscope/geo/8.07/drugs.txt'
    else:
        argv = sys.argv[1:]
        path = argv[0]

    path, drugs = os.path.split(path)
    d_mod = drugs.split(sep='.')[0]
    geroprot = open(os.path.join(path, drugs), 'r').read().split(sep='\n')

    if os.path.isfile(os.path.join(path, 'retry_unprocess_%s.pickle' % d_mod)):
        with open(os.path.join(path, 'retry_unprocess_%s.pickle' % d_mod, 'rb')) as f:
            gero_dict = pickle.load(f)
    elif os.path.isfile(os.path.join(path, 'retry_%s.pickle' % d_mod)):
        with open(os.path.join(path, 'retry_%s.pickle' % d_mod), 'rb') as f:
            gero_dict = pickle.load(f)
    else:
        gero_dict = set_id_list(makedic(geroprot))
        with open(os.path.join(path, 'retry_%s.pickle' % d_mod), 'wb') as f:
            pickle.dump(gero_dict, f)

    retrieve_record(gero_dict, os.path.join(path, drugs))
    return None

if __name__=='__main__':
    main()