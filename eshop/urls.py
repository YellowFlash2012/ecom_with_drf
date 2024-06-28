
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("api/v1/products/", include("products.urls")),
    
    path("api/v1/orders/", include("orders.urls")),
    
    path("api/v1/users/", include("users.urls")),
    
    # simpleJWT config
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

handler404 = "eshop.utils.error_handling_views.handler404"
handler500 = "eshop.utils.error_handling_views.handler500"