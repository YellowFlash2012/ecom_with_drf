from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create your views here.
@api_view(["POST"])
def register_user(request):
    data = request.data
    
    user = RegisterSerializer(data=data)
    
    if user.is_valid():
        if not User.objects.filter(username=data["email"]).exists():
            user = User.objects.create(
                first_name = data["first_name"],
                last_name = data["last_name"],
                email = data["email"],
                username = data["email"],
                password = make_password(data["password"]),
            )
            
            return Response({"success":True, "message": f"Welcome aboard, {user.first_name}!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success":False, "message":"A user with this email already exists!"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user.error, status=status.HTTP_400_BAD_REQUEST)