from django.db import models
from django.contrib.auth.models import User

class Shopkeeper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.shop_name} - {self.user.username}"

    class Meta:
        db_table = 'shopkeepers'

class Customer(models.Model):
    shopkeeper = models.ForeignKey(Shopkeeper, on_delete=models.CASCADE, related_name='customers')
    customer_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name

    def total_dues(self):
        return self.dues.filter(status='PENDING').aggregate(models.Sum('amount'))['amount__sum'] or 0

    class Meta:
        db_table = 'customers'

class Due(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='dues')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.customer_name} - ₹{self.amount} - {self.status}"

    class Meta:
        db_table = 'dues'
        ordering = ['-created_at']
