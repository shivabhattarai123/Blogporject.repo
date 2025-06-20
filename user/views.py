from django.shortcuts import render
from rest_framework .views import APIView
from rest_framework .response import Response
from rest_framework .serializers import ValidationError
from django .contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from .models import UserProfile
# Create your views here.
class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            raise ValidationError({
                "details": "Both username and password required"
            })
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            try:
                role = user.profile.role
            except UserProfile.DoesNotExist:
                role = None  # or some default, or handle error differently

            return Response({
                "token": token.key,
                "username": user.username,
                "role": role
            }, status=status.HTTP_202_ACCEPTED)
        return Response({
            "details": "User is not registered."
        }, status=status.HTTP_401_UNAUTHORIZED)

class RegisterUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role')

        if not role in ['author', 'reader']:
            return Response({"error": "Role must be 'author' or 'reader'"}, status=400)

        if username and password:
            if User.objects.filter(username=username).exists():
                return Response({"error": "Username already taken"}, status=400)

            user = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user, role=role)
            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                "message": "User registered",
                "token": token.key,
                "role": role
            }, status=status.HTTP_201_CREATED)

        return Response({"error": "Username and password required"}, status=400)
    
    




