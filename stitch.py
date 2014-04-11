__author__ = 'maximk'


from biomartpy import make_lookup, list_marts, list_attributes, list_datasets, list_filters
from sqlalchemy import create_engine


engine = create_engine('mysql+pymysql://root:root@localhost/stitch')
# execute = engine.execute('select c.name, a.alias, ac.item_id_a, ac.mode, ac.action from actions ac, chemicals c,'
#                          'chemical_aliases a where(ac.item_id_b=c.chemical)and(c.chemical=a.chemical);')
execute = engine.execute('select * from actions;')
count = 0

for r in execute:
    with open('/home/maximk/Work/geroscope/stitch/stitch.tsv', 'a') as file:
        line = dict(r)
        file.write('%s\t%s\t%s\t%s\n' % (line['item_id_a'], line['item_id_b'], line['mode'], line['action']))
        count += 1
        print(count)

# mart_name = 'ensembl'
# dataset = 'hsapiens_gene_ensembl'
# attributes = ['external_gene_id']
# filters = {'ensembl_peptide_id': ['ENSP00000216117']}
# df = make_lookup(mart_name=mart_name, dataset=dataset, attributes=attributes, filters=filters)
# print(df)