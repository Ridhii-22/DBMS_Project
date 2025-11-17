from django.core.management.base import BaseCommand
from tracker.models import Shopkeeper, Customer, Due
import random
import string
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Seed database with sample data"

    def random_string(self, length=8):
        return ''.join(random.choices(string.ascii_letters, k=length))

    def random_phone(self):
        return ''.join(random.choices("0123456789", k=10))

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding 50 records...")

        # Create Shopkeepers
        shopkeepers = []
        for _ in range(5):
            sk = Shopkeeper.objects.create(
                shop_name="Shop " + self.random_string(5),
                phone_number=self.random_phone(),
            )
            shopkeepers.append(sk)

        # Create Customers
        customers = []
        for _ in range(50):
            cust = Customer.objects.create(
                customer_name="Customer " + self.random_string(4),
                phone_number=self.random_phone(),
                shopkeeper=random.choice(shopkeepers),
            )
            customers.append(cust)

        # Create Dues for each customer
        for c in customers:
            Due.objects.create(
                customer=c,
                amount=random.randint(50, 1000),
                due_date=datetime.now() - timedelta(days=random.randint(1, 30)),
                paid=random.choice([True, False]),
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded 50 records!"))
