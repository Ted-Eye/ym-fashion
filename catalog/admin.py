from django.contrib import admin
from .models import Hairstyle, Product

# Register your models here.

#username:....admin password:...ym_fashionadmin

admin.site.register(Hairstyle)
admin.site.register(Product)