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