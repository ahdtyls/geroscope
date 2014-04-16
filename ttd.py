__author__ = 'maximk'


# def add_to_dic(dic, key, element):
#     if key in dic:
#         dic[key]
#     else:
#         dic[key] = element


def ttd_uniprot(file):
    uniprot = [line.replace('\ufeff', '').split(sep='\t') for line in file.read().split(sep='\n')]
    ids_set = set(line[0] for line in uniprot)
    keys_set = set(line[0] for line in uniprot)
    return None


def ttd_syn(file):
    syn = [line.replace('\ufeff', '').split(sep='\t') for line in file.read().split(sep='\n')]
    return None


def ttd_crossmatch(file):
    crossmatch = [line.replace('\ufeff', '').split(sep='\t') for line in file.read().split(sep='\n')]
    ids_set = set(line[0] for line in crossmatch)
    keys_set = set(line[0] for line in crossmatch)
    return None


def ttd_main(file):
    main_dict = dict()
    main = [line.replace('\ufeff', '').split(sep='\t') for line in file.read().split(sep='\n')]
    ids_set = sorted(list(set(line[0] for line in main)))
    keys_set = set(line[1] for line in main)
    for main_id in ids_set:
        main_dict[main_id] = dict(zip(keys_set, ['']*len(keys_set)))
    for line in main:
        main_dict[line[0]][line[1]] = line[2]
    return None




ttd_main(open('/home/maximk/Work/geroscope/ttd/TTD_download.txt', 'r'))