__author__ = 'maximk'

from os import listdir
from os.path import isfile, join

dtdb_path = '/home/maximk/Work/geroscope/dtdb/'

filenames = [f for f in listdir(dtdb_path) if isfile(join(dtdb_path,f))]

db_prefix = {'bindingdb_dtdb.tsv': 'BDB', 'chembl_dtdb.tsv': 'CBL', 'ctd_dtdb.tsv': 'CTD',
             'drugbank_dtdb.tsv': 'DRB', 'kegg_dtdb.tsv': 'KEG', 'matador_dtdb.tsv': 'MTD',
             'nci_dtdb.tsv': 'NCI', 'pgkb_dtdb.tsv': 'PGK', 'stitch_dtdb.tsv': 'STI',
             'ttd_dtdb.tsv': 'TTD'}

for filename in filenames:
    with open('dtdb_path'+filename, 'r') as file:
        prefix = db_prefix[filename]
        for line_num, line in enumerate(file):
            num = '0'*(7-len(str(line_num))) + str(line_num)
            if line_num > 0:
                line_split = line.split(sep='\t')
                drug = open('/home/maximk/Work/geroscope/dtdb/drug.tsv', 'a')
                action = open('/home/maximk/Work/geroscope/dtdb/action.tsv', 'a')
                target = open('/home/maximk/Work/geroscope/dtdb/target.tsv', 'a')

                drug.write('%sD%s\t%s\t\n' % (prefix, num, '\t'.join(line[0:10])))
                action.write('%sA%s\t%sD%s\t%sT%s\t%s\t\n' % (prefix, num, prefix, num, prefix, num, '\t'.join(line[10:15])))
                target.write('%sT%s\t%s\n' % (prefix, num, '\t'.join(line[15:])))