from django.db import models
from django.contrib.auth.models import User

class Category(models.TextChoices):
    ELECTRONICS = "Electronics",
    LAPTOPS = "Laptops",
    ARTS = "Arts",
    FOOD = "Food",
    HOME = "Home",
    KITCHEN = "Kitchen",

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200, default="", blank=False)
    description = models.TextField(max_length=1000, default="", blank=False)
    price = models.DecimalField(max_digits=7, default=0, decimal_places=2)
    category = models.CharField(max_length=30, choices=Category.choices)
    
    ratings=models.DecimalField(max_digits=3, default=0, decimal_places=2)
    
    stock=models.IntegerField(default=0)
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name