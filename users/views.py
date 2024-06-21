from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .serializers import RegisterSerializer, UserSerializer
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
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user)
    
    # print(user.data)
    
    return Response({"success":True, "message":f'Here are the details of {user.data["first_name"]}', "user":user.data}, status=status.HTTP_200_OK)