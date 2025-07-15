from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile
User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'role', 'bio']  # Add bio or other editable fields
        read_only_fields = ['role']  # Prevent readers from changing their role

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)  # Include the related UserProfile using the nested serializer, read-only

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}   # Ensures password is only used when writing (POST/PUT), not shown in responses
        }

