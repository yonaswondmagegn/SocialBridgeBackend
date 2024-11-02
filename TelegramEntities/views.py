from rest_framework.viewsets import ModelViewSet
from .models import LoadenedEntitiy
from .serializer import LoadenedEntitiySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

class LoadenedEntitiyViewSet(ModelViewSet):
    queryset = LoadenedEntitiy.objects.all()
    serializer_class = LoadenedEntitiySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'link', 'user', 'entity_type', 'label', 'date']
    search_fields = ['id', 'link', 'entity_type', 'label']
    ordering_fields = ['id', 'link', 'user', 'entity_type', 'label', 'date']
    ordering = ['id']

