import sqlite3

DB_NAME = "stripe_analytics.db"

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

print("\n--- PAYMENT SUMMARY ---")

cursor.execute("""
SELECT
    COUNT(*) AS total_payments,
    SUM(amount) AS total_value,
    AVG(amount) AS average_payment
FROM payments;
""")

summary = cursor.fetchone()

print(f"Total payments: {summary[0]}")
print(f"Total payment value: ${summary[1]:.2f}")
print(f"Average payment: ${summary[2]:.2f}")


print("\n--- PAYMENT STATUS ---")

cursor.execute("""
SELECT
    status,
    COUNT(*) AS payment_count,
    SUM(amount) AS total_value
FROM payments
GROUP BY status
ORDER BY total_value DESC;
""")

for row in cursor.fetchall():
    print(
        f"{row[0]:30} "
        f"Count: {row[1]:2} "
        f"Value: ${row[2]:.2f}"
    )


print("\n--- PAYMENT METHODS ---")

cursor.execute("""
SELECT
    payment_method_type,
    COUNT(*) AS payment_count,
    SUM(amount) AS total_value
FROM payments
GROUP BY payment_method_type
ORDER BY total_value DESC;
""")

for row in cursor.fetchall():
    method = row[0] or "Unknown"
    print(
        f"{method:15} "
        f"Count: {row[1]:2} "
        f"Value: ${row[2]:.2f}"
    )


print("\n--- DAILY PAYMENT TREND ---")

cursor.execute("""
SELECT
    DATE(created_at) AS payment_date,
    COUNT(*) AS payment_count,
    SUM(amount) AS total_value
FROM payments
GROUP BY DATE(created_at)
ORDER BY payment_date;
""")

for row in cursor.fetchall():
    print(
        f"{row[0]} "
        f"Count: {row[1]:2} "
        f"Value: ${row[2]:.2f}"
    )


connection.close()