__author__ = 'maximk'

import urllib.request
from tissues import retry

@retry(urllib.error.URLError)
def get_target_genes(target_ids):
    """

    """
    ko_names = []
    hsa_names = []

    target_tails = list()
    for line in target_ids:
        if 'HSA' in line:
            target_tails.extend(['hsa:'+hsa_id for hsa_id in line.replace('HSA:', '').replace(']', '').split()])
        elif 'KO' in line:
            target_tails.extend(['ko:'+ko_id for ko_id in line.replace('KO:', '').replace(']', '').split()])

    for target_id in target_tails:
        url = 'http://www.kegg.jp/dbget-bin/www_bget?%s' % target_id
        kegg_html = urllib.request.urlopen(url).read().decode('utf-8').split(sep='\n')
        for line in range(len(kegg_html)):
            if ('<nobr>Name</nobr>' in kegg_html[line]) or ('<nobr>Gene name</nobr>' in kegg_html[line]):
                names = kegg_html[line + 1].split(sep='>')[-2].replace('<br', '')
                if 'ko' in target_id:
                    ko_names.append(names)
                elif 'hsa' in target_id:
                    hsa_names.append(names)

    return {'KO': ', '.join(ko_names), 'HSA': ', '.join(hsa_names)}


with open('/home/maximk/Work/geroscope/kegg/drug4', 'r') as kegg_db:
    kegg_drugs = kegg_db.read().split(sep='\n///\n')

kegg_dict = dict()

for drug in kegg_drugs:
    field = ''
    id = ''
    value = ''
    empty = ' '*12
    for line in drug.split(sep = '\n'):
        if line[0:12] != empty:
            if line[0:12].strip() == 'ENTRY':
                kegg_id = line[12:18]
                kegg_dict[kegg_id] = {'ENTRY':line[18:].strip()}
            else:
                field = line[0:12].strip()
                value = line[12:].strip()
                kegg_dict[kegg_id][field] = value
        else:
            value = line[12:].strip()
            kegg_dict[kegg_id][field] += '\n' + value

kegg_keys = list(kegg_dict.keys())
kegg_keys.sort()

for drug in kegg_keys:
    name = kegg_dict[drug]['NAME'].split(sep=';\n')[0]
    alias = ', '.join(kegg_dict[drug]['NAME'].split(sep=';\n')[1:])
    kegg_dict[drug]['NAME'] = name
    kegg_dict[drug]['ALIAS'] = alias
    target_na = []

    if 'TARGET' in kegg_dict[drug]:
        for target in kegg_dict[drug]['TARGET'].split(sep='\n'):
            target_name = ' '.join(target.split(sep='[')[0].strip().split(sep=' ')[:-1])
            target_action = target.split(sep = '[')[0].strip().split(sep=' ')[-1]
            target_genes = get_target_genes(target.split(sep='['))
            target_na.append('%s;%s;%s;%s\n' % (target_name, target_action, target_genes['KO'],target_genes['HSA']))
        target_na = ';;;;;;'.join(target_na)
    else:
        target_na = '\n'

    pubchem_id = ''
    drugbank_id = ''
    if 'DBLINKS' in kegg_dict[drug]:
        for link in kegg_dict[drug]['DBLINKS'].split(sep='\n'):
            if link.split(sep=':')[0].strip() == 'PubChem':
                pubchem_id = link.split(sep=':')[1].strip()
            elif link.split(sep=':')[0].strip() == 'DrugBank':
                drugbank_id = link.split(sep=':')[1].strip()

    with open('/home/maximk/Work/geroscope/kegg/kegg4.csv', 'a') as kegg_file:
        kegg_file.write('%s;%s;%s;%s;%s;%s;%s' % (drug, kegg_dict[drug]['ENTRY'], kegg_dict[drug]['NAME'], kegg_dict[drug]['ALIAS'], pubchem_id, drugbank_id, target_na))