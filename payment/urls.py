from django.urls import path
from .views import initiate_payment, check_payment_status

urlpatterns = [
    path('initiate/', initiate_payment),
    path('status/<str:reference>/', check_payment_status),
]