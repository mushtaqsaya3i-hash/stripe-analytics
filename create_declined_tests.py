import os
import stripe
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

if not stripe.api_key:
    raise ValueError("STRIPE_SECRET_KEY not found in .env")


# Create one test customer
customer = stripe.Customer.create(
    name="Declined Payment Test Customer",
    email="declined.test@example.com"
)

print(f"Customer created: {customer.id}")


# Stripe test card that produces a decline
declined_payments = [
    30,
    55,
    90,
    175
]


for amount in declined_payments:

    try:

        payment_intent = stripe.PaymentIntent.create(
            amount=amount * 100,
            currency="usd",
            customer=customer.id,
            payment_method="pm_card_chargeDeclined",
            confirm=True,
            description="Declined Payment Test",
            automatic_payment_methods={
                "enabled": True,
                "allow_redirects": "never",
            },
        )

        print(
            f"${amount:>3} | "
            f"{payment_intent.status} | "
            f"{payment_intent.id}"
        )

    except stripe.CardError:

        print(
            f"${amount:>3} | "
            f"card_declined | "
            f"Decline recorded as expected"
        )


print("\nDeclined test creation complete.")