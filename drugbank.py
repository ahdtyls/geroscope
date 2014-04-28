__author__ = 'maximk'

#import xml.etree.ElementTree as etree
from lxml import etree

drugbank = etree.parse('/home/maximk/Work/geroscope/drugbank/single.xml')
drugs = drugbank.getroot()

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

        if drug_field.tag == '{http://drugbank.ca}external-identifiers':
            ex_ids = [ex_id for ex_id in drug_field]
            for ex_id in ex_ids:
                if ex_id.tag == '{http://drugbank.ca}external-identifier':
                    print()
                    # if ex_id.text == 'ChEBI':
                    #
                    # if ex_id.text == 'PubChem Compound':
                    #
                    # if ex_id.text == 'PubChem Substance':
                    #
                    # if ex_id.text == 'KEGG Drug':
                    #
                    # if ex_id.text == 'PharmGKB':

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
                targets.append(target_line)
    with open('/home/maximk/Work/geroscope/drugbank/single_out.csv', 'a') as file:
        file.write('%s;%s;%s;%s\n' % (name, cas, atc, '\n;;'.join(';'.join(line) for line in targets)))