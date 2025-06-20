from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'categories',CategoryAPiView)
router.register(r'post',PostViewset)
router.register(r'comments',CommentViewset)
urlpatterns = [
    # path('category',CategoryAPiView.as_view({'get':'list','post':'create'})),
    # path('category/<int:pk>/',CategoryAPiView.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'}))

] +router.urls