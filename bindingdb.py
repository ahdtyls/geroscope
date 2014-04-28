__author__ = 'maximk'

binding_file = open('/home/maximk/Work/geroscope/bindingdb/BindingDB_All.tsv', 'r')

with open('/home/maximk/Work/geroscope/bindingdb/bindingdb.tsv', 'a') as bindingdb:
    for line in binding_file.read().strip().split(sep='\n'):
        rec = line.split('\t')
        if 'Homo sapiens' in rec[5]:
            drug_name = rec[3]
            pubchem_cid = rec[26]
            pubchem_sid = rec[27]
            chebi = rec[28]
            chembl = rec[29]
            kegg = rec[32]

            action = 'binding'
            evidence = rec[14]
            pmid = rec[16]

            target_name = rec[4]
            gene_symbol = rec[38].split(sep='_')[0]
            uniprot = rec[38]

            bindingdb.write('%s\t\t\t\t\t%s\t%s\t%s\t%s\t%s\t%s\t\t%s\t%s\t\t%s\t%s\t\t\t%s\t\n'
                            % (drug_name, pubchem_cid, pubchem_sid, chebi, chembl, kegg, action, evidence, pmid,
                               gene_symbol,target_name, uniprot))