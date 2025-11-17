from django.contrib import admin
from .models import Shopkeeper, Customer, Due

@admin.register(Shopkeeper)
class ShopkeeperAdmin(admin.ModelAdmin):
    list_display = ['shop_name', 'user', 'phone_number', 'created_at']
    search_fields = ['shop_name', 'user__username']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'shopkeeper', 'phone_number', 'created_at']
    list_filter = ['shopkeeper', 'created_at']
    search_fields = ['customer_name', 'phone_number']

@admin.register(Due)
class DueAdmin(admin.ModelAdmin):
    list_display = ['customer', 'amount', 'status', 'due_date', 'created_at']
    list_filter = ['status', 'due_date', 'created_at']
    search_fields = ['customer__customer_name', 'description']
