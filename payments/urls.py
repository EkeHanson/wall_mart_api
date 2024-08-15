from rest_framework.routers import DefaultRouter
from .views import BankDetailViewSet, CryptoWalletDetailViewSet

router = DefaultRouter()
router.register(r'bank-details', BankDetailViewSet)
router.register(r'crypto-wallets', CryptoWalletDetailViewSet)

urlpatterns = router.urls
