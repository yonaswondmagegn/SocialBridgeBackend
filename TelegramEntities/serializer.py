from rest_framework import serializers
from .models import LoadenedEntitiy

class LoadenedEntitiySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadenedEntitiy
        fields = '__all__'


