import os
import csv
import stripe
from dotenv import load_dotenv
from datetime import datetime, timezone

# Load environment variables
load_dotenv()

# Get Stripe API key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

if not stripe.api_key:
    raise ValueError("STRIPE_SECRET_KEY not found in .env")

# Retrieve PaymentIntents
payment_intents = stripe.PaymentIntent.list(limit=100)

rows = []

for payment in payment_intents.data:

    payment_method_type = ""

    if payment.payment_method:
        try:
            payment_method = stripe.PaymentMethod.retrieve(
                payment.payment_method
            )
            payment_method_type = payment_method.type or ""
        except Exception:
            payment_method_type = ""

    failure_code = ""
    failure_message = ""

    if payment.last_payment_error:
        failure_code = payment.last_payment_error.code or ""
        failure_message = payment.last_payment_error.message or ""

    rows.append({
        "payment_id": payment.id,
        "amount": payment.amount / 100,
        "currency": payment.currency,
        "status": payment.status,
        "created_at": datetime.fromtimestamp(
            payment.created,
            tz=timezone.utc
        ).strftime("%Y-%m-%d %H:%M:%S"),
        "customer_id": payment.customer or "",
        "description": payment.description or "",
        "payment_method_type": payment_method_type,
        "capture_method": payment.capture_method or "",
        "confirmation_method": payment.confirmation_method or "",
        "livemode": payment.livemode,
        "receipt_email": payment.receipt_email or "",
        "cancellation_reason": payment.cancellation_reason or "",
        "failure_code": failure_code,
        "failure_message": failure_message
    })


fieldnames = [
    "payment_id",
    "amount",
    "currency",
    "status",
    "created_at",
    "customer_id",
    "description",
    "payment_method_type",
    "capture_method",
    "confirmation_method",
    "livemode",
    "receipt_email",
    "cancellation_reason",
    "failure_code",
    "failure_message"
]

with open(
    "stripe_payments.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Export complete: {len(rows)} payments exported.")
print("File created: stripe_payments.csv")