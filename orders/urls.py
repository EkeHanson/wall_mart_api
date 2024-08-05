from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderGrabbingViewSet

router = DefaultRouter()
# router.register(r'orders', OrderViewSet)
router.register(r'order-grabbings', OrderGrabbingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
