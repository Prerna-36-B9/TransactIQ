import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PG26@ss",
    database="transactiq_db"
)

print("Connected successfully!")

query = """
SELECT year, SUM(transaction_amount) AS total_amount
FROM aggregated_transaction
GROUP BY year
ORDER BY year;
"""

df = pd.read_sql(query, conn)

plt.figure()
plt.plot(df['year'], df['total_amount'], marker='o')
plt.title("Yearly Transaction Trend")
plt.xlabel("Year")
plt.ylabel("Total Amount")
plt.grid()

plt.show()

query2 = """
SELECT state, SUM(transaction_amount) AS total_amount
FROM aggregated_transaction
GROUP BY state
ORDER BY total_amount DESC
LIMIT 10;
"""

df2 = pd.read_sql(query2, conn)

plt.figure()
plt.bar(df2['state'], df2['total_amount'])
plt.xticks(rotation=45)
plt.title("Top 10 States by Transaction Amount")
plt.xlabel("State")
plt.ylabel("Total Amount")

plt.show()

query3 = """
SELECT year, quarter, SUM(transaction_amount) AS total_amount
FROM aggregated_transaction
GROUP BY year, quarter
ORDER BY year, quarter;
"""

df3 = pd.read_sql(query3, conn)

plt.figure()
plt.plot(range(len(df3)), df3['total_amount'], marker='o')
plt.title("Quarterly Transaction Trend")
plt.xlabel("Time (Year-Quarter)")
plt.ylabel("Total Amount")

plt.show()