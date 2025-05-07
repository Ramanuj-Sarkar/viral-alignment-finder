#!/usr/local/bin/python3

import cgi, json
import os
import mysql.connector

def main():
	print("Hello.")
	print("Content-Type: application/json\n\n")
	form = cgi.FieldStorage()

if __name__ == '__main__':
    main()
