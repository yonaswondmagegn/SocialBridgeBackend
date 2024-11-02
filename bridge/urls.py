
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('TelegramEntities.urls')),
    path('',include('core.urls')),
    path('',include('Profile.urls')),
    path('',include('FacebookMarkatePlace.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
