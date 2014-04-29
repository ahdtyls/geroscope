__author__ = 'maximk'


def ttd_main(file):
    main_dict = dict()
    main = [line.split(sep='\t') for line in file.read().replace('\ufeff', '').split(sep='\n')]
    ids_set = sorted(list(set(line[0] for line in main)))
    keys_set = set(line[1] for line in main)
    for main_id in ids_set:
        main_dict[main_id] = dict(zip(keys_set, ['']*len(keys_set)))
    for line in main:
        main_dict[line[0]][line[1]] = line[2]
    return main_dict

def ttd_drug(file):
    main_dict = dict()
    main = [line.split(sep='\t') for line in file.read().replace('\ufeff', '').split(sep='\n')]
    ids_set = sorted(list(set(line[0] for line in main)))
    keys_set = set(line[2] for line in main)
    for main_id in ids_set:
        main_dict[main_id] = dict(zip(keys_set, ['']*len(keys_set)))
    for line in main:
        main_dict[line[0]][line[2]] = line[3]

    drug_dict = dict()
    for key in main_dict.keys():
        drug_dict[main_dict[key]['DrugName']] = main_dict[key]

    return drug_dict

def ttd_syn(file):
    main_dict = dict()
    main = [line.split(sep='\t') for line in file.read().replace('\ufeff', '').split(sep='\n')]

    for line in main:
        main_dict[line[1]] = line[2]
    return main_dict


ttd = ttd_main(open('/home/maximk/Work/geroscope/ttd/TTD_download.txt', 'r'))
ttd_drugs = ttd_drug(open('/home/maximk/Work/geroscope/ttd/TTD_crossmatching.txt', 'r'))
ttd_syns = ttd_syn(open('/home/maximk/Work/geroscope/ttd/TTD_Synonyms.txt', 'r'))

result = []

actions = sorted(['Activator', 'Intercalator', 'Ligand', 'Antibody', 'Aptamer', 'Opener', 'Blocker', 'Antagonist',
           'Suppressor', 'Breaker', 'Regulator', 'Agonist', 'Antisense', 'Enhancer', 'Minor groove binder',
           'Antigen', 'Vaccine', 'Stimulator', 'Cofactor', 'Binder', 'Stablizer', 'Modulator', 'Inducer',
           'Inhibitor', 'UpRegulator', 'Adduct'])

for rec in ttd.values():
    target = '\t%s\t\t\t\t%s\t\t\t%s\n' % (rec['Type of target'], rec['Name'], rec['UniProt ID'])
    for action in actions:
        if rec[action]:
            drug_name = rec[action]
            atc, cas, pubchem_cid, pubchem_sid, chebi, aliases = '', '', '', '', '', ''
            if ttd_drugs.get(drug_name, ''):
                atc = ttd_drugs[drug_name].get('SuperDrug ATC', '')
                cas = ttd_drugs[drug_name].get('CAS Number', '')
                pubchem_cid = ttd_drugs[drug_name].get('PubChem CID', '')
                if pubchem_cid:
                    pubchem_cid = pubchem_cid.split(sep=' ')[1]
                pubchem_sid = ttd_drugs[drug_name].get('PubChem SID', '')
                if pubchem_sid:
                    pubchem_sid = pubchem_sid.split(sep=' ')[1]
                chebi = ttd_drugs[drug_name].get('ChEBI ID', '')
            if ttd_syns.get(drug_name, ''):
                aliases = ttd_syns[drug_name]
            result.append('%s\t%s\t%s\t%s\t\t%s\t%s\t%s\t\t\t%s\t%s' % (drug_name, aliases, atc, cas, pubchem_cid, pubchem_sid, chebi, action, target))

with open('/home/maximk/Work/geroscope/ttd/ttd.tsv', 'w') as ttd_result:
    ttd_result.writelines(sorted(result))