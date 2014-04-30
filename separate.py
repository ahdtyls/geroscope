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


stitch_set = set()

stitch_id = open('/home/maximk/Work/geroscope/stitch/stitch_filtered.tsv', 'r').read().split(sep='\n')

for line in stitch_id:
    for token in line.split():
        if 'CID0' in token:
            stitch_set.add(token)

stitch_dict = dict([id, {'ATC': '', 'ChEBI': '', 'ChEMBL': '', 'PC': '', 'PS': '', 'KEGG': ''}] for id in stitch_set)

# # big_stitch = open('/home/maximk/Work/geroscope/stitch/ch_srcaf', 'r')
small_stitch = open('/home/maximk/Work/geroscope/stitch/chemical_source.tsv', 'r')
small_stitch_out = open('/home/maximk/Work/geroscope/stitch/chemical_source_out.tsv', 'w')
#
#
# with open('/home/maximk/Work/geroscope/stitch/chemical_source.tsv', 'w') as small_st:
#     for line in small_stitch:
#         line = '\t'.join(line.split(sep='\t')[1:])
#         small_st.writelines(line)

for line in small_stitch:
    cid = line.split(sep='\t')[0]
    db = line.split(sep='\t')[1]
    val = line.split(sep='\t')[2].replace('\n', '')
    stitch_dict[cid][db] = val

for key in sorted(stitch_dict.keys()):
    rec = stitch_dict[key]
    small_stitch_out.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (key, rec['ATC'], rec['PC'], rec['PS'], rec['ChEBI'], rec['ChEMBL'], rec['KEGG']))
