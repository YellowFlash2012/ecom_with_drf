from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register_user, name="register_user"),
    
    path("profile", views.current_user, name="current_user"),
    
    path("profile/update", views.update_user_details, name="update_user_details"),
    
    path("forgot_password", views.forgot_password, name="forgot_password"),
    
    path("reset_password/<str:token>", views.reset_password, name="reset_password"),
    
    
]
