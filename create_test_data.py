import os
import stripe
from dotenv import load_dotenv

# --------------------------------------------------
# Load Stripe credentials
# --------------------------------------------------

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

if not stripe.api_key:
    raise ValueError("STRIPE_SECRET_KEY not found in .env")


# --------------------------------------------------
# Create test customers
# --------------------------------------------------

customers = []

customer_data = [
    ("Analytics Customer A", "customer.a@example.com"),
    ("Analytics Customer B", "customer.b@example.com"),
]

for name, email in customer_data:

    customer = stripe.Customer.create(
        name=name,
        email=email
    )

    customers.append(customer)

    print(
        f"Customer created: {customer.id} | {email}"
    )


# --------------------------------------------------
# Successful payments
# --------------------------------------------------

successful_payments = [
    (25, 0, "Online Purchase"),
    (40, 0, "Online Purchase"),
    (60, 1, "Subscription"),
    (85, 1, "Online Purchase"),
    (120, 0, "Subscription"),
    (150, 1, "Online Purchase"),
    (200, 0, "Premium Order"),
    (35, 1, "Online Purchase"),
    (75, 0, "Subscription"),
    (300, 1, "Premium Order"),
]


for amount, customer_index, description in successful_payments:

    payment_intent = stripe.PaymentIntent.create(
        amount=amount * 100,
        currency="usd",
        customer=customers[customer_index].id,
        payment_method="pm_card_visa",
        confirm=True,
        description=description,
        receipt_email=customers[customer_index].email,
        automatic_payment_methods={
            "enabled": True,
            "allow_redirects": "never",
        },
    )

    print(
        f"SUCCESS | "
        f"${amount:>3} | "
        f"{description:<20} | "
        f"{payment_intent.status:<20} | "
        f"{payment_intent.id}"
    )


# --------------------------------------------------
# Declined payments
# --------------------------------------------------

declined_payments = [
    (30, 0, "Declined Test"),
    (55, 1, "Declined Test"),
    (90, 0, "Declined Test"),
    (175, 1, "Declined Test"),
]


for amount, customer_index, description in declined_payments:

    payment_intent = stripe.PaymentIntent.create(
        amount=amount * 100,
        currency="usd",
        customer=customers[customer_index].id,
        payment_method="pm_card_chargeDeclined",
        confirm=True,
        description=description,
        automatic_payment_methods={
            "enabled": True,
            "allow_redirects": "never",
        },
    )

    print(
        f"DECLINED | "
        f"${amount:>3} | "
        f"{description:<20} | "
        f"{payment_intent.status:<20} | "
        f"{payment_intent.id}"
    )


print("\nControlled test dataset creation complete.")