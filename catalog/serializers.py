from rest_framework import serializers
from .models import Hairstyle, Product

class HairstyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hairstyle
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'