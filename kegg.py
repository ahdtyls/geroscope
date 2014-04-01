__author__ = 'maximk'


with open('/home/maximk/Work/geroscope/kegg/drug.db', 'r') as kegg_db:
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
            target_na.append('%s;%s\n' % (target_name, target_action))
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

    with open('/home/maximk/Work/geroscope/kegg/kegg.csv', 'a') as kegg_file:
        kegg_file.write('%s;%s;%s;%s;%s;%s;%s' % (drug, kegg_dict[drug]['ENTRY'], kegg_dict[drug]['NAME'], kegg_dict[drug]['ALIAS'], pubchem_id, drugbank_id, target_na))