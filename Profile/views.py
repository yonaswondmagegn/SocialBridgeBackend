from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import ProfileSerialize
from django_filters.rest_framework import DjangoFilterBackend

from .models import Profile


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerialize
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user"]

