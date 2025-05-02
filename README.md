# About

Compares viral genomes.

* rhinovirus B14: https://www.ncbi.nlm.nih.gov/protein/NP_041009.1?report=fasta
* 

# Requirements

# Detailed Usage

<!--
This project is from Ramanuj Sarkar for Spring 2025 at JHU for AS.410.712.

This browsing tool allows people to analyze and interrogate the DNA of different coronaviruses, such as the common cold virus and CoViD-19.

The user is shown an HTML page, and they select which organisms to see data from using a series of radio buttons, with the option to view data from all organisms. Then, they can choose to search using either the names or the descriptions of genes. After this, they can choose to search using specific names or specific words in the descriptions of the genes.

All of these choices are to construct a SQL query made using a CGI file which uses mysql.connector to connect to a MySQL library which already has the data from NCBI. The data in this case uses a data scheme which resembles Chado in order to effectively store and query this data using MySQL queries. The resulting table would then be passed back to the client side as a JSON dump in order to create a table which can then be displayed to the user.

The user is able to focus on only specific columns.
-->

