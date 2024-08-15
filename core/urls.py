from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenVerifyView,TokenRefreshView,)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/orders/', include('orders.urls')),

     path('api/recharge/', include('recharge.urls')),  # Include the recharge URLs
     path('api/payments/', include('payments.urls')),

    path('api/accounts/', include('accounts.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
