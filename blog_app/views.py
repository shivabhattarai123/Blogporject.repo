from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from .models import *
from django.shortcuts import get_object_or_404
from .models import Category
from .serializers import *
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView,ListCreateAPIView,RetrieveAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework .viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from .filters import CategoryFilter, PostFilter
from django_filters import rest_framework as filter
from rest_framework.permissions import IsAuthenticated
from .permission import IsAuthenticatedOrReadonly
from user.models import UserProfile
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
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





class CategoryList(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    
@extend_schema(
    parameters=[
        OpenApiParameter(name='name', description='Filter by name', required=False, type=str),],
    description='this is the category delete',
    )
def get(self, request, *args, **kwargs):
        name = request.query_params.get('name')
        if name:
            Category = Category.objects.filter(name=name)
            serializers = CategorySerializer(Category, many=True)
            return Response(serializers.data)
        return super().list(request)
    
@extend_schema(
    parameters=[
        OpenApiParameter(name='name', description='Filter by name', required=False, type=str),],
    description='this is the category delete',
    )
def destroy(self,request,pk):
    Category = get_object_or_404(Category,id=pk)
    Category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)








class CategoryAPiView(ModelViewSet):
    queryset = Category.objects.select_related().all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,filter.DjangoFilterBackend)
    filterset_class = CategoryFilter
    search_fields = ('name',)
    permission_classes = [IsAuthenticatedOrReadonly] 
    
    def perform_create(self, serializer):
        if self.request.user.userprofile.role != 'author':
            raise PermissionDenied("Only authors can create categories.")
        serializer.save()
        
class PostViewset(ModelViewSet):
    queryset = Post.objects.select_related().all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,filter.DjangoFilterBackend)
    filterset_class = PostFilter
    search_fields = ('name',)
    permission_classes = [IsAuthenticated] 
    
    def perform_create(self, serializer):
        if self.request.user.userprofile.role != 'author':
            raise PermissionDenied("Only authors can create posts.")
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.userprofile.role != 'author':
            raise PermissionDenied("Only authors can update posts.")
        serializer.save()
    def perform_destroy(self, instance):
        if self.request.user.userprofile.role != 'author':
            raise PermissionDenied("Only authors can delete posts.")
        instance.delete()
    
class CommentViewset(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination  
    
    def perform_create(self, serializer):
        if self.request.user.userprofile.role != 'reader':
            raise PermissionDenied("Only readers can create comments.")
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
