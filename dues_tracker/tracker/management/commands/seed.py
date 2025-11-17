import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from tracker.models import Shopkeeper, Customer, Due


FIRST_NAMES = ["Rohan", "Priya", "Amit", "Neha", "Arjun", "Simran", "Karan", "Pooja", "Vikram", "Ritu"]

SHOP_NAMES = [
    "General Store", "Super Mart", "Daily Needs", "Fresh Mart",
    "City Store", "Quick Shop", "Family Mart", "Local Bazaar",
    "Budget Store", "Mega Mart"
]

DUE_DESCRIPTIONS = [
    "Milk and bread", "Snacks purchase", "Monthly grocery",
    "Cold drinks", "Household items", "Stationery",
    "Biscuits and chips", "Sugar and tea", "Cleaning supplies", "Cooking essentials"
]


class Command(BaseCommand):
    help = "Seed database with shopkeepers, customers, and dues"

    def handle(self, *args, **options):

        # ---------- CREATE ADMIN ----------
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                password="admin123"
            )
            self.stdout.write(self.style.SUCCESS("Admin created: admin / admin123"))
        else:
            self.stdout.write("Admin already exists")

        # ---------- CREATE SHOPKEEPERS ----------
        for i, first in enumerate(FIRST_NAMES, start=1):

            username = f"{first.lower()}{i}"     # e.g. rohan1, priya2, amit3...

            # Prevent duplicate username error
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f"Skipping existing user: {username}"))
                continue

            # Create user
            user = User.objects.create_user(
                username=username,
                password="password123",
                first_name=first
            )

            # Create shopkeeper
            shopkeeper = Shopkeeper.objects.create(
                user=user,
                shop_name=random.choice(SHOP_NAMES) + f" {i}",
                phone_number=f"98765{random.randint(10000, 99999)}",
                address=f"Street {random.randint(1, 50)}, City {random.randint(1, 5)}"
            )

            # ---------- CREATE CUSTOMERS ----------
            for j in range(5):
                cname = FIRST_NAMES[j]     # Fixed name list

                customer = Customer.objects.create(
                    shopkeeper=shopkeeper,
                    customer_name=cname,
                    phone_number=f"99887{random.randint(10000, 99999)}",
                    address=f"Area {random.randint(1, 20)}, Block {random.randint(1, 10)}"
                )

                # ---------- CREATE DUES ----------
                for k in range(3):

                    due_date = datetime.now().date() - timedelta(days=random.randint(1, 60))
                    amount = round(random.uniform(50, 500), 2)

                    Due.objects.create(
                        customer=customer,
                        amount=amount,
                        description=random.choice(DUE_DESCRIPTIONS),
                        due_date=due_date,
                        status=random.choice(["PENDING", "PAID"])
                    )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
