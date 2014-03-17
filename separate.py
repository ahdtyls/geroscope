__author__ = 'maximk'

path = ''

gero = open('/home/maximk/Work/geroscope/done/gero.txt', 'r').read().split(sep='\n')
affy = open('/home/maximk/Work/geroscope/affy.txt','w')
a = []
non_affy = open('/home/maximk/Work/geroscope/non_affy.txt','w')
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