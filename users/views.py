
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from datetime import timedelta, datetime

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
    user = UserSerializer(request.user, many=False)
    
    # print(user.data)
    
    return Response({"success":True, "message":f'Here are the details of {user.data["first_name"]}', "user":user.data}, status=status.HTTP_200_OK)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user_details(request):
    user = request.user
    data = request.data
    
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.username = data['email']
    user.email = data['email']
    
    if data["password"] != "":
        user.password = make_password(data["password"])
        
    user.save()
    
    serializer = UserSerializer(user, many=False)
    
    return Response({"success":True, "message": "Your details were successfully updated!", "data":serializer.data}, status=status.HTTP_201_CREATED)

# password reset views
def get_current_host(request):
    protocol = request.is_secure() and "https" or "http"
    host = request.get_host()
    
    return "{protocol}://{host}/".format(protocol=protocol, host=host)

@api_view(["POST"])
def forgot_password(request):
    data = request.data
    
    user = get_object_or_404(User, email=data["email"])
    
    token = get_random_string(39)
    expire_data = datetime.now() + timedelta(minutes=3)
    
    # from Profile model
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_data
    
    user.profile.save()
    
    host = get_current_host(request)
    
    link = "{host}api/v1/users/reset_pw/{token}".format(host=host, token=token)
    
    body = "Your password reset link is: {link}".format(link=link)
    
    send_mail(
        "Password reset for eShop",
        body,
        "noreply@eshop.com",
        [data["email"]]
    )
    
    return Response({"success":True, "message":"Password reset email sent to: {email}".format(email=data["email"])})

@api_view(["POST"])
def reset_password(request, token):
    data = request.data
    
    user = get_object_or_404(User, profile__reset_password_token=token)
    
    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({"success":False, "error":"token has expired"}, status=status.HTTP_400_BAD_REQUEST)
    
    if data["password"] != data["confirmPassword"]:
        return Response({"success":False, "error":"The passwords do NOT match!"}, status=status.HTTP_400_BAD_REQUEST)
    
    user.password = make_password(data["password"])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None
    
    user.profile.save()
    user.save()
    
    return Response({"success":True, "message":"Your password was successfully changed!"}, status=status.HTTP_201_CREATED)