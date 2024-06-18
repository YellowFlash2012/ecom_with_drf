from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_products, name="products"),
    
    path("new", views.add_new_product, name="add_new_product"),
    
    path("<str:pk>", views.get_one_product, name="get_one_product"),
    
    path("<str:pk>/update", views.update_product, name="update_product"),
    
    path("<str:pk>/delete", views.delete_product, name="delete_product"),
    
    path("upload_images", views.upload_product_images, name="upload_images"),
]
