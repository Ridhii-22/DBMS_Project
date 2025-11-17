from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('customers/', views.customers_view, name='customers'),
    path('customers/add/', views.add_customer_view, name='add_customer'),
    path('customers/<int:customer_id>/', views.customer_detail_view, name='customer_detail'),
    path('customers/<int:customer_id>/add-due/', views.add_due_view, name='add_due'),
    path('dues/<int:due_id>/mark-paid/', views.mark_paid_view, name='mark_paid'),
]
