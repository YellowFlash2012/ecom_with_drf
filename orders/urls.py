from django.urls import path
from . import views

urlpatterns = [
    path("", views.new_order, name="new_order"),
    

]
