import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="TransactIQ Dashboard",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.main {
    background-color: #f8f9fa;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1 {
    color: #6C5CE7;
    font-weight: 700;
}

[data-testid="metric-container"] {
    background-color: white;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# ---------------- DATABASE CONNECTION ----------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PG26@ss",
    database="transactiq_db"
)

# ---------------- TITLE ----------------
st.title("💜 TransactIQ Dashboard")

st.caption(
    "Decoding how India pays — patterns, behavior & growth insights 💜"
)

st.info(
    "📊 Telangana leads in transaction value, while Maharashtra dominates in transaction frequency."
)

# ---------------- SIDEBAR ----------------
st.sidebar.header("🎛️ Filters")

states = pd.read_sql(
    "SELECT DISTINCT state FROM aggregated_transaction",
    conn
)['state']

years = pd.read_sql(
    "SELECT DISTINCT year FROM aggregated_transaction",
    conn
)['year']

selected_state = st.sidebar.selectbox(
    "Select State",
    ["All"] + list(states)
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + list(years)
)

# ---------------- FILTER FUNCTION ----------------
def apply_filters(query):

    if selected_state != "All":
        query += f" AND state = '{selected_state}'"

    if selected_year != "All":
        query += f" AND year = {selected_year}"

    return query

# ---------------- KPI SECTION ----------------
st.markdown("## 📌 Key Insights")

col1, col2 = st.columns(2)

# Total Transaction Amount
query_total = """
SELECT SUM(transaction_amount) AS total
FROM aggregated_transaction
WHERE 1=1
"""

query_total = apply_filters(query_total)

total_amount = pd.read_sql(query_total, conn)['total'][0]

# Top State
query_top_state = """
SELECT state, SUM(transaction_amount) AS total
FROM aggregated_transaction
WHERE 1=1
"""

query_top_state = apply_filters(query_top_state)

query_top_state += """
GROUP BY state
ORDER BY total DESC
LIMIT 1
"""

top_state_df = pd.read_sql(query_top_state, conn)

with col1:
    st.metric(
        "💰 Total Transaction Amount",
        f"{int(total_amount):,}"
    )

with col2:
    st.metric(
        "🏆 Top State",
        top_state_df['state'][0]
    )

st.markdown("---")

# =====================================================
# 1. TOP STATES BY TRANSACTION AMOUNT
# =====================================================

query1 = """
SELECT state, SUM(transaction_amount) AS total_amount
FROM aggregated_transaction
WHERE 1=1
"""

query1 = apply_filters(query1)

query1 += """
GROUP BY state
ORDER BY total_amount DESC
LIMIT 10
"""

df1 = pd.read_sql(query1, conn)

fig1 = px.bar(
    df1,
    x='state',
    y='total_amount',
    title="📍 Top States by Transaction Amount",
    text_auto=True
)

# =====================================================
# 2. TOP STATES BY TRANSACTION COUNT
# =====================================================

query2 = """
SELECT state, SUM(transaction_count) AS total_count
FROM aggregated_transaction
WHERE 1=1
"""

query2 = apply_filters(query2)

query2 += """
GROUP BY state
ORDER BY total_count DESC
LIMIT 10
"""

df2 = pd.read_sql(query2, conn)

fig2 = px.bar(
    df2,
    x='state',
    y='total_count',
    title="📊 Top States by Transaction Count",
    text_auto=True
)

# =====================================================
# 3. TRANSACTION TYPE DISTRIBUTION
# =====================================================

query3 = """
SELECT transaction_type,
SUM(transaction_count) AS total_transactions
FROM aggregated_transaction
WHERE 1=1
"""

query3 = apply_filters(query3)

query3 += """
GROUP BY transaction_type
ORDER BY total_transactions DESC
"""

df3 = pd.read_sql(query3, conn)

fig3 = px.pie(
    df3,
    names='transaction_type',
    values='total_transactions',
    title="💳 Transaction Type Distribution"
)

# =====================================================
# 4. YEARLY GROWTH TREND
# =====================================================

query4 = """
SELECT year,
SUM(transaction_amount) AS yearly_total
FROM aggregated_transaction
WHERE 1=1
"""

query4 = apply_filters(query4)

query4 += """
GROUP BY year
ORDER BY year
"""

df4 = pd.read_sql(query4, conn)

fig4 = px.line(
    df4,
    x='year',
    y='yearly_total',
    title="📈 Yearly Growth Trend",
    markers=True
)

# =====================================================
# 5. QUARTERLY TREND ANALYSIS
# =====================================================

query5 = """
SELECT year,
quarter,
SUM(transaction_amount) AS total_amount
FROM aggregated_transaction
WHERE 1=1
"""

query5 = apply_filters(query5)

query5 += """
GROUP BY year, quarter
ORDER BY year, quarter
"""

df5 = pd.read_sql(query5, conn)

df5['Time'] = (
    df5['year'].astype(str)
    + " Q"
    + df5['quarter'].astype(str)
)

fig5 = px.line(
    df5,
    x='Time',
    y='total_amount',
    title="📅 Quarterly Trend Analysis",
    markers=True
)

# ---------------- DASHBOARD LAYOUT ----------------

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

st.markdown("## 📈 Seasonal & Quarterly Analysis")

st.plotly_chart(fig5, use_container_width=True)

# ---------------- FOOTER ----------------

st.markdown("---")

st.caption("✨ Built by Prerna Gupta | TransactIQ")