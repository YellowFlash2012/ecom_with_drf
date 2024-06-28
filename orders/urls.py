from django.urls import path
from . import views

urlpatterns = [
    path("new", views.new_order, name="new_order"),
    
    path("", views.get_user_orders, name="get_user_orders"),
    
    path("<str:pk>", views.get_single_order, name="get_single_order"),
    

]
