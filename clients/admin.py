from django.contrib import admin
from .models import Order, Coupon, Review

# Register your models here.

#username:....admin password:...ym_fashionadmin


admin.site.register(Order)
admin.site.register(Coupon)
admin.site.register(Review)