from django.urls import path
from .views import *
from .views import RegisterUser
urlpatterns = [
    path('login/',LoginAPIView.as_view()),
    path('register',RegisterUser.as_view(),)
]
