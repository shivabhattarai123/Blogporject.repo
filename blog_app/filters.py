from django_filters import FilterSet
from .models import Category, Post


class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = ['name','field',] # serach garda name ra field lae search hunxa
    
class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = ['title','category'] #serach garda title ra category lae search hunxa
    
