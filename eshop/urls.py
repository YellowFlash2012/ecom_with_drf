
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("api/v1/products/", include("products.urls")),
    
    path("api/v1/users/", include("users.urls")),
]

handler404 = "eshop.utils.error_handling_views.handler404"
handler500 = "eshop.utils.error_handling_views.handler500"