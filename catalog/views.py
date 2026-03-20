from django.shortcuts import render
from rest_framework import permissions, viewsets
from .models import Hairstyle, Product
from .serializers import HairstyleSerializer, ProductSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
# @method_decorator(csrf_exempt, name='dispatch')
class HairstyleViewset(viewsets.ModelViewSet):
    queryset = Hairstyle.objects.all()
    serializer_class = HairstyleSerializer
    permission_classes = [permissions.AllowAny]


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]