import os
from dotenv import load_dotenv
import stripe

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

payment_intents = stripe.PaymentIntent.list(limit=10)

print(f"Connected to Stripe successfully!")
print(f"PaymentIntents found: {len(payment_intents.data)}")

for payment in payment_intents.data:
    print(
        payment.id,
        payment.amount,
        payment.currency,
        payment.status
    )