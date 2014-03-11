__author__ = 'maximk'

def makedic(file):
    """
    Превращает список лекарств и альясов к ним в словарь-шаблон
    """
    al_dict = {}
    for line in file:
        name = line.strip().split(sep='\t')
        al_dict[name[0]] = dict()
        al_dict[name[0]][name[0]] = dict()
        if len(name) > 1:
            al_list = name[1].split(sep=';')
            for al in al_list:
                al_dict[name[0]][al] = dict()
    return al_dict

path = '/home/maximk/Work/Heroscope/geroprotective_drugs.txt'
geroprot = open(path, 'r').read().split(sep='\n')

d = makedic(geroprot)