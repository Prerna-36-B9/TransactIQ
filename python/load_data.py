import os
import json
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PG26@ss",
    database="transactiq_db"
)

cursor = conn.cursor()

# Path to your dataset
base_path = "../data/pulse/data/aggregated/transaction/country/india/state"

for state in os.listdir(base_path):
    state_path = os.path.join(base_path, state)
    
    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        
        for file in os.listdir(year_path):
            if file.endswith(".json"):
                quarter = int(file.replace(".json", ""))
                
                with open(os.path.join(year_path, file), 'r') as f:
                    data = json.load(f)

                    try:
                        for item in data['data']['transactionData']:
                            name = item['name']
                            count = item['paymentInstruments'][0]['count']
                            amount = item['paymentInstruments'][0]['amount']

                            cursor.execute("""
                                INSERT INTO aggregated_transaction 
                                (state, year, quarter, transaction_type, transaction_count, transaction_amount)
                                VALUES (%s, %s, %s, %s, %s, %s)
                            """, (state, int(year), quarter, name, count, amount))

                    except:
                        pass

conn.commit()
cursor.close()
conn.close()

print("Data loaded successfully!")