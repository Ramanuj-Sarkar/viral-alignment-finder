#!/usr/local/bin/python3

import cgi, json
import os
import mysql.connector

def main():
    print("Content-Type: application/json\n\n")
    form = cgi.FieldStorage()
    gene_term = form.getvalue('gene_search_term')
    product_term = form.getvalue('product_search_term')
    
    # records which columns are active
    col_int = 0
    
    col_list = ['organism', 'genename', 'productname', 'length']

    col_dict = {x: 'no' for x in col_list}
    
    # checks columns
    for x in range(len(col_list)):
        if form.getvalue(f'column{x}'):
            col_int += 2 ** x 
            col_dict[col_list[x]] = 'yes'

    # names in use
    which_list = []
    
    # the maximum number of files
    file_number = 99

    # organism list
    # the "file_number + 1" allows for 0 columns to be selected
    id_list = [f'{file_number+1}']

    # sets up json file
    results = {'columns': col_dict, 'match_count': 0, 'matches': which_list, 'misc': {'cols': col_int} }

    # makes sure all sequences are included
    # from html
    for x in range(file_number):
        if form.getvalue(f'sequence{x}'):
            id_list.append(f'{x}')

    id_string = '(' + ', '.join(id_list) + ')'

    # sql query data
    first_database = ''
    select_clause = ''
    from_clause = ''
    
    # query is different based on columns
    match col_int:
        case 1:
            select_clause += 'organism'
            from_clause += 'source'
            first_database += 'source'
        case 2:
            select_clause += 'genename'
            from_clause += 'gene'
            first_database += 'gene'
        case 3:
            select_clause += 'organism, genename'
            from_clause += 'source JOIN gene ON sourceid=geneid'
            first_database += 'source'
        case 4:
            select_clause += 'productname'
            from_clause += 'cds'
            first_database += 'cds'        
        case 5:
            select_clause += 'organism, productname'
            from_clause += 'source JOIN cds ON sourceid=cdsid'
            first_database += 'source'
        case 6:
            select_clause += 'genename, productname'
            from_clause += 'gene JOIN cds ON genename=relevantgene AND geneid=cdsid'
            first_database += 'gene'
        case 7:
            select_clause += 'organism, genename, productname'
            from_clause += 'source JOIN gene on sourceid=geneid JOIN cds ON genename=relevantgene AND geneid=cdsid'
            first_database += 'source'
        case 8:
            select_clause += 'length'
            from_clause += 'cds'
            first_database += 'cds'
        case 9:
            select_clause += 'organism, length'
            from_clause += 'source JOIN cds ON sourceid=cdsid'
            first_database += 'source'
        case 10:
            select_clause += 'genename, length'
            from_clause += 'gene JOIN cds ON genename=relevantgene AND geneid=cdsid'
            first_database += 'gene'
        case 11:
            select_clause += 'organism, genename, length'
            from_clause += 'source JOIN gene on sourceid=geneid JOIN cds ON genename=relevantgene AND geneid=cdsid'
            first_database += 'source'
        case 12:
            select_clause += 'productname, length'
            from_clause += 'cds'
            first_database += 'cds'
        case 13:
            select_clause += 'organism, productname, length'
            from_clause += 'source JOIN cds ON sourceid=cdsid'
            first_database += 'source'
        case 14:
            select_clause += 'genename, productname, length'
            from_clause += 'gene JOIN cds ON genename=relevantgene AND geneid=cdsid'
            first_database += 'gene'
        case 15:
            select_clause += 'organism, genename, productname, length'
            from_clause += 'source JOIN gene on sourceid=geneid JOIN cds ON genename=relevantgene AND geneid=cdsid'
            first_database += 'source'
        case _:
            first_database = 'source'
            select_clause = '*'
            from_clause = 'source'

    # this one doesn't change based on columns
    where_clause = f' {first_database}id IN ' +  id_string
    
    # stops errors based on queries
    if col_dict['genename'] == 'no':
        gene_term = None
    if col_dict['productname'] == 'no' and col_dict['length'] == 'no':
        product_term = None

    # start sql query
    conn = mysql.connector.connect(user='rsarkar6', password='Willtry3work?', host='localhost', database='rsarkar6')
    
    curs = conn.cursor()
    
    qry = 'SELECT ' + select_clause + ' FROM ' + from_clause + ' WHERE ' + where_clause
    
    # final query
    if gene_term is not None and product_term is not None:
        curs.execute(qry + "AND genename LIKE %s AND productname LIKE %s;", ('%' + gene_term + '%', '%' + product_term + '%'))
    elif gene_term is not None:
        curs.execute(qry + "AND genename LIKE %s;", ('%' + gene_term + '%',))
    elif product_term is not None:
        curs.execute(qry + 'AND productname LIKE %s;', ('%' + product_term + '%',))
    else:
        curs.execute(qry + ';')
    
    # makes sure each query element is in the correct column
    for x in curs:
        answer= {'organism': '', 'genename': '', 'productname': '', 'length': ''}
        position = 0

        if col_dict['organism'] == 'yes':
            answer['organism'] = x[position]
            position += 1

        if col_dict['genename'] == 'yes':
            answer['genename'] = x[position]
            position += 1

        if col_dict['productname'] == 'yes':
            answer['productname'] = x[position]
            position += 1

        if col_dict['length'] == 'yes':
            answer['length'] = x[position]
            position += 1

        which_list.append(answer)
        results['match_count'] += 1

    conn.close()

    # the json is complete
    print(json.dumps(results))

if __name__ == '__main__':
    main()
