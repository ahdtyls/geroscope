__author__ = 'maximk'

from sqlalchemy import create_engine

# http://string-stitch.blogspot.ru/2008/02/we-have-api.html

def chem_name(stitch_id):
    """
    Получение названия драга из базы
    """
    execute = engine.execute("select name from chemicals where chemical = '%s';" % stitch_id)
    stitch_name = set()
    if execute.rowcount:
        for n in execute:
            stitch_name.add(dict(n)['name'])
    return ', '.join(list(stitch_name))

def chem_alias(stitch_id):
    """
    Получение алиас драга из базы
    """
    execute = engine.execute("select alias from chemical_aliases where chemical = '%s';" % stitch_id)
    stitch_alias = set()
    if execute.rowcount:
        for n in execute:
            stitch_alias.add(dict(n)['alias'])
    return ', '.join(list(stitch_alias))


def parse_ensp(ensp_file):
    """
    Парсинг названия генов из ENSEMBL, полученных через biomaRt
    """
    ensp = dict()
    for line in ensp_file.read().split(sep='\n'):
        ensp_id = line.split(sep=',')[1].replace('"', '')
        gene_name = line.split(sep=',')[2].replace('"', '')
        if ensp_id:
            ensp[ensp_id] = gene_name
    return ensp


# ensembl_prot = parse_ensp(open('/home/maximk/Work/geroscope/stitch/ensembl.csv', 'r'))

# plain login&password
engine = create_engine('mysql+pymysql://root:root@localhost/stitch')
# execute = engine.execute('select * from actions;')
# count = 0
#
# for r in execute:
#     with open('/home/maximk/Work/geroscope/stitch/stitch.tsv', 'a') as file:
#         line = dict(r)
#         ch_name = chem_name(line['item_id_b'])
#         name1 = line['item_id_a'] + '\t' + chem_name(line['item_id_a']) if 'CID' in line['item_id_a'] \
#             else line['item_id_a'].split(sep='.')[1] + '\t' + ensembl_prot.get(line['item_id_a'].split(sep='.')[1], '')
#         name2 = line['item_id_b'] + '\t' + chem_name(line['item_id_b']) if 'CID' in line['item_id_b'] \
#             else line['item_id_b'].split(sep='.')[1] + '\t' + ensembl_prot.get(line['item_id_b'].split(sep='.')[1], '')
#         file.write('%s\t%s\t%s\t%s\n' % (name1, name2, line['mode'], line['action']))
#         count += 1
#         print(count)

stitch_id = open('/home/maximk/Work/geroscope/stitch/stitch_filtered_2.tsv', 'r').read().split(sep='\n')
stitch_set = dict([line.split(sep='\t')[0], {'name': line.split(sep='\t')[1],
                                             'gene_symbol': line.split(sep='\t')[3],
                                             'ensp': line.split(sep='\t')[2],
                                             'action': '\t'.join(line.split(sep='\t')[4:6]),
                                             'score':line.split(sep='\t')[6]}] for line in stitch_id)

# for line in stitch_id:
#     for token in line.split():
#         if 'CID0' in token:
#             stitch_set.add(token)


stitch_dict = dict([id, {'ATC': '', 'ChEBI': '', 'ChEMBL': '', 'PC': '', 'PS': '', 'KEGG': ''}] for id in stitch_set.keys())

# # big_stitch = open('/home/maximk/Work/geroscope/stitch/ch_srcaf', 'r')
small_stitch = open('/home/maximk/Work/geroscope/stitch/chemical_source.tsv', 'r')

#
#
# with open('/home/maximk/Work/geroscope/stitch/chemical_source.tsv', 'w') as small_st:
#     for line in small_stitch:
#         line = '\t'.join(line.split(sep='\t')[1:])
#         small_st.writelines(line)

for line in small_stitch:
    cid = line.split(sep='\t')[0]
    if stitch_dict.get(cid, ''):
        db = line.split(sep='\t')[1]
        val = line.split(sep='\t')[2].replace('\n', '')
        stitch_dict[cid][db] = val

with open('/home/maximk/Work/geroscope/stitch/chemical_source_out.tsv', 'a') as small_stitch_out:
    for key in sorted(stitch_dict.keys()):
        rec = stitch_dict[key]
        small_stitch_out.write('%s\t%s\t%s\t\t\t%s\t%s\t%s\t%s\t%s\t%s\t\t\t%s\t%s\t\t%s\n' %
                               (stitch_set[key]['name'], chem_alias(key), rec['ATC'], rec['PC'], rec['PS'],
                                rec['ChEBI'], rec['ChEMBL'], rec['KEGG'], stitch_set[key]['action'],
                                stitch_set[key]['score'], stitch_set[key]['gene_symbol'], stitch_set[key]['ensp']))