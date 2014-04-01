__author__ = 'maximk'


with open('/home/maximk/Work/geroscope/kegg/test.txt', 'r') as kegg_db:
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

for drug in kegg_dict.keys():
    name = kegg_dict[drug]['NAME'].split(sep=';\n')[0]
    alias = '\n'.join(kegg_dict[drug]['NAME'].split(sep=';\n')[1:])
    kegg_dict[drug]['NAME'] = name
    kegg_dict[drug]['ALIAS'] = alias
    target_na = ''

    for target in kegg_dict[drug]['TARGET'].split(sep='\n'):
        target_name = ' '.join(target.split(sep='[')[0].strip().split(sep=' ')[:-1])
        target_action = target.split(sep = '[')[0].strip().split(sep=' ')[-1]
        target_na += '%s;%s\n' % (target_name, target_action)

    print('ID\t%s\nENTRY\t%s\nNAME\t%s\nALIAS\t%s\nDBLINKS\t%s\nTARGET\t%s\n' % (drug, kegg_dict[drug]['ENTRY'], kegg_dict[drug]['NAME'], kegg_dict[drug]['ALIAS'],kegg_dict[drug]['DBLINKS'], target_na))