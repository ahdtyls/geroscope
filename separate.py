# __author__ = 'maximk'
#
# path = ''
#
# gero = open('/home/maximk/Work/geroscope/retry_process.txt', 'r').read().split(sep='\n')
# affy = open('/home/maximk/Work/geroscope/affy.txt', 'w')
# a = []
# non_affy = open('/home/maximk/Work/geroscope/non_affy.txt', 'w')
# na = []
#
# for line in gero:
#     if 'Affymetrix' in line:
#         a.append(line)
#     else:
#         na.append(line)
#
# a.sort()
# na.sort()
# affy.write('\n'.join(a))
# non_affy.write('\n'.join(na))

# tissue = open('/home/maximk/Work/geroscope/tissues/tissues.txt', 'r').read().split(sep='\n')
# tiss_table = open('/home/maximk/Work/geroscope/tissues/tissue_table.txt', 'w')
#
# for line in tissue:
#     if 'GSE' in line:
#         tiss_table.write('%s\n' % line)
#     else:
#         tiss_table.write(';;;;;;;;%s\n' % line)

# r = []
# res = open('/home/maximk/Work/geroscope/stitch/stitch_filtered.tsv', 'w')
# with open('/home/maximk/Work/geroscope/stitch/stitch.tsv', 'r') as stitch:
#     for line in stitch.read().split(sep='\n'):
#         rec = line.split(sep='\t')
#         if ('C' in rec[0] and rec[1])and('E' in rec[2]):
#             r.append(line+'\n')
#         elif ('C' in rec[2] and rec[3])and('E' in rec[0]):
#             r.append(line+'\n')
#         elif ('C' in rec[0] and rec[1])and('C' in rec[2] and rec[3]):
#             r.append(line+'\n')
# r.sort()
# res.writelines(r)
#
#
#
# evidence = open('/home/maximk/Work/geroscope/nci_cancerindex/evidence.tsv', 'r').read()
# evi_table = sorted(open('/home/maximk/Work/geroscope/nci_cancerindex/evi_table.tsv', 'r').read().split(sep='\n'), reverse = True)
#
# for ev in evi_table:
#     abb = ev.split(sep='\t')[0]
#     term = ev.split(sep='\t')[1]
#     evidence = evidence.replace(abb, term)
#
# evidence = evidence.replace('finished', ' (finished)')\
#         .replace('redundant information', ' (redundant information)')\
#         .replace('unclear', ' (unclear)')\
#         .replace('\t', '')
#
#
#
# with open('/home/maximk/Work/geroscope/nci_cancerindex/evidence_tr.tsv', 'w') as e_t:
#     e_t.write(evidence)
#
# ctd_human = open('/home/maximk/Work/geroscope/dtdb/ctd_human.tsv', 'a')
#
# with open('/home/maximk/Work/geroscope/dtdb/ctd_dtdb.tsv', 'r') as ctd:
#     ctd_file = ctd.read().split(sep='\n')
#     for line in ctd_file:
#         if ('9606' in line)and('Homo sapiens' in line):
#             ctd_human.write(line+'\n')

from sqlalchemy import create_engine


def stitch_score(item_id_a, item_id_b):
    """
    Получение скора
    """
    execute = engine.execute("select score from actions where (item_id_a = '%s')and(item_id_b = '%s');" % (item_id_a, item_id_b))
    stitch_score = set()
    if execute.rowcount:
        for n in execute:
            stitch_score.add(str(dict(n)['score']))
    return ', '.join(list(stitch_score))

# plain login&password
engine = create_engine('mysql+pymysql://root:root@localhost/stitch')

with open('/home/maximk/Work/geroscope/stitch/stitch_filtered.tsv', 'r') as stitch_filtered:
    with open('/home/maximk/Work/geroscope/stitch/stitch_filtered_2.tsv', 'a') as stitch_filtered_2:
        for line in stitch_filtered:
            if ('CID' in line.split(sep='\t')[0])and('ENSP' in line.split(sep='\t')[2]):
                cid = '\t'.join(line.split(sep='\t')[0:2])
                ensp = '\t'.join(line.split(sep='\t')[2:4])
                action = '\t'.join(line.split(sep='\t')[4:]).replace('\n', '')
                score = stitch_score(line.split(sep='\t')[0], '9606.' + line.split(sep='\t')[2])
            elif('CID' in line.split(sep='\t')[2])and('ENSP' in line.split(sep='\t')[0]):
                cid = '\t'.join(line.split(sep='\t')[2:4])
                ensp = '\t'.join(line.split(sep='\t')[0:2])
                action = '\t'.join(line.split(sep='\t')[4:]).replace('\n', '')
                score = stitch_score('9606.' + line.split(sep='\t')[0], line.split(sep='\t')[2])
            stitch_filtered_2.write('%s\t%s\t%s\t%s\n' % (cid, ensp, action, score))


