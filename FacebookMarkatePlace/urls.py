from django.urls import path
from .views import PostToFacebookMarketplace

urlpatterns = [
    path('fb',PostToFacebookMarketplace.as_view())
]