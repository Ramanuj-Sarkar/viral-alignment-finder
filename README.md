# About

Web front-end; two .html pages which query a MySQL database about seven human coronaviruses

"gene_finder.html"
* can show the organism names, gene names, product names, and product lengths in a table
* Multiple organisms can be selected, and the searches can be filtered using specific gene names and product names
* the names of each gene link to a NCBI page with more information.

"alignment_finder.html"
* finds the alignment between two products of genes
  * uses product names shown by gene_finder.html
* dynamically analyzes the alignment based on BioPython's blast-p alignment
* shows the number of alignments, the alignment score, and the length of the top alignment.

# Requirements

The tool requires either a SQL database named rsarkar6 or create privileges.

It requires the following Python libraries:
* Bio
* cgi
* json
* mysql.connector

# Detailed Usage

1. Use the text in the file "sql_data.txt" to create the databases.
2. Click on "gene_finder.html" or "alignment_finder.html".

# Folder-by-Folder Explanation

final
* css
  * "project.css" - contains css data for page
* gbfiles
  * "sql_data.txt" - the SQL data required in the file
  * "load_data.py" - Python file which can be used to recreate that file
  * "sequence0.gb" through "sequence6.gb" - the Genbank files used to obtain the data
* js
  * "project.js" - contains javascript to run projects
* "alignment_finder.cgi" - creates JSON for "alignment_finder.html"
* "alignment_finder.html" - finds alignment, as stated above
* "gene_finder.cgi" - creates JSON for "gene_finder.html"
* "gene_finder.html" - creates table, as stated above
* "final_narrative.pdf" - final project narrative
