__author__ = 'maximk'

#import xml.etree.ElementTree as etree
from lxml import etree

drugbank = etree.parse('/home/maximk/Work/geroscope/drugbank/single.xml')
drugs = drugbank.getroot()

def parse_pmids(pmid_line):
    papers = pmid_line.split(sep='\r\n')
    papers = [paper[-20:].split(sep='/')[-1] for paper in papers]
    return ', '.join(papers)

for drug in drugs:
    targets = []
    for drug_field in drug:
        name, cas, atc = '', '', ''
        if drug_field.tag == '{http://drugbank.ca}name':
            name = drug_field.text

        if drug_field.tag == '{http://drugbank.ca}cas-number':
            cas = drug_field.text

        if drug_field.tag == '{http://drugbank.ca}atc-codes':
            for atc in drug_field:
                if atc.tag == '{http://drugbank.ca}atc-code':
                    atc = drug_field.text
        ex_id_dict = dict()
        if drug_field.tag == '{http://drugbank.ca}external-identifiers':
            for ex_id in drug_field:
                if ex_id.tag == '{http://drugbank.ca}external-identifier':
                    in_tag = [tag for tag in ex_id]
                    ex_id_dict[in_tag[0].text] = in_tag[1].text
        chebi = ex_id_dict.get('ChEBI', '')
        pcid = ex_id_dict.get('PubChem Compound', '')
        psid = ex_id_dict.get('PubChem Substance', '')
        kegg = ex_id_dict.get('KEGG Drug', '')
        target_lines = []

        if drug_field.tag == '{http://drugbank.ca}targets':
            for target in drug_field:
                for target_field in target:
                    if target_field.tag == '{http://drugbank.ca}name':
                        target_name = target_field.text

                    if target_field.tag == '{http://drugbank.ca}organism':
                        organism = target_field.text

                    if target_field.tag == '{http://drugbank.ca}actions':
                        for action_field in target_field:
                            if action_field.tag == '{http://drugbank.ca}action':
                                action = action_field.text

                    if target_field.tag == '{http://drugbank.ca}references':
                        pmids = target_field.text
                        if pmids:
                            pmids = parse_pmids(pmids)

                    if target_field.tag == '{http://drugbank.ca}known-action':
                        ph_action = target_field.text

                    if target_field.tag == '{http://drugbank.ca}components':
                        for polypeptide in target_field:
                            for component_field in polypeptide:
                                if component_field.tag == '{http://drugbank.ca}gene-name':
                                    gene_name = component_field.text
                                if component_field.tag == '{http://drugbank.ca}external-identifiers':
                                    extern_line = ['']*3
                                    for extern_id in component_field:
                                        if extern_id[0].text == 'GenBank Gene Database':
                                            extern_line[0] = extern_id[1].text
                                        if extern_id[0].text == 'GenBank Protein Database':
                                            extern_line[1] = extern_id[1].text
                                        if extern_id[0].text == 'UniProtKB':
                                            extern_line[2] = extern_id[1].text
                                    t_external_ids = ';'.join(extern_line)
                target_lines.append('%s\t%s\t\t%s\t\t%s\t%s' % (action, ph_action, pmids, gene_name, target_name))
        for target_line in target_lines:
            if 'Human' in target_line:
                with open('/home/maximk/Work/geroscope/drugbank/single_out.tsv', 'a') as file:
                    file.write('%s\t\t%s\t%s\t\t%s\t%s\t%s\t\t%s\t%s\n' % (name, atc, cas, pcid, psid, chebi, kegg, target_line))