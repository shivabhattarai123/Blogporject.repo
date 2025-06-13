from rest_framework import serializers
from .models import Category, Post, Comment
from django.contrib.auth.models import User


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] 

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Category already exists.")
        return value


# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'created_at',
            'updated_at',
            'author',
            'category',
            'category_id',
        ]


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post = serializers.StringRelatedField(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        source='post',
        write_only=True
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'body',
            'created_at',
            'author',
            'post',
            'post_id',
        ]
