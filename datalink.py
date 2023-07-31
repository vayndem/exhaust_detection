import mysql.connector
import json

# create connection object
con = mysql.connector.connect(
    host="localhost", user="root",
    password="", database="knalpota")

# create cursor object
cursor = con.cursor()

# create database "knalpot" if not exists
create_database_query = '''
    CREATE DATABASE IF NOT EXISTS knalpota
'''
cursor.execute(create_database_query)

# select database "knalpot"
con.database = "knalpota"

# create table "data_knalpot" if not exists
create_table_query = '''
    CREATE TABLE IF NOT EXISTS data_knalpot (
        id INT AUTO_INCREMENT PRIMARY KEY,
        json_data TEXT,
        standar TEXT,
        non_standar TEXT
    )
'''
cursor.execute(create_table_query)

# close the cursor and connection
cursor.close()
con.close()
