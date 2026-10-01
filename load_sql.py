import sqlite3
import csv

DB_NAME = "stripe_analytics.db"
CSV_FILE = "stripe_payments.csv"

# Connect to SQLite database
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

# Create payments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS payments (
    payment_id TEXT PRIMARY KEY,
    amount REAL,
    currency TEXT,
    status TEXT,
    created_at TEXT,
    customer_id TEXT,
    description TEXT,
    payment_method_type TEXT,
    capture_method TEXT,
    confirmation_method TEXT,
    livemode BOOLEAN,
    receipt_email TEXT,
    cancellation_reason TEXT,
    failure_code TEXT,
    failure_message TEXT
)
""")

# Load CSV
with open(CSV_FILE, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute("""
        INSERT OR REPLACE INTO payments (
            payment_id,
            amount,
            currency,
            status,
            created_at,
            customer_id,
            description,
            payment_method_type,
            capture_method,
            confirmation_method,
            livemode,
            receipt_email,
            cancellation_reason,
            failure_code,
            failure_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["payment_id"],
            row["amount"],
            row["currency"],
            row["status"],
            row["created_at"],
            row["customer_id"],
            row["description"],
            row["payment_method_type"],
            row["capture_method"],
            row["confirmation_method"],
            row["livemode"],
            row["receipt_email"],
            row["cancellation_reason"],
            row["failure_code"],
            row["failure_message"]
        ))

connection.commit()

# Check number of records
cursor.execute("SELECT COUNT(*) FROM payments")
count = cursor.fetchone()[0]

print(f"SQL database created successfully.")
print(f"Payments loaded: {count}")

connection.close()