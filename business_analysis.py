import sqlite3

DB_NAME = "stripe_analytics.db"

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()


print("\n========================================")
print("       STRIPE BUSINESS ANALYSIS")
print("========================================")


# --------------------------------------------------
# 1. Overall KPIs
# --------------------------------------------------

cursor.execute("""
SELECT
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_attempted_value,
    SUM(CASE WHEN status = 'succeeded' THEN 1 ELSE 0 END),
    SUM(CASE WHEN status = 'succeeded' THEN amount ELSE 0 END),
    SUM(CASE WHEN status != 'succeeded' THEN amount ELSE 0 END)
FROM payments;
""")

total, attempted_value, successful_count, successful_value, unsuccessful_value = cursor.fetchone()

success_rate = (successful_count / total) * 100

print("\n--- KEY PERFORMANCE INDICATORS ---")
print(f"Total transactions:        {total}")
print(f"Attempted payment value:   ${attempted_value:,.2f}")
print(f"Successful transactions:   {successful_count}")
print(f"Successful payment value:  ${successful_value:,.2f}")
print(f"Unsuccessful value:         ${unsuccessful_value:,.2f}")
print(f"Success rate:               {success_rate:.2f}%")


# --------------------------------------------------
# 2. Average and largest successful transaction
# --------------------------------------------------

cursor.execute("""
SELECT
    AVG(amount),
    MAX(amount),
    MIN(amount)
FROM payments
WHERE status = 'succeeded';
""")

avg_success, max_success, min_success = cursor.fetchone()

print("\n--- SUCCESSFUL TRANSACTIONS ---")
print(f"Average successful payment: ${avg_success:,.2f}")
print(f"Largest successful payment: ${max_success:,.2f}")
print(f"Smallest successful payment: ${min_success:,.2f}")


# --------------------------------------------------
# 3. Customer analysis
# --------------------------------------------------

print("\n--- CUSTOMER ANALYSIS ---")

cursor.execute("""
SELECT
    COALESCE(customer_id, 'Unknown') AS customer,
    COUNT(*) AS transactions,
    SUM(amount) AS total_value
FROM payments
GROUP BY customer_id
ORDER BY total_value DESC;
""")

for customer, transactions, total_value in cursor.fetchall():
    print(
        f"{customer:<30} "
        f"Transactions: {transactions:2} "
        f"Value: ${total_value:,.2f}"
    )


# --------------------------------------------------
# 4. Description / product analysis
# --------------------------------------------------

print("\n--- REVENUE BY DESCRIPTION ---")

cursor.execute("""
SELECT
    COALESCE(description, 'Unknown') AS description,
    COUNT(*) AS transactions,
    SUM(amount) AS total_value
FROM payments
WHERE status = 'succeeded'
GROUP BY description
ORDER BY total_value DESC;
""")

for description, transactions, total_value in cursor.fetchall():
    print(
        f"{description:<25} "
        f"Transactions: {transactions:2} "
        f"Value: ${total_value:,.2f}"
    )


# --------------------------------------------------
# 5. Failure analysis
# --------------------------------------------------

print("\n--- FAILURE ANALYSIS ---")

cursor.execute("""
SELECT
    COALESCE(failure_code, 'No failure code') AS failure_code,
    COUNT(*) AS transactions,
    SUM(amount) AS value
FROM payments
WHERE status != 'succeeded'
GROUP BY failure_code
ORDER BY value DESC;
""")

for failure_code, transactions, value in cursor.fetchall():
    print(
        f"{failure_code:<25} "
        f"Transactions: {transactions:2} "
        f"Value: ${value:,.2f}"
    )


connection.close()