"""
Synthetic data generator for AgentGuard simulations.
ALL data is 100% synthetic — no real payment data.
"""
import random
import uuid
from datetime import datetime, timedelta
from decimal import Decimal

FIRST_NAMES = [
    "Aarav", "Priya", "Vivaan", "Ananya", "Aditya", "Meera", "Arjun", "Diya",
    "Kabir", "Ishita", "Rohan", "Saanvi", "Siddharth", "Neha", "Vikram", "Pooja",
    "Rajesh", "Nandini", "Amit", "Kavya", "Suresh", "Tara", "Manoj", "Riya",
    "Dev", "Zara", "Kartik", "Simran", "Harsh", "Lakshmi"
]

LAST_NAMES = [
    "Sharma", "Patel", "Singh", "Kumar", "Gupta", "Jain", "Reddy", "Nair",
    "Mehta", "Malhotra", "Choudhary", "Verma", "Kapoor", "Iyer", "Mishra",
    "Agarwal", "Banerjee", "Das", "Shah", "Desai", "Bhat", "Rao", "Pillai",
    "Chatterjee", "Kohli", "Sethi", "Joshi", "Trivedi", "Pandit", "Saxena"
]

RISK_LEVELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
RISK_WEIGHTS = [0.30, 0.35, 0.25, 0.10]


def generate_customers(n: int, rng: random.Random) -> list[dict]:
    """Generate n synthetic customers."""
    customers = []
    for i in range(n):
        first = rng.choice(FIRST_NAMES)
        last = rng.choice(LAST_NAMES)
        cid = f"CUS-{1000 + i}"
        # Lifetime value between 5k and 5L
        value = round(rng.uniform(5000, 500000), 2)
        # 10% opt-out rate
        opt_out = rng.random() < 0.10
        prev_payments = rng.randint(0, 15)
        # Last contact: random 0-72 hours ago, or None
        has_contact = rng.random() < 0.6
        last_contact = (
            datetime.utcnow() - timedelta(hours=rng.uniform(1, 72))
            if has_contact
            else None
        )

        customers.append({
            "id": str(uuid.uuid4()),
            "customer_id": cid,
            "name": f"{first} {last}",
            "email": f"{first.lower()}.{last.lower()}{rng.randint(1,99)}@example.com",
            "customer_value": Decimal(str(value)),
            "opt_out": opt_out,
            "previous_successful_payments": prev_payments,
            "last_contact_at": last_contact,
            "created_at": datetime.utcnow() - timedelta(days=rng.randint(30, 365)),
        })
    return customers


def generate_transactions(customers: list[dict], n: int, rng: random.Random) -> list[dict]:
    """Generate n synthetic failed transactions across the customers."""
    transactions = []
    for i in range(n):
        customer = rng.choice(customers)
        tid = f"TXN-{10000 + i}"
        # Amount: Rs. 500 to Rs. 1,50,000
        amount = round(rng.uniform(500, 150000), 2)
        retry_count = rng.choices([0, 1, 2, 3], weights=[0.4, 0.3, 0.2, 0.1])[0]
        risk = rng.choices(RISK_LEVELS, weights=RISK_WEIGHTS)[0]
        prob = round(rng.uniform(0.1, 0.95), 2)
        # Intervention cost scales with amount
        intervention_cost = round(amount * rng.uniform(0.02, 0.08), 2)

        transactions.append({
            "id": str(uuid.uuid4()),
            "transaction_id": tid,
            "customer_id": customer["customer_id"],
            "amount": Decimal(str(amount)),
            "currency": "INR",
            "status": "FAILED",
            "retry_count": retry_count,
            "recovery_probability": prob,
            "intervention_cost": Decimal(str(intervention_cost)),
            "risk_level": risk,
            "created_at": datetime.utcnow() - timedelta(hours=rng.uniform(1, 48)),
            "updated_at": datetime.utcnow(),
        })
    return transactions
