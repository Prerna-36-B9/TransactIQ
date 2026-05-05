import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="TransactIQ", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #f8f9fa;
}
.block-container {
    padding-top: 2rem;
}
h1 {
    color: #6c5ce7;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DB CONNECTION ----------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PG26@ss",
    database="transactiq_db"
)

# ---------------- TITLE ----------------
st.title("💜 TransactIQ Dashboard")
st.caption("Decoding how India pays — patterns, behavior & growth insights 💜")
st.info("📊 Telangana leads in transaction value, while Maharashtra dominates in usage frequency — revealing distinct regional payment behaviors.")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Filters")

states = pd.read_sql("SELECT DISTINCT state FROM aggregated_transaction", conn)['state']
years = pd.read_sql("SELECT DISTINCT year FROM aggregated_transaction", conn)['year']

selected_state = st.sidebar.selectbox("Select State", ["All"] + list(states))
selected_year = st.sidebar.selectbox("Select Year", ["All"] + list(years))

# ---------------- FILTER FUNCTION ----------------
def apply_filters(base_query):
    if selected_state != "All":
        base_query += f" AND state = '{selected_state}'"
    if selected_year != "All":
        base_query += f" AND year = {selected_year}"
    return base_query

# ---------------- KPI CARDS ----------------
st.markdown("### 📌 Key Insights")

col1, col2 = st.columns(2)

query_total = "SELECT SUM(transaction_amount) as total FROM aggregated_transaction WHERE 1=1"
query_total = apply_filters(query_total)
total = pd.read_sql(query_total, conn)['total'][0]

query_top = """
SELECT state, SUM(transaction_amount) AS total
FROM aggregated_transaction WHERE 1=1
"""
query_top = apply_filters(query_top)
query_top += " GROUP BY state ORDER BY total DESC LIMIT 1"

top_state_df = pd.read_sql(query_top, conn)

with col1:
    st.metric("💰 Total Transaction Amount", f"{int(total):,}")

with col2:
    st.metric("🏆 Top State", top_state_df['state'][0])

st.markdown("---")

# ---------------- YEARLY TREND ----------------
query1 = """
SELECT year, SUM(transaction_amount) AS total_amount
FROM aggregated_transaction WHERE 1=1
"""
query1 = apply_filters(query1)
query1 += " GROUP BY year ORDER BY year"

df1 = pd.read_sql(query1, conn)

fig1 = px.line(df1, x='year', y='total_amount',
               title="Yearly Transaction Trend",
               markers=True)

# ---------------- TOP STATES ----------------
query2 = """
SELECT state, SUM(transaction_amount) AS total_amount
FROM aggregated_transaction WHERE 1=1
"""
query2 = apply_filters(query2)
query2 += " GROUP BY state ORDER BY total_amount DESC LIMIT 10"

df2 = pd.read_sql(query2, conn)

fig2 = px.bar(df2, x='state', y='total_amount',
              title="Top 10 States",
              text_auto=True)

# ---------------- QUARTERLY TREND ----------------
query3 = """
SELECT year, quarter, SUM(transaction_amount) AS total_amount
FROM aggregated_transaction WHERE 1=1
"""
query3 = apply_filters(query3)
query3 += " GROUP BY year, quarter ORDER BY year, quarter"

df3 = pd.read_sql(query3, conn)

df3['time'] = df3['year'].astype(str) + " Q" + df3['quarter'].astype(str)

fig3 = px.line(df3, x='time', y='total_amount',
               title="Quarterly Trend",
               markers=True)

# ---------------- TRANSACTION TYPE ----------------
query4 = """
SELECT transaction_type, SUM(transaction_count) AS total_count
FROM aggregated_transaction WHERE 1=1
"""
query4 = apply_filters(query4)
query4 += " GROUP BY transaction_type ORDER BY total_count DESC"

df4 = pd.read_sql(query4, conn)

fig4 = px.pie(df4, names='transaction_type', values='total_count',
              title="Transaction Type Distribution")

# ---------------- LAYOUT ----------------
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.plotly_chart(fig4, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("✨ Built with love using TransactIQ")