import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- DATABASE CONNECTION ----------------

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PG26@ss",
    database="transactiq_db"
)

# ---------------- 1. TOP STATES BY TRANSACTION AMOUNT ----------------

query1 = """
SELECT state, SUM(transaction_amount) AS total_amount
FROM aggregated_transaction
GROUP BY state
ORDER BY total_amount DESC
LIMIT 10;
"""

df1 = pd.read_sql(query1, conn)

plt.figure(figsize=(10,5))
plt.bar(df1['state'], df1['total_amount'])
plt.title("Top States by Transaction Amount")
plt.xlabel("State")
plt.ylabel("Transaction Amount")
plt.xticks(rotation=45)
plt.show()

# ---------------- 2. TOP STATES BY TRANSACTION COUNT ----------------

query2 = """
SELECT state, SUM(transaction_count) AS total_count
FROM aggregated_transaction
GROUP BY state
ORDER BY total_count DESC
LIMIT 10;
"""

df2 = pd.read_sql(query2, conn)

plt.figure(figsize=(10,5))
plt.bar(df2['state'], df2['total_count'])
plt.title("Top States by Transaction Count")
plt.xlabel("State")
plt.ylabel("Transaction Count")
plt.xticks(rotation=45)
plt.show()

# ---------------- 3. TRANSACTION TYPE DISTRIBUTION ----------------

query3 = """
SELECT transaction_type, SUM(transaction_count) AS total_transactions
FROM aggregated_transaction
GROUP BY transaction_type
ORDER BY total_transactions DESC;
"""

df3 = pd.read_sql(query3, conn)

plt.figure(figsize=(8,8))
plt.pie(
    df3['total_transactions'],
    labels=df3['transaction_type'],
    autopct='%1.1f%%'
)

plt.title("Transaction Type Distribution")
plt.show()

# ---------------- 4. YEARLY GROWTH TREND ANALYSIS ----------------

query4 = """
SELECT year, SUM(transaction_amount) AS yearly_total
FROM aggregated_transaction
GROUP BY year
ORDER BY year;
"""

df4 = pd.read_sql(query4, conn)

plt.figure(figsize=(10,5))
plt.plot(df4['year'], df4['yearly_total'], marker='o')
plt.title("Yearly Growth Trend")
plt.xlabel("Year")
plt.ylabel("Transaction Amount")
plt.grid(True)
plt.show()

# ---------------- 5. QUARTERLY TREND ANALYSIS ----------------

query5 = """
SELECT year, quarter, SUM(transaction_amount) AS total_amount
FROM aggregated_transaction
GROUP BY year, quarter
ORDER BY year, quarter;
"""

df5 = pd.read_sql(query5, conn)

df5['Time'] = df5['year'].astype(str) + " Q" + df5['quarter'].astype(str)

plt.figure(figsize=(12,5))
plt.plot(df5['Time'], df5['total_amount'], marker='o')
plt.title("Quarterly Transaction Trend")
plt.xlabel("Quarter")
plt.ylabel("Transaction Amount")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# ---------------- CLOSE CONNECTION ----------------

conn.close()