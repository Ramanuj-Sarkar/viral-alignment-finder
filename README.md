# About

My main project consists of two html pages which query a MySQL database. Each of them make queries based on seven species of coronavirus which infect humans.

The first page, "gene_finder.html", can show the organism names, gene names, product names, and product lengths in a table using the data in these tables. Multiple organisms can be selected, and the searches can be filtered using specific gene names and product names. Additionally, the names of each gene link to a NCBI page with more information.

The second page, "alignment_finder.html", finds the alignment between two products of genes. It dynamically analyzes the alignment based on BioPython's blast-p alignment, showing the number of alignments, the alignment score, and the length of the top alignment.

Additionally, in the "gbfiles" folder, I have the files which can be used to create the database which the pages query. Specifically, it contains:

* "sql_data.txt" - the SQL data required in the file
* "load_data.py" - Python file which can be used to recreate that file
* "sequence0.gb" through "sequence6.gb" - the Genbank files used to obtain the data

# Requirements

The tool requires either a SQL database named rsarkar6 or create privileges.

It requires the following Python libraries:
* Bio
* cgi
* json
* mysql.connector

# Detailed Usage

Assuming this has never been run, and the goal is to use 


