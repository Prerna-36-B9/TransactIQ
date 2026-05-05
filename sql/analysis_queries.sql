-- =========================================
-- Project: TransactIQ
-- Author: Prerna Gupta
-- Description: Data-driven analysis of digital payment behavior in India
-- =========================================
-- TransactIQ SQL Analysis
-- Understanding Digital Payment Behavior
-- =========================================

-- 1. Top States by Transaction Amount
-- Business Question: Which states generate the highest transaction value?

SELECT 
    state,
    SUM(transaction_amount) AS total_amount
FROM aggregated_transaction
GROUP BY state
ORDER BY total_amount DESC
LIMIT 10;


-- 2. Top States by Transaction Count
-- Business Question: Which states have highest user activity?

SELECT 
    state,
    SUM(transaction_count) AS total_count
FROM aggregated_transaction
GROUP BY state
ORDER BY total_count DESC
LIMIT 10;


-- 3. Transaction Type Distribution
-- Business Question: Which payment methods are most popular?

SELECT 
    transaction_type,
    SUM(transaction_count) AS total_transactions
FROM aggregated_transaction
GROUP BY transaction_type
ORDER BY total_transactions DESC;


-- 4. Yearly Growth Trend
-- Business Question: How are digital payments growing over time?

SELECT 
    year,
    SUM(transaction_amount) AS yearly_total
FROM aggregated_transaction
GROUP BY year
ORDER BY year;


-- 5. Quarterly Trend Analysis
-- Business Question: Is there any seasonal pattern in transactions?

SELECT 
    year,
    quarter,
    SUM(transaction_amount) AS total_amount
FROM aggregated_transaction
GROUP BY year, quarter
ORDER BY year, quarter;


-- 6. Top Performing State (Value)
-- Business Question: Which state leads in transaction value?

SELECT 
    state,
    SUM(transaction_amount) AS total
FROM aggregated_transaction
GROUP BY state
ORDER BY total DESC
LIMIT 1;


-- 7. Average Transaction Size by State
-- Business Question: Which states have higher-value transactions?

SELECT 
    state,
    SUM(transaction_amount)/SUM(transaction_count) AS avg_transaction_value
FROM aggregated_transaction
GROUP BY state
ORDER BY avg_transaction_value DESC
LIMIT 10;


-- 8. Total Platform Transaction Value
-- Business Question: What is the overall scale of transactions?

SELECT 
    SUM(transaction_amount) AS total_platform_value
FROM aggregated_transaction;