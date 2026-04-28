from django.conf import settings
from django.db import models
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    order_number = models.CharField(max_length=30, unique=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    customer_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20)
    district = models.CharField(max_length=80)
    thana = models.CharField(max_length=80)
    address = models.TextField()
    items = models.JSONField(default=list)
    total_price = models.PositiveIntegerField()
    status = models.CharField(max_length=30, default="Confirmed")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            next_id = (Order.objects.order_by("-id").first().id + 1) if Order.objects.exists() else 1
            self.order_number = f"ORD-{timestamp}-{next_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number
