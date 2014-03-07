__author__ = 'maximk'

from Bio import Entrez
from ftplib import FTP

Entrez.email = 'kuleshov.max.v@gmail.com'

def cel(ftp_adress):
    """
    Проверяет наличие CEL-файлов
    """
    cel_pres = '-'
    ftp = FTP('ftp.ncbi.nlm.nih.gov')
    ftp.login()
    ftp.cwd(ftp_adress[26:])
    # Вообще-то nlst нужно заменить на mlsd
    files_list = ftp.nlst()
    if 'suppl' in files_list:
        ftp.cwd('suppl')
    files_list = ftp.nlst()
    if 'filelist.txt' in files_list:
        ftp.retrbinary('RETR filelist.txt', open('filelist.txt', 'wb').write)

    filelist = open('/home/maximk/PycharmProjects/heroscope/filelist.txt', 'r').read()
    for line in filelist.split(sep='\n'):
        if 'CEL' in line:
            cel_pres = '+'
            ftp.quit()
            return cel_pres
    ftp.quit()
    return cel_pres

def platform(gpl):
    """
    Возвращает название платформы
    """
    platforms = []
    gpl_id = '1' + (8-len(str(gpl)))*'0' + str(gpl)
    handle = Entrez.esummary(db="gds", id=gpl_id)
    summary = Entrez.read(handle)
    platforms.append(summary[0]['title'])
    return platforms

def retrieve_record(query):
    """
    Возвращает выбранные параметры для всех записией по данному запросу
    """
    handle = Entrez.esearch(db='gds', retmax=200, term='("bevacizumab"[All Fields] OR Bevacizumab[All Fields]) AND ("expression profiling by array"[DataSet Type] OR "expression profiling by high throughput sequencing"[DataSet Type]) AND "gse"[Filter]')
    #((expression profiling by array[DataSet Type])OR(expression profiling by high throughput sequencing[DataSet Type]))AND(gse[Filter])AND((ThT[Description])OR(ThT[Title]))
    record = Entrez.read(handle)
    for geo_id in record['IdList']:
            handle = Entrez.esummary(db='gds', id=geo_id)
            summary = Entrez.read(handle)
            cel_presence = cel(summary[0]['FTPLink'])

            for c in str(summary[0]['GPL']).split(sep = ';'):
                #print('GEO Series ID: %s\nName: %s\nSamples: %s\nCEL files: %s\nGEO Platform ID: GPL%s\nPlatform: %s' % (summary[0]['Accession'], summary[0]['title'], len(summary[0]['Samples']), cel_presence, c, ','.join(platform(c))))
                print('%s;%s;%s;%s;GPL%s;%s' % (summary[0]['Accession'], summary[0]['title'], len(summary[0]['Samples']), cel_presence, c, ','.join(platform(c))))
                #print()

    return None

retrieve_record('')
#cel('ftp.debian.org')