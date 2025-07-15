from django.shortcuts import render
from rest_framework .views import APIView
from rest_framework .response import Response
from rest_framework .serializers import ValidationError
from django .contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveUpdateAPIView
from .models import UserProfile
User = get_user_model()
# Create your views here.
class LoginAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        if not phone_number or not password:
            raise ValidationError({"details": "Phone number and password are required."})

        user = authenticate(username=phone_number, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            role = user.userprofile.role if hasattr(user, 'userprofile') else None
            return Response({
                "token": token.key,
                "username": user.username,
                "role": role
            }, status=status.HTTP_202_ACCEPTED)

        return Response({"details": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)



class RegisterUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number')
        email = request.data.get('email', '')  # optional
        role = request.data.get('role')

        # Validate role
        if role not in ['author', 'reader']:
            return Response({"error": "Role must be 'author' or 'reader'"}, status=400)

        # Validate required fields
        if not username or not password or not phone_number:
            return Response({"error": "Username, password, and phone_number are required"}, status=400)

        # Check if username exists
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=400)

        # Check if phone number exists
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({"error": "Phone number already taken"}, status=400)

        # Create user with all required fields
        user = User.objects.create_user(
            username=username,
            password=password,
            phone_number=phone_number,
            email=email
        )
        user.userprofile.role = role
        user.userprofile.save()

        # Create auth token
        token, _ = Token.objects.get_or_create(user=user)

        # Success response
        return Response({
            "message": "User registered successfully",
            "token": token.key,
            "role": role
        }, status=status.HTTP_201_CREATED)



class MyProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile = self.request.user.userprofile
        if profile.role != 'reader':
            raise PermissionDenied("Only readers can access this view.")
        return profile