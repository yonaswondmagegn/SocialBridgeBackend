from django.urls import path
from .views import PostToFacebookMarketplace,GetProduct

urlpatterns = [
    path('fb',PostToFacebookMarketplace.as_view()),
    path('mp',GetProduct.as_view())
]