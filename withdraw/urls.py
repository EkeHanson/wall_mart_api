from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WithdrawViewSet

router = DefaultRouter()
router.register(r'withdraw', WithdrawViewSet, basename='withdrawal')

urlpatterns = [
    path('', include(router.urls)),
]
