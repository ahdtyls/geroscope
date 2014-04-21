__author__ = 'maximk'

import xmltodict
import os.path
import pickle
from collections import OrderedDict

def parce_nci(nci_file):
    """

    """
    return None

def get_nci(nci_id):
    """

    """
    return None

if os.path.isfile('/home/maximk/Work/geroscope/nci_cancerindex/nci.pickle'):
    with open('/home/maximk/Work/geroscope/nci_cancerindex/nci.pickle', 'rb') as nci_pickle:
        nci = pickle.load(nci_pickle)
else:
    nci = xmltodict.parse(open('/home/maximk/Work/geroscope/nci_cancerindex/sample.xml', 'r').read())
    with open('/home/maximk/Work/geroscope/nci_cancerindex/nci.pickle', 'wb') as nci_pickle:
        pickle.dump(nci, nci_pickle)

nci_result = list()
for gene_entry_key in nci['GeneEntryCollection'].keys():
    nci_set = set()
    if gene_entry_key == 'GeneEntry':
        gene_entry_list = nci['GeneEntryCollection']['GeneEntry']
        if type(gene_entry_list) == OrderedDict:
            gene_entry_list = [gene_entry_list]
        for gene_entry in gene_entry_list:
            gene_name = gene_entry.get('HUGOGeneSymbol', '')

            if gene_entry.get('SequenceIdentificationCollection', ''):
                gene_genbank = gene_entry['SequenceIdentificationCollection'].get('GenbankAccession', '')
                gene_refseq = gene_entry['SequenceIdentificationCollection'].get('RefSeqID', '')
                gene_uniprot = gene_entry['SequenceIdentificationCollection'].get('UniProtID', '')
                gene_hugo = gene_entry['SequenceIdentificationCollection'].get('HgncID', '')

            if gene_entry.get('Sentence', ''):
                for sentence_key in gene_entry.keys():
                    if sentence_key == 'Sentence':
                        sentence_list = gene_entry['Sentence']
                        if type(sentence_list) == OrderedDict:
                            sentence_list = [sentence_list]
                        for sentence in sentence_list:
                            if sentence.get('Organism', '') == 'Human':
                                cell_line = sentence.get('CellineIndicator', '')
                                evidence = sentence.get('EvidenceCode', '')
                                if type(evidence) == list:
                                    evidence = ', '.join(evidence)

                                # todo Запарсить сюда NCI Thesaurus
                                drug_name = ''
                                if sentence.get('DrugData', ''):
                                    drug_name = sentence['DrugData'].get('DrugTerm', '')
                                    drug_concept = sentence['DrugData'].get('NCIDrugConceptCode', '')

                                gene_concept = ''
                                if sentence.get('GeneData', ''):
                                    gene_concept = sentence['GeneData'].get('NCIGeneConceptCode', '')

                                role = ''
                                if sentence.get('Roles', ''):
                                    role = sentence['Roles'].get('PrimaryNCIRoleCode', '')
                                    second_role = sentence['Roles'].get('OtherRole', '')
                                    if type(role) == list:
                                        role = ', '.join(role)
                                    if type(second_role) == list:
                                        second_role = ', '.join(second_role)
                                    role = (role + ' (' + second_role + ')').replace('_', ' ')\
                                        .replace('Chemical or Drug ', '')\
                                        .replace('not assigned', '')\
                                        .replace(' ()', '')
                                    if(role[1] == '(')and(role[-1] == ')'):
                                        role = role[1:-1]

                                sentence_status = sentence.get('SentenceStatusFlag').replace('_', ' ')

                                nci_set.add('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %
                                            (drug_name, gene_name, role, gene_genbank, gene_refseq, gene_uniprot,
                                             gene_hugo, cell_line, evidence, sentence_status))
    nci_result += list(nci_set)

with open('/home/maximk/Work/geroscope/nci_cancerindex/nci.tsv', 'a') as nci_result_file:
    nci_result_file.writelines(sorted(nci_result))