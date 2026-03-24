from django.db import models

# Create your models here.
class Payment(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "pending"), 
        ("SUCCESS", "success"),
        ("FAILED", "failed")
    ]
    reference = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reference