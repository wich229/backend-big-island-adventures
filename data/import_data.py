import csv
import psycopg2
  
conn = psycopg2.connect(database="touring_api_development",
                        user='postgres',host='127.0.0.1', port='5432'
)
  
conn.autocommit = True
cursor = conn.cursor()
  
  
# sql = '''CREATE TABLE tours_data_testing(id INT PRIMARY KEY, name TEXT,\
# city CHAR(20), address VARCHAR(200), date DATE, duration_in_min INT, price FLOAT(4), category CHAR(40), is_outdoor BOOLEAN NOT NULL,\
# capacity INT, description TEXT);'''

with open('./data/tours_data_testing.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header row.
    for row in reader:
        cursor.execute(
        "INSERT INTO tour VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        row
    )
    #other way-----------------------------------------------
    # next(f) # Skip the header row.
    # cursor.copy_from(f, 'tour', sep=',')
    f.close()
    
conn.commit()

cursor.execute()
all = cursor.fetchall()

