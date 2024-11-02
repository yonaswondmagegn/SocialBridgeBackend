from rest_framework  import serializers
from core.serializer import UserSerializer
from .models import Profile

class ProfileSerialize(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = "__all__"