__author__ = 'maximk'

import pickle
import ftplib
import urllib

from Bio import Entrez
from copy import deepcopy

Entrez.email = 'kuleshov.max.v@gmail.com'


def cel(ftp_address):
    """
    Проверяет наличие CEL-файлов
    """
    cel_pres = '-'
    try:
        ftp = ftplib.FTP('ftp.ncbi.nlm.nih.gov')
        ftp.login()
        ftp.cwd(ftp_address[26:])
        files_list = ftp.mlsd()
        if 'suppl' in files_list:
            ftp.cwd('suppl')
        files_list = ftp.mlsd()
        if 'filelist.txt' in files_list:
            ftp.retrbinary('RETR filelist.txt', open('filelist.txt', 'wb').write)

        filelist = open('filelist.txt', 'r').read()
        for line in filelist.split(sep='\n'):
            if 'CEL' in line:
                cel_pres = '+'
                ftp.quit()
                return cel_pres
        ftp.quit()
    except ftplib.all_errors as e:
        print('%s' % e)
        cel_pres = '0'
    return cel_pres


def platform(gpls):
    """
    Возвращает название платформы
    """
    platforms = []
    for gpl in gpls.split(sep=';'):
        gpl_id = '1' + (8 - len(str(gpl))) * '0' + str(gpl)
        handle = Entrez.esummary(db="gds", id=gpl_id)
        summary = Entrez.read(handle)
        platforms.append(summary[0]['title'])
    return platforms


def check_design(drug_names, geo_id):
    """
    Проверяет, есть ли название лекарства в overall design
    """

    url = 'http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE%s&targ=self&form=text&view=brief' % geo_id
    geo_xml = urllib.request.urlopen(url).read().decode('utf-8').split(sep='\n')
    overall_design = ' '.join(line for line in geo_xml if '!Series_overall_design' in line)
    for drug_name in drug_names:
        if (drug_name in overall_design) or (drug_name.lower() in overall_design):
            return True
    return False


def check_presence(drug_name, summary):
    """
    Проверяет, на самом ли деле в названии или описании эксперимента говорится о заданном лекарстве
    """
    drug_names = [' ' + drug_name + ' ', ' ' + drug_name + '.', ' ' + drug_name + ',', '(' + drug_name + ')', ]
    for drug_name in drug_names:
        if (drug_name in summary[0]['title']) or (drug_name in summary[0]['summary']) \
                or (drug_name.lower() in summary[0]['title']) or (drug_name.lower() in summary[0]['summary']):
            return True
    return check_design(drug_names, summary[0]['GSE'])


def retrieve_record(gero_dict, path):
    """
    Возвращает выбранные параметры для всех записией по данному запросу
    """
    geo_dir = path
    gero_dict_copy = deepcopy(gero_dict)
    for drug in gero_dict.keys():
        for alias in gero_dict[drug].keys():
            if gero_dict[drug][alias]:
                for geo_id in gero_dict[drug][alias]:
                    handle = Entrez.esummary(db='gds', id=geo_id)
                    summary = Entrez.read(handle)
                    if check_presence(alias, summary):
                        cel_presence = cel(summary[0]['FTPLink'])
                        for c in str(summary[0]['GPL']).split(sep=';'):
                            print('%s;%s;%s;%s;%s;%s;GPL%s;%s' %
                                  (drug, alias, summary[0]['Accession'], summary[0]['title'],
                                   summary[0]['n_samples'], cel_presence, c, ','.join(platform(c))))
                            with open(geo_dir + 'retry_process.txt', 'a') as file:
                                file.write('%s;%s;%s;%s;%s;%s;GPL%s;%s\n' %
                                           (drug, alias, summary[0]['Accession'], summary[0]['title'],
                                            summary[0]['n_samples'], cel_presence, c, ','.join(platform(c))))
                            if (gero_dict_copy[drug][alias]) and (geo_id in gero_dict_copy[drug][alias]):
                                gero_dict_copy[drug][alias].remove(geo_id)
                                with open(geo_dir + 'retry_unprocess.pickle', 'wb') as f:
                                    pickle.dump(gero_dict_copy, f)
                    elif (gero_dict_copy[drug][alias]) and (geo_id in gero_dict_copy[drug][alias]):
                        gero_dict_copy[drug][alias].remove(geo_id)
                        with open(geo_dir + 'retry_unprocess.pickle', 'wb') as f:
                            pickle.dump(gero_dict_copy, f)
    return None


def main():
    return None


if __name__ == '__main__':
    main()