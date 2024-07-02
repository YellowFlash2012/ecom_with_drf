from django.urls import path
from . import views

urlpatterns = [
    path("new", views.new_order, name="new_order"),
    
    path("", views.get_user_orders, name="get_user_orders"),
    
    path("<str:pk>", views.get_single_order, name="get_single_order"),
    
    path("<str:pk>/process", views.process_single_order, name="process_single_order"),
    
    path("<str:pk>/delete", views.delete_single_order, name="delete_single_order"),
    
    path("create-checkout-session", views.create_checkout_session, name="create_checkout_session"),
    

]
