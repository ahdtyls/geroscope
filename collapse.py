__author__ = 'maximk'


from lxml import etree


def drug_completeion(drugs):

    for drug in drugs:
        targets = []
        name, mechanism, = '', ''
        ex_id_dict = dict()
        for drug_field in drug:
            if drug_field.tag == '{http://drugbank.ca}name':
                name = drug_field.text


            if drug_field.tag == '{http://drugbank.ca}mechanism-of-action':
                mechanism = drug_field.text
                if mechanism:
                    mechanism = mechanism.replace('\r\n', ' ')


            if drug_field.tag == '{http://drugbank.ca}external-identifiers':
                ex_id_dict = dict()
                for ex_id in drug_field:
                    if ex_id.tag == '{http://drugbank.ca}external-identifier':
                        in_tag = [tag for tag in ex_id]
                        ex_id_dict[in_tag[0].text] = in_tag[1].text


            target_lines = []

            if drug_field.tag == '{http://drugbank.ca}targets':
                organism, ph_action = '', ''
                for target in drug_field:
                    action, pmids, gene_name, target_name, uniprot = '', '', '', '', ''
                    for target_field in target:
                        if target_field.tag == '{http://drugbank.ca}name':
                            target_name = target_field.text

                        if target_field.tag == '{http://drugbank.ca}known-action':
                            ph_action = target_field.text

                        if target_field.tag == '{http://drugbank.ca}organism':
                            organism = target_field.text

                        if target_field.tag == '{http://drugbank.ca}actions':
                            for action_field in target_field:
                                if action_field.tag == '{http://drugbank.ca}action':
                                    action = action_field.text


                        if target_field.tag == '{http://drugbank.ca}components':
                            for polypeptide in target_field:
                                for component_field in polypeptide:
                                    if component_field.tag == '{http://drugbank.ca}gene-name':
                                        gene_name = component_field.text
                                    if component_field.tag == '{http://drugbank.ca}external-identifiers':
                                        uniprot = []
                                        for extern_id in component_field:
                                            if extern_id[0].text == 'UniProtKB':
                                                uniprot.append(extern_id[1].text)
                                        uniprot = ', '.join(uniprot)
                    target_lines.append('%s\t%s\t\t%s\t\t%s\t%s\t\t\t%s\t' %
                                        (action, mechanism, pmids, gene_name, target_name, uniprot))
                if (organism == 'Human') and (ph_action == 'yes'):
                    for target_line in target_lines:
                        with open('/home/maximk/Work/geroscope/drugbank/drugbank.tsv', 'a') as file:
                            file.write('%s\t\t%s\t%s\t\t%s\t%s\t%s\t\t%s\t%s\n' %
                                       (name, target_line))
    return None

def target_completeion(drug_name):
    return None


def main():
    drug = open('/home/maximk/Work/geroscope/dtdb/drug.tsv', 'r')
    action = open('/home/maximk/Work/geroscope/dtdb/action.tsv', 'r')
    target = open('/home/maximk/Work/geroscope/dtdb/target.tsv', 'r')

    drugbank = etree.parse('/home/maximk/Work/geroscope/drugbank/drugbank.xml')
    drugs = drugbank.getroot()

    return None

if __name__ == 'main':
    main()