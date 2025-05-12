#!/usr/local/bin/python3

from Bio import SeqIO

# deletes old tables
# creates new tables
def starting():
    start_thing = '''CREATE DATABASE IF NOT EXISTS rsarkar6;

USE rsarkar6;

DROP TABLE IF EXISTS source;
DROP TABLE IF EXISTS gene;
DROP TABLE IF EXISTS cds;

CREATE TABLE source(
    sourceid INT,
    organism VARCHAR(64)
);

CREATE TABLE gene(
        geneid INT,
        genename VARCHAR(64)
);

CREATE TABLE cds(
        cdsid INT,
        relevantgene VARCHAR(64) NULL,
        productname VARCHAR(64),
        length INT,
        translation TEXT
);

'''

    return start_thing

# populates new tables with Genbank data
def bio_genebank(rec, idnum):
    statements = []

    for feature in rec.features:
        if feature.type in ['source', 'gene', 'CDS']:
            if feature.type == 'CDS':
                relevant = ''
                if 'gene' in feature.qualifiers:
                    relevant += f"'{feature.qualifiers['gene'][0]}'"
                else:
                    relevant += 'NULL'

                statements.append(f"INSERT INTO cds VALUES ({idnum}, {relevant}, '{feature.qualifiers['product'][0]}', {len(feature.qualifiers['translation'][0])}, '{feature.qualifiers['translation'][0]}' );")
            elif feature.type == 'source':
                statements.append(f"INSERT INTO source VALUES ({idnum}, '{feature.qualifiers['organism'][0]}');")
            elif feature.type == 'gene':
                statements.append(f"INSERT INTO gene VALUES ({idnum}, '{feature.qualifiers['gene'][0]}');")
    
    return statements


# consolidates data to create and populate new tables
# using mysql.connector doesn't work
def main():
    starting_statement = starting()
    
    check_exception = '';

    insertion_list = []
    try:
        number_checker = 0
        
        while True:

            record = SeqIO.read(f"sequence{number_checker}.gb", "genbank")

            insertion_list += bio_genebank(record, number_checker)

            number_checker += 1
    except Exception as e:
        check_exception += "This breaks the loop, basically."
    
    # saves data in sql_data.txt
    with open('sql_data.txt', 'w+') as sqldata:
        sqldata.write(starting_statement)
        for statement in insertion_list:
            sqldata.write(statement + '\n')


if __name__ == '__main__':
    main()
