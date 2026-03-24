from django.contrib import admin
from .models import Booking, Coupon, Review

# Register your models here.

#username:....admin password:...ym_fashionadmin


admin.site.register(Booking)
admin.site.register(Coupon)
admin.site.register(Review)