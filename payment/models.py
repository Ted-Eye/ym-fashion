from django.db import models
from clients.models import Booking
# Create your models here.



class Payment(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "pending"), 
        ("SUCCESS", "success"),
        ("FAILED", "failed")
    ]
    reference = models.CharField(max_length=100, unique=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment", null=True)
    name = models.CharField(max_length=50, null=True, blank=False)
    phone = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reference