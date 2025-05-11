#!/usr/local/bin/python3

import cgi, json
import os
import mysql.connector
from Bio import Align

def main():
    print("Content-Type: application/json\n\n")
    form = cgi.FieldStorage()
    first_radio = form.getvalue("first_radio")
    first_product = form.getvalue("first_product")
    second_radio = form.getvalue("second_radio")
    second_product = form.getvalue('second_product')

    results = {'error': '', 'align': '', 'align_count': 0, 'align_score': 0.0}
    
    # checks simple errors
    if first_radio is None or second_radio is None:
        results['error'] += 'You have to select one from both sets of buttons.'
        print(json.dumps(results))
        return

    if first_product is None or second_product is None:
        results['error'] += 'You have to fill out both products.'
        print(json.dumps(results))
        return
    
    # get sql data
    conn = mysql.connector.connect(user='rsarkar6', password='Willtry3work?', host='localhost', database='rsarkar6')

    curs = conn.cursor()

    qry1 = 'SELECT translation FROM cds WHERE cdsid = %s AND productname = %s;'

    # get first one
    curs.execute(qry1, (int(first_radio[-1]), first_product, ))

    answer_num = 0
    
    first_translation = ''
    
    # check to see there's only one answer, since there should only be one
    for x in curs:
        first_translation += x[0]
        answer_num += 1
    
    # even if there are more answers, there should only be one
    if answer_num != 1:
        results['error'] += f'It\'s likely the first product is incorrect - there were {answer_num} answers.'
        print(json.dumps(results))
        return
    
    # repeat with second one
    qry2 = 'SELECT translation FROM cds WHERE cdsid = %s AND productname = %s;'

    curs.execute(qry2, (int(second_radio[-1]), second_product, ))
    
    answer_num = 0

    second_translation = ''
    
    for x in curs:
        second_translation = x[0]
        answer_num += 1

    if answer_num != 1:
        results['error'] += f'It\'s likely the second product is incorrect - there were {answer_num} answers.'
        print(json.dumps(results))
        return

    conn.close()
    
    # do alignment procedure
    aligner = Align.PairwiseAligner(scoring='blastp')
    alignments = aligner.align(first_translation, second_translation)
    
    shaped = alignments[0].shape

    # put results in json
    results['align_count'] += len(alignments)
    results['align_score'] += alignments.score
    results['error'] += 'No errors detected.'
    results['align'] += f"{shaped[1]}"

    print(json.dumps(results))

if __name__ == '__main__':
    main()
