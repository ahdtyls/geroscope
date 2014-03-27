__author__ = 'maximk'

#import xml.etree.ElementTree as etree
from lxml import etree

drugbank = etree.parse('/home/maximk/Work/geroscope/drugbank/drugbank.xml')
drugs = drugbank.getroot()

for drug in drugs:
    drug_line = ['']*2
    targets = []
    for drug_field in drug:
        if drug_field.tag == '{http://drugbank.ca}drugbank-id':
            drug_line[0] = drug_field.text

        if drug_field.tag == '{http://drugbank.ca}name':
            drug_line[1] = drug_field.text

        if drug_field.tag == '{http://drugbank.ca}targets':
            for target in drug_field:
                target_line = ['']*6
                for target_field in target:
                    if target_field.tag == '{http://drugbank.ca}name':
                        target_line[0] = target_field.text

                    if target_field.tag == '{http://drugbank.ca}organism':
                        target_line[1] = target_field.text

                    if target_field.tag == '{http://drugbank.ca}actions':
                        for action_field in target_field:
                            if action_field.tag == '{http://drugbank.ca}action':
                                target_line[2] = action_field.text

                    if target_field.tag == '{http://drugbank.ca}known-action':
                        target_line[3] = target_field.text

                    if target_field.tag == '{http://drugbank.ca}components':
                        for polypeptide in target_field:
                            for component_field in polypeptide:
                                if component_field.tag == '{http://drugbank.ca}gene-name':
                                    target_line[4] = component_field.text
                                if component_field.tag == '{http://drugbank.ca}external-identifiers':
                                    extern_line = ['']*3
                                    for extern_id in component_field:
                                        if extern_id[0].text == 'GenBank Gene Database':
                                            extern_line[0] = extern_id[1].text
                                        if extern_id[0].text == 'GenBank Protein Database':
                                            extern_line[1] = extern_id[1].text
                                        if extern_id[0].text == 'UniProtKB':
                                            extern_line[2] = extern_id[1].text
                                    target_line[5] = ';'.join(extern_line)
                for i in range(len(target_line)):
                    if not target_line[i]:
                        target_line[i] = ''
                targets.append(target_line)
    with open('/home/maximk/Work/geroscope/drugbank/drugbank_out.csv', 'a') as file:
        file.write('%s;%s\n' % (';'.join(drug_line), '\n;;'.join(';'.join(line) for line in targets)))