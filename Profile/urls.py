from django.urls import path
from .views import ProfileViewSet
from rest_framework_nested import routers

route = routers.DefaultRouter()
route.register('profile',ProfileViewSet)

urlpatterns = route.urls