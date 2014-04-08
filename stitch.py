__author__ = 'maximk'

# mysql -uroot -p stitch --local-infile
# create table chemicals(chemical VARCHAR(127), name VARCHAR(255), molecular_weight VARCHAR(255), SMILES_string VARCHAR(255), primary key (chemical));
# LOAD DATA LOCAL INFILE '/home/maximk/Work/geroscope/stitch/actions.v3.1.tsv' INTO TABLE actions FIELDS TERMINATED BY '\t';
# create table actions(item_id_a VARCHAR(127), item_id_b VARCHAR(127), mode VARCHAR(255), action VARCHAR(255), a_is_acting int, score int, primary key(item_id_a));
# LOAD DATA LOCAL INFILE '/home/maximk/Work/geroscope/stitch/chemicals.v3.1.tsv' INTO TABLE chemicals FIELDS TERMINATED BY '\t';
# show table status from stitch;