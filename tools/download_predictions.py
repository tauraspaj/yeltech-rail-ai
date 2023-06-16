import csv
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# connect to the database
db_connection = mysql.connector.connect(
    host=os.getenv('DB_ENDPOINT'),
    user=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    database='yeltech_ai_db'
)

# query the database and get the results
query = 'SELECT * FROM predictions'

cursor = db_connection.cursor()
cursor.execute(query)
results = cursor.fetchall()

# save results to a csv
with open("tmp_prediction_analysis.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(results)
