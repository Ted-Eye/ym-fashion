
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from catalog import views
from clients import views as clientViews
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

#CATALOG URLS
router = routers.DefaultRouter()
router.register("hairstyles", views.HairstyleViewset, basename='hairstyles' )
router.register("products", views.ProductViewset, basename='products' )

#CLIENTS URLS
router.register("bookings", clientViews.BookingViewset, basename='bookings' )
router.register("coupons", clientViews.CouponViewset, basename='coupons' )
router.register("reviews", clientViews.ReviewViewset, basename='reviews' )


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='access-token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('admin/', admin.site.urls),
    path('catalog/', include(router.urls)),
    path('clients/', include(router.urls)),
    path('payment/', include("payment.urls"))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
