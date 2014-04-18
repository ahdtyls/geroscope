__author__ = 'maximk'

import xmltodict

nci = xmltodict.parse(open('/home/maximk/Work/geroscope/nci_cancerindex/nci.xml', 'r').read())

for gene_entry in nci['GeneEntryCollection']['GeneEntry']:
    gene_name = gene_entry.get('HUGOGeneSymbol', '')
    if gene_name == 'ACSL5':
        print()
    gene_genbank = gene_entry.get('GenbankAccession', '')
    gene_refseq = gene_entry.get('RefSeqID', '')
    gene_uniprot = gene_entry.get('UniProtID', '')
    if type(gene_entry.get('Sentence', '')) == str:
        print()
    if gene_entry.get('Sentence', ''):
        for sentence in gene_entry['Sentence']:
            if sentence.get('Organism', '') == 'Human':
                cell_line = sentence.get('CellineIndicator', '')
                evidence = sentence.get('EvidenceCode', '')
                if type(evidence) == list:
                    evidence = ', '.join(evidence)

                drug_name = ''
                drug_concept = ''
                if sentence.get('DrugData', ''):
                    drug_name = sentence['DrugData'].get('DrugTerm', '')
                    drug_concept = sentence['DrugData'].get('NCIDrugConceptCode', '')

                gene_concept = ''
                if sentence.get('GeneData', ''):
                    gene_concept = sentence['GeneData'].get('NCIGeneConceptCode', '')

                role = ''
                if sentence.get('Roles', ''):
                    role = sentence['Roles'].get('PrimaryNCIRoleCode', '')
                    if type(role) == list:
                        role = ', '.join(role)
                    role = role.replace('_', ' ')

                sentence_status = sentence.get('SentenceStatusFlag').replace('_', ' ')

                with open('/home/maximk/Work/geroscope/nci_cancerindex/nci.tsv', 'a') as nci_result:
                    nci_result.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'
                                     % (drug_name, drug_concept, gene_name, gene_concept, role,
                                        gene_genbank, gene_refseq, gene_uniprot, cell_line, evidence, sentence_status))