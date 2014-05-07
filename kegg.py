__author__ = 'maximk'

import urllib.request
import os.path
import pickle
from tissues import retry
from copy import deepcopy

@retry(urllib.error.URLError)
def get_target_genes(target_ids):
    """
    Возвращает гены для таргета из KEGG Homo Sapience
    :param target_ids: TARGET string from KEGG Drugs
    """
    hsa_names = []
    uniprot = []
    ensg = []

    target_tails = list()
    for line in target_ids:
        if 'HSA' in line:
            target_tails.extend(['hsa:'+hsa_id for hsa_id in line.replace('HSA:', '').replace(']', '').split()])

    for target_id in target_tails:
        url = 'http://www.kegg.jp/dbget-bin/www_bget?%s' % target_id
        kegg_html = urllib.request.urlopen(url).read().decode('utf-8').split(sep='\n')

        if target_id in hsa_cache:
            hsa_names.extend(hsa_cache[target_id]['gene_symbol'])
            uniprot.extend(hsa_cache[target_id]['uniprot'])
            ensg.extend(hsa_cache[target_id]['ensg'])
        else:
            for line in range(len(kegg_html)):
                if '<nobr>Gene name</nobr>' in kegg_html[line]:
                    names = kegg_html[line + 1].split(sep='>')[-2].replace('<br', '')
                    hsa_names.append(names)
                elif('Other DBs' in kegg_html[line]):
                    clob = kegg_html[line+1].split(sep='</div>')
                    for db_line in clob:
                        if 'ensembl' in db_line:
                            ensg_line = db_line.replace('<div style="margin-left:5em">', '')\
                                .replace('<a href="http://www.ensembl.org/Homo_sapiens/geneview?gene=', '')\
                                .replace('">', ' ').replace('</a>', ' ')
                            ensg.extend(list((set(ensg_line.strip().split()))))
                        elif 'uniprot' in db_line:
                            uniprot_line = db_line.replace('<div style="margin-left:5em">', '')\
                                .replace('<a href="http://www.uniprot.org/uniprot/', '')\
                                .replace('">', ' ').replace('</a>', ' ')
                            uniprot.extend(list((set(uniprot_line.strip().split()))))
            hsa_cache[target_id] = {'gene_symbol': hsa_names, 'uniprot': uniprot, 'ensg': ensg}

    with open('/home/maximk/Work/geroscope/kegg/kegg_hsa.pickle', 'wb') as f:
        pickle.dump(hsa_cache, f)
    return {'gene_symbol': ', '.join(hsa_names), 'uniprot': ', '.join(uniprot), 'ensg': ', '.join(ensg)}


with open('/home/maximk/Work/geroscope/kegg/drug.db', 'r') as kegg_db:
    kegg_drugs = kegg_db.read().split(sep='\n///\n')

hsa_cache = dict()
if os.path.isfile('/home/maximk/Work/geroscope/kegg/kegg_hsa.pickle'):
    with open('/home/maximk/Work/geroscope/kegg/kegg_hsa.pickle', 'rb') as f:
        hsa_cache = pickle.load(f)

kegg_dict = dict()
for drug in kegg_drugs:
    field = ''
    value = ''
    empty = ' '*12
    for line in drug.split(sep='\n'):
        if line[0:12] != empty:
            if line[0:12].strip() == 'ENTRY':
                kegg_id = line[12:18]
                kegg_dict[kegg_id] = {'ENTRY': line[18:].strip()}
            else:
                field = line[0:12].strip()
                value = line[12:].strip()
                kegg_dict[kegg_id][field] = value
        else:
            value = line[12:].strip()
            kegg_dict[kegg_id][field] += '\n' + value

if os.path.isfile('/home/maximk/Work/geroscope/kegg/kegg_keys.pickle'):
    with open('/home/maximk/Work/geroscope/kegg/kegg_keys.pickle', 'rb') as f:
        kegg_keys = pickle.load(f)
else:
    kegg_keys = list(kegg_dict.keys())
    kegg_keys.sort()

tmp = deepcopy(kegg_keys)

# drug = kegg_id
for drug in kegg_keys:
    if 'TARGET' in kegg_dict[drug]:
        name = kegg_dict[drug]['NAME'].split(sep=';\n')[0]
        alias = ', '.join(kegg_dict[drug]['NAME'].split(sep=';\n')[1:])
        kegg_dict[drug]['NAME'] = name
        kegg_dict[drug]['ALIAS'] = alias

        pubchem_id = ''
        drugbank_id = ''
        cas = ''
        atc = ''

        if 'REMARK' in kegg_dict[drug]:
            for remark in kegg_dict[drug]['REMARK'].split(sep='\n'):
                if remark.split(sep=':')[0].strip() == 'ATC code':
                    atc = ', '.join(remark.split(sep=':')[1].strip().split())

        if 'DBLINKS' in kegg_dict[drug]:
            for link in kegg_dict[drug]['DBLINKS'].split(sep='\n'):
                if link.split(sep=':')[0].strip() == 'PubChem':
                    pubchem_id = link.split(sep=':')[1].strip()
                elif link.split(sep=':')[0].strip() == 'DrugBank':
                    drugbank_id = link.split(sep=':')[1].strip()
                elif link.split(sep=':')[0].strip() == 'CAS':
                    cas = link.split(sep=':')[1].strip()

            target_na = []
            for target in kegg_dict[drug]['TARGET'].split(sep='\n'):
                target_name = ' '.join(target.split(sep='[')[0].strip().split(sep=' ')[:-1])
                target_action = target.split(sep='[')[0].strip().split(sep=' ')[-1]
                target_genes = get_target_genes(target.split(sep='['))
                target_na.append('%s\t\t\t\t\t%s\t%s\t\t%s\t%s\n' % (target_action, target_genes['gene_symbol'], target_name, target_genes['ensg'], target_genes['uniprot']))
            for target_rec in target_na:
                with open('/home/maximk/Work/geroscope/kegg/kegg.csv', 'a') as kegg_file:
                    kegg_file.write('%s\t%s\t%s\t%s\t\t\t%s\t\t\t%s\t%s' % (name, alias, atc, cas, pubchem_id, drug, target_rec))

    del tmp[0]
    with open('/home/maximk/Work/geroscope/kegg/kegg_keys.pickle', 'wb') as f:
        pickle.dump(tmp, f)