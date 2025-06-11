from django.urls import path, include
from .views import *
urlpatterns = [
    path('category',category_list),
    path('category/<id>/',category_detail)
]