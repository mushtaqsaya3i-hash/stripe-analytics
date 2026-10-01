import sqlite3

DB_NAME = "stripe_analytics.db"

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

cursor.execute("DROP VIEW IF EXISTS payment_analysis")

cursor.execute("""
CREATE VIEW payment_analysis AS
SELECT
    payment_id,
    amount,
    currency,
    status,
    created_at,
    customer_id,

    CASE
        WHEN description LIKE 'Premium Order%' THEN 'Premium Order'
        WHEN description LIKE 'Online Purchase%' THEN 'Online Purchase'
        WHEN description LIKE 'Subscription%' THEN 'Subscription'
        WHEN description LIKE 'Sandbox Analytics Test%' THEN 'Sandbox Test'
        WHEN description = 'Declined Payment Test' THEN 'Declined Test'
        ELSE 'Unknown'
    END AS business_category,
CASE
    WHEN description LIKE 'Premium Order%' THEN 'Business'
    WHEN description LIKE 'Online Purchase%' THEN 'Business'
    WHEN description LIKE 'Subscription%' THEN 'Business'
    ELSE 'Test'
END AS transaction_type,

    payment_method_type,
    capture_method,
    confirmation_method,
    livemode,
    receipt_email,
    cancellation_reason,
    failure_code,
    failure_message

FROM payments;
""")

connection.commit()

print("Analytical view created successfully.")

# Verify the categories
cursor.execute("""
SELECT
    business_category,
    COUNT(*) AS transactions,
    SUM(amount) AS total_value
FROM payment_analysis
GROUP BY business_category
ORDER BY total_value DESC;
""")

print("\n--- BUSINESS CATEGORIES ---")

for category, transactions, value in cursor.fetchall():
    print(
        f"{category:<20} "
        f"Transactions: {transactions:2} "
        f"Value: ${value:,.2f}"
    )

connection.close()