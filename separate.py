__author__ = 'maximk'

# path = ''
#
gero = open('/home/maximk/Work/geroscope/retry_process.txt', 'r').read().split(sep='\n')
affy = open('/home/maximk/Work/geroscope/affy.txt', 'w')
a = []
non_affy = open('/home/maximk/Work/geroscope/non_affy.txt', 'w')
na = []

for line in gero:
    if 'Affymetrix' in line:
        a.append(line)
    else:
        na.append(line)

a.sort()
na.sort()
affy.write('\n'.join(a))
non_affy.write('\n'.join(na))

# tissue = open('/home/maximk/Work/geroscope/tissues/tissues.txt', 'r').read().split(sep='\n')
# tiss_table = open('/home/maximk/Work/geroscope/tissues/tissue_table.txt', 'w')
#
# for line in tissue:
#     if 'GSE' in line:
#         tiss_table.write('%s\n' % line)
#     else:
#         tiss_table.write(';;;;;;;;%s\n' % line)