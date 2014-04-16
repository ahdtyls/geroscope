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
            print()
            stitch_name.add(dict(n)['name'])
    return ', '.join(list(stitch_name))


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


ensembl_prot = parse_ensp(open('/home/maximk/Work/geroscope/stitch/ensembl.csv', 'r'))

engine = create_engine('mysql+pymysql://root:root@localhost/stitch')
execute = engine.execute('select * from actions;')
count = 0

for r in execute:
    with open('/home/maximk/Work/geroscope/stitch/stitch.tsv', 'a') as file:
        line = dict(r)
        ch_name = chem_name(line['item_id_b'])
        name1 = line['item_id_a'] + '\t' + chem_name(line['item_id_a']) if 'CID' in line['item_id_a'] \
            else line['item_id_a'].split(sep='.')[1] + '\t' + ensembl_prot.get(line['item_id_a'].split(sep='.')[1], '')
        name2 = line['item_id_b'] + '\t' + chem_name(line['item_id_b']) if 'CID' in line['item_id_b'] \
            else line['item_id_b'].split(sep='.')[1] + '\t' + ensembl_prot.get(line['item_id_b'].split(sep='.')[1], '')
        file.write('%s\t%s\t%s\t%s\n' % (name1, name2, line['mode'], line['action']))
        count += 1
        print(count)