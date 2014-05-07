_author__ = 'maximk'


def separate(pgkb):
    pgkb_list = list()
    for line in pgkb:
        entity_1_type = line.split()[2]
        entity_2_type = line.split()[5]
        if(entity_1_type == 'Gene')and(entity_2_type == 'Drug'):
            print()
        elif(entity_1_type == 'Drug')and(entity_2_type == 'Gene'):
            print()
    return None


def cross_split(line):
    """
    Парсит строку с кросс-референсами в словарь вида source:id
    """
    x_dict = dict()
    l_split = line.split(sep=',')
    for line in l_split:
        if line.split(sep=':')[0] in x_dict:
            x_dict[line.split(sep=':')[0]] += ', ' + line.split(sep=':')[1]
        else:
            x_dict[line.split(sep=':')[0]] = line.split(sep=':')[1]
    return x_dict

def genes_dict(genes):
    g_dict = dict()
    for line in genes:
        l_split = line.split()
        cross = cross_split(l_split[9])
        uniprot = cross.get('uniProtKb', '')
        refseq = cross.get('refSeqDna', '')
        g_dict[l_split[0]] = '%s\t%s\t\t%s\t%s\t%s' % (l_split[4], l_split[3], l_split[2], uniprot, refseq)
    return g_dict


def drugs_dict(drugs):
    d_dict = dict()
    for line in drugs:
        l_split = line.split()
        cross = cross_split(l_split[6])
        atc = ''
        mesh = ''
        pcid = cross.get('pubChemCompound', '')
        psid = cross.get('pubChemSubstance', '')
        kegg = cross.get('keggCompound', '')
        chebi = cross.get('chebi', '')
        if l_split[9]:
            atc = l_split[9].split(sep=',')[0].split(sep=':')[1]
            if 'MeSH' in l_split[9].split(sep=',')[1]:
                mesh = l_split[9].split(sep=',')[1].split(sep=':')[1]

        d_dict[l_split[0]] = '%s\t%s\t%s\t\t%s\t%s\t%s\t%s\t\t%s'\
                             % (l_split[1], l_split[3], atc, mesh, pcid, psid, chebi, kegg)
    return None


drugs_dict = drugs_dict()