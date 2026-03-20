from django.db import models
# models.py
from django.db import models
import cloudinary.uploader

class Hairstyle(models.Model):
    # image = models.ImageField(upload_to='uploads/images')
    image_url = models.URLField(null=True, blank=True)
    public_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=50, blank=False)
    #treatment = models.Choices() 
    # Choices will be: standard touch, premium touch, diamond treatment
    price = models.PositiveIntegerField(blank=False)
    description = models.CharField(max_length=100)
    treatment_duration = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        if self.public_id:
            cloudinary.uploader.destroy(self.public_id)
        super().delete(*args, **kwargs)

class Product(models.Model):
    # image = models.ImageField(upload_to='uploads/images')
    image_url = models.URLField(null=True, blank=True)
    public_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        if self.public_id:
            cloudinary.uploader.destroy(self.public_id)
        super().delete(*args, **kwargs)
