from django.db import models
from django.utils import timezone
from datetime import timedelta
from catalog.models import Hairstyle

# Create your models here.

class Order(models.Model):
    style = models.ForeignKey(Hairstyle, on_delete=models.CASCADE)
    client = models.CharField(max_length=100)
    tel = models.IntegerField()
    address = models.CharField(max_length=100, blank=True)
    schedule_date = models.DateTimeField(blank=False)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.client
    

class Coupon(models.Model):
    bearer = models.CharField(max_length=100, verbose_name='client')
    tel = models.IntegerField()
    value = models.ForeignKey(Hairstyle, on_delete=models.CASCADE)
    issued_on = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateTimeField(blank=True, null=True)

#  OVERRIDE THE SAVE METHOD AND USE TIMEDELTA TO AUTOMATICALLY SET EXPIRY DATE, COUNTING FROM THE ISSUED DATE
    def save(self, *args, **kwargs):
        if not self.expires_on:
            self.expires_on = timezone.now() + timedelta(days=30)

    def __str__(self):
        return self.bearer


class Review(models.Model):
    client = models.CharField(max_length=100, verbose_name='author')
    comment = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='uploads/images', blank=True)

    def __str__(self):
        return self.client