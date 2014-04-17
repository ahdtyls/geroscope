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


ttd = ttd_main(open('/home/maximk/Work/geroscope/ttd/TTD_download.txt', 'r'))
result = []
actions = sorted(['Activator', 'Intercalator', 'Ligand', 'Antibody', 'Aptamer', 'Opener', 'Blocker', 'Antagonist',
           'Suppressor', 'Breaker', 'Regulator', 'Agonist', 'Antisense', 'Enhancer', 'Minor groove binder',
           'Antigen', 'Vaccine', 'Stimulator', 'Cofactor', 'Binder', 'Stablizer', 'Modulator', 'Inducer',
           'Inhibitor', 'UpRegulator', 'Adduct'])

for rec in ttd.values():
    target = '%s\t%s\t%s\t%s\n' % (rec['Name'], rec['Synonyms'], rec['UniProt ID'], rec['Type of target'])
    for action in actions:
        if rec[action]:
            result.append('%s\t%s\t%s' % (rec[action], action, target))

with open('/home/maximk/Work/geroscope/ttd/ttd.tsv', 'w') as ttd_result:
    ttd_result.writelines(sorted(result))