from django.urls import  path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_nested import routers
from .views import RegisterUser


urlpatterns = [
    path('register/',RegisterUser.as_view()),
    path('refresh/',TokenRefreshView.as_view())
]