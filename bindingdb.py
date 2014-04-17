__author__ = 'maximk'

binding_file = open('/home/maximk/Work/geroscope/bindingdb/BindingDB_All.tsv', 'r')

with open('/home/maximk/Work/geroscope/bindingdb/bindingdb.tsv', 'a') as bindingdb:
    for line in binding_file.read().strip().split(sep='\n'):
        rec = line.split('\t')
        if 'Homo sapiens' in rec[5]:
            # Drug name, Target name, Uniprot Gene Name, Source,
            bindingdb.write('%s\t%s\t%s\t%s\n' % (rec[3], rec[4], rec[38].split(sep='_')[0], rec[14]))