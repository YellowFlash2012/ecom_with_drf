from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_products, name="products"),
    path("<str:pk>", views.get_one_product, name="get_one_product"),
    path("upload_images", views.upload_product_images, name="upload_images")
]
