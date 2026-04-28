from django.contrib import admin
from .models import Order, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "customer_name", "phone_number", "district", "thana", "total_price", "status", "created_at")
    search_fields = ("order_number", "customer_name", "phone_number", "district", "thana", "user__username")
    list_filter = ("status", "created_at")
