# recharge/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RechargeViewSet

router = DefaultRouter()
router.register(r'recharges', RechargeViewSet, basename='recharge')

urlpatterns = [
    path('', include(router.urls)),
]
