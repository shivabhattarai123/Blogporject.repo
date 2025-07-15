from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import Category
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()   # Get the custom user model if you’re using one


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] 

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name','field']

    def save(self, **kwargs):
        validated_data = self.validated_data
        name = validated_data.get('name')
        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError({
                'detail': 'Category already exists.'
            })

        category = Category(**validated_data)
        category.save()
        return category

# Post Serializer
# class PostSerializer(serializers.ModelSerializer):
#     author = UserSerializer()   # Show author details but don't allow changing it directly
#     category = serializers.StringRelatedField(read_only=True)
#     category_id = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all(),
#         source='category',
#         write_only=True
#     )

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
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
            'author',
            'category',
            'category_id',
        ]

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
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
            'content',
            'created_at',
            'post',
            'post_id',
            # 'Category_id',
        ]
