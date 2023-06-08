# import required modules 
import mysql.connector 
import json 
# create connection object 
con = mysql.connector.connect( 
host="localhost", user="root", 
password="", database="knalpor") 
 
# create cursor object 
cursor = con.cursor() 
 
create_table_query = ''' 
    CREATE TABLE IF NOT EXISTS check ( 
        id INT AUTO_INCREMENT PRIMARY KEY, 
        json_data TEXT 
    ) 
''' 
cursor.execute(create_table_query)
