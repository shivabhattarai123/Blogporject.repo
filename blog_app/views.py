from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.shortcuts import get_object_or_404
from .models import Category
from .serializers import *
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView,ListCreateAPIView,RetrieveAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework .viewsets import ModelViewSet

# create your views here

# class CategoryList(ListCreateAPIView):
#     queryset = Category.objects
#     serializer_class = CategorySerializers
    
# class CategoryDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializers
#     lookup_field = 'id'
    
#     def destroy(self,request,id):
#         Category = get_object_or_404(Category,id=id)
#         Category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryAPiView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class PostViewset(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
class CommentViewset(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer